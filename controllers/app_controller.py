from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

from PyQt6.QtWidgets import QApplication

from exports.export_manager import ExportManager
from models.optimization_model import MATCH_SCENARIOS, OptimizationConfig
from reports.report_generator import PDFReportGenerator
from solver.simplex_solver import SmartFlowSimplexSolver
from ui.main_window import MainWindow
from utils.logger import AppLogger


class AppController:
    def __init__(self) -> None:
        self.window = MainWindow()
        self.logger = AppLogger()
        self.export_manager = ExportManager()
        self.report_generator = PDFReportGenerator()
        self.saturated_constraints: List[str] = []
        self.recommendations: List[str] = []

        self.window.btn_optimize.clicked.connect(self.run_optimization)
        self.window.btn_start_sim.clicked.connect(self.start_simulation)
        self.window.btn_stop_sim.clicked.connect(self.stop_simulation)
        self.window.btn_export_pdf.clicked.connect(self.export_pdf)
        self.window.btn_export_excel.clicked.connect(self.export_excel)
        self.window.btn_capture.clicked.connect(self.export_png)

    def show(self) -> None:
        self.window.show()
        self.run_optimization()

    def run_optimization(self) -> None:
        config = OptimizationConfig(
            budget_limit=float(self.window.in_budget.text() or 30000),
            infra_limit=float(self.window.in_infra.text() or 16),
            space_limit=float(self.window.in_space.text() or 36),
            min_police=float(self.window.in_security.text() or 4),
        )
        solver = SmartFlowSimplexSolver(config)
        output = solver.solve()
        result = output.result
        self.saturated_constraints = result.saturated_constraints

        budget_used = 1500 * result.x1_police + 800 * result.x2_stewards + 200 * result.x3_volunteers
        infra_used = result.x1_police + result.x2_stewards + 0.5 * result.x3_volunteers
        metrics = {
            "x1": result.x1_police,
            "x2": result.x2_stewards,
            "x3": result.x3_volunteers,
            "flow": result.z_max,
            "budget_used": budget_used,
            "infra_pct": (infra_used / config.infra_limit) * 100,
            "state": "Stable" if result.z_max > 250 else "Surveillance",
        }
        self.window.refresh_dashboard(metrics)

        solution_text = (
            f"x1 (Police) = {result.x1_police:.2f}\n"
            f"x2 (Stewards) = {result.x2_stewards:.2f}\n"
            f"x3 (Benevoles) = {result.x3_volunteers:.2f}\n"
            f"Z max = {result.z_max:.2f}\n\n"
            f"Contraintes saturees: {', '.join(result.saturated_constraints) or 'Aucune'}\n\n"
            "Iterations Simplexe:\n"
        )
        for it in result.simplex_iterations:
            solution_text += (
                f"Iter {it['iteration']}: x1={it['x1']:.2f}, x2={it['x2']:.2f}, "
                f"x3={it['x3']:.2f}, Z={it['z']:.2f}\n"
            )

        self.window.show_optimization_result(solution_text, result.simplex_iterations)
        self.window.refresh_charts()
        self.logger.log("Optimisation executee avec succes.")
        for line in output.logs:
            self.logger.log(line)

        self.recommendations = self._generate_recommendations(metrics)
        self.logger.log("Recommandations: " + " | ".join(self.recommendations))
        self.window.append_logs(self.logger.list_messages())

    def start_simulation(self) -> None:
        scenario_name = self.window.scenario_combo.currentText()
        scenario = MATCH_SCENARIOS[scenario_name]
        security_level = min(1.0, (self.window.metrics.get("x1", 4) / 8))
        self.window.sim_view.start(arrival_rate=scenario["arrival_rate"], security_level=security_level)
        self.window.start_live_pull()
        self.logger.log(f"Simulation demarree ({scenario_name}).")
        self.window.append_logs([self.logger.list_messages()[-1]])

    def stop_simulation(self) -> None:
        self.window.sim_view.stop()
        self.window.stop_live_pull()
        self.logger.log("Simulation arretee.")
        self.window.append_logs([self.logger.list_messages()[-1]])

    def export_pdf(self) -> None:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path("reports") / f"rapport_smartflow_{now}.pdf"
        self.report_generator.create_report(path, self.window.metrics, self.saturated_constraints, self.recommendations)
        self.window.report_status.setText(f"PDF genere: {path}")
        QApplication.beep()

    def export_excel(self) -> None:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path("exports") / f"smartflow_{now}.xlsx"
        self.export_manager.export_excel(path, self.window.metrics)
        self.window.report_status.setText(f"Excel genere: {path}")

    def export_png(self) -> None:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path("exports") / f"dashboard_{now}.png"
        self.export_manager.export_dashboard_png(path, self.window)
        self.window.report_status.setText(f"Capture dashboard: {path}")

    @staticmethod
    def _generate_recommendations(metrics: dict) -> List[str]:
        recs = []
        infra = metrics.get("infra_pct", 0)
        if infra > 85:
            recs.append("Le systeme recommande l'ouverture de 2 portiques supplementaires.")
        if metrics.get("x2", 0) < 4:
            recs.append("Augmenter les stewards pour reduire la congestion.")
        if metrics.get("budget_used", 0) > 28500:
            recs.append("Budget proche de la limite: prioriser des benevoles en renfort.")
        if not recs:
            recs.append("Configuration actuelle optimale et stable.")
        return recs
