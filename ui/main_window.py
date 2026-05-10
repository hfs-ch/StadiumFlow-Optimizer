from __future__ import annotations

from typing import Dict, List

from datetime import datetime

from PyQt6.QtCore import QPropertyAnimation, QTimer
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from charts.chart_manager import ChartManager
from simulations.realtime_simulation import StadiumSimulationView
from ui.styles import APP_STYLE


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SONARGES SmartFlow Optimizer")
        self.resize(1480, 860)
        self.setStyleSheet(APP_STYLE)

        self.metrics: Dict[str, float] = {}
        self.simplex_iterations: List[Dict[str, float]] = []

        self.central = QWidget()
        self.setCentralWidget(self.central)
        root = QHBoxLayout(self.central)

        self.sidebar = QFrame(objectName="sidebar")
        self.sidebar.setFixedWidth(250)
        side_layout = QVBoxLayout(self.sidebar)
        side_layout.addWidget(QLabel("SONARGES", objectName="title"))
        side_layout.addWidget(QLabel("SmartFlow Optimizer"))
        side_layout.addSpacing(12)

        self.stack = QStackedWidget()
        self.pages = {
            "Dashboard": self._build_dashboard_page(),
            "Optimisation": self._build_optimization_page(),
            "Simulation": self._build_simulation_page(),
            "Graphiques": self._build_charts_page(),
            "Rapports": self._build_reports_page(),
            "Logs": self._build_logs_page(),
        }
        self._page_animation: QPropertyAnimation | None = None
        for name, page in self.pages.items():
            btn = QPushButton(name)
            btn.setObjectName("navButton")
            btn.clicked.connect(lambda _, n=name: self._go_to_page(n))
            side_layout.addWidget(btn)
            self.stack.addWidget(page)
        side_layout.addStretch()

        main_area = QWidget()
        main_layout = QVBoxLayout(main_area)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        topbar = QFrame(objectName="topbar")
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(12, 8, 12, 8)
        self.system_status = QLabel("Systeme: OPERATIONNEL")
        self.system_status.setStyleSheet("color:#76f8a5;font-weight:700;")
        self.alert_level = QLabel("Alerte: NIVEAU BAS")
        self.alert_level.setStyleSheet("color:#ffd674;font-weight:600;")
        self.clock_label = QLabel("--:--:--")
        self.clock_label.setStyleSheet("color:#9fdfff;font-weight:600;")
        topbar_layout.addWidget(self.system_status)
        topbar_layout.addStretch()
        topbar_layout.addWidget(self.alert_level)
        topbar_layout.addSpacing(14)
        topbar_layout.addWidget(self.clock_label)

        content_pane = QFrame(objectName="contentPane")
        content_layout = QVBoxLayout(content_pane)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.addWidget(self.stack)

        main_layout.addWidget(topbar)
        main_layout.addWidget(content_pane, 1)

        root.addWidget(self.sidebar)
        root.addWidget(main_area, 1)

        self.live_timer = QTimer(self)
        self.live_timer.timeout.connect(self._pull_live_stats)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)
        self._update_clock()

    def _build_dashboard_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Dashboard Principal", objectName="title"))

        hero = QFrame(objectName="heroCard")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(14, 12, 14, 12)
        hero_title = QLabel("Vue 3D Supervision - Stade Marrakech")
        hero_title.setStyleSheet("font-size:16px;font-weight:700;color:#b5f1ff;")
        self.hero_subtitle = QLabel("Analyse predictive active - Mode FIFA Control")
        self.hero_subtitle.setStyleSheet("color:#8bc0da;")
        left_box = QVBoxLayout()
        left_box.addWidget(hero_title)
        left_box.addWidget(self.hero_subtitle)
        hero_layout.addLayout(left_box, 1)
        self.live_congestion = QProgressBar()
        self.live_congestion.setRange(0, 100)
        self.live_congestion.setValue(12)
        self.live_congestion.setFormat("Congestion: %p%")
        self.live_congestion.setFixedWidth(290)
        hero_layout.addWidget(self.live_congestion)
        layout.addWidget(hero)

        grid = QGridLayout()
        self.kpi_labels = {}
        for i, key in enumerate(["Flux max", "Budget", "Infrastructure", "Personnel total", "Etat systeme"]):
            card = QFrame(objectName="card")
            glow = QGraphicsDropShadowEffect(self)
            glow.setBlurRadius(28)
            glow.setOffset(0, 0)
            card.setGraphicsEffect(glow)
            card_layout = QVBoxLayout(card)
            title = QLabel(key, objectName="kpiTitle")
            card_layout.addWidget(title)
            val = QLabel("--")
            val.setObjectName("kpiValue")
            card_layout.addWidget(val)
            self.kpi_labels[key] = val
            grid.addWidget(card, i // 3, i % 3)
        layout.addLayout(grid)
        return page

    def _build_optimization_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Ecran Optimisation", objectName="title"))
        form = QFormLayout()
        self.in_budget = QLineEdit("30000")
        self.in_infra = QLineEdit("16")
        self.in_space = QLineEdit("36")
        self.in_security = QLineEdit("4")
        form.addRow("Budget max", self.in_budget)
        form.addRow("Infrastructure max", self.in_infra)
        form.addRow("Espace max", self.in_space)
        form.addRow("Securite minimale x1", self.in_security)
        layout.addLayout(form)
        self.btn_optimize = QPushButton("Lancer optimisation")
        layout.addWidget(self.btn_optimize)
        self.optimization_output = QTextEdit()
        self.optimization_output.setReadOnly(True)
        layout.addWidget(self.optimization_output, 1)
        return page

    def _build_simulation_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Simulation Temps Reel", objectName="title"))
        controls = QHBoxLayout()
        self.scenario_combo = QComboBox()
        self.scenario_combo.addItems(
            ["Faible affluence", "Moyenne affluence", "Forte affluence", "Scenario critique"]
        )
        self.btn_start_sim = QPushButton("Demarrer simulation")
        self.btn_stop_sim = QPushButton("Arreter simulation")
        controls.addWidget(self.scenario_combo)
        controls.addWidget(self.btn_start_sim)
        controls.addWidget(self.btn_stop_sim)
        layout.addLayout(controls)
        self.sim_view = StadiumSimulationView()
        layout.addWidget(self.sim_view)
        self.sim_stats_label = QLabel("Stats live: --")
        layout.addWidget(self.sim_stats_label)
        return page

    def _build_charts_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Graphiques Dynamiques", objectName="title"))
        self.chart_canvas = ChartManager(page)
        layout.addWidget(self.chart_canvas, 1)
        return page

    def _build_reports_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Rapports & Exports", objectName="title"))
        self.btn_export_pdf = QPushButton("Exporter PDF premium")
        self.btn_export_excel = QPushButton("Exporter Excel")
        self.btn_capture = QPushButton("Capture dashboard PNG")
        layout.addWidget(self.btn_export_pdf)
        layout.addWidget(self.btn_export_excel)
        layout.addWidget(self.btn_capture)
        self.report_status = QLabel("Aucun export effectue.")
        layout.addWidget(self.report_status)
        layout.addStretch()
        return page

    def _build_logs_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Logs & Historique", objectName="title"))
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        layout.addWidget(self.logs_text, 1)
        return page

    def refresh_dashboard(self, metrics: Dict[str, float]) -> None:
        self.metrics = metrics
        self.kpi_labels["Flux max"].setText(f"{metrics.get('flow', 0):.2f}/min")
        self.kpi_labels["Budget"].setText(f"{metrics.get('budget_used', 0):.0f}")
        self.kpi_labels["Infrastructure"].setText(f"{metrics.get('infra_pct', 0):.1f}%")
        total = metrics.get("x1", 0) + metrics.get("x2", 0) + metrics.get("x3", 0)
        self.kpi_labels["Personnel total"].setText(f"{total:.1f}")
        self.kpi_labels["Etat systeme"].setText(metrics.get("state", "Nominal"))
        self.system_status.setText(f"Systeme: {metrics.get('state', 'Stable').upper()}")
        infra_pct = metrics.get("infra_pct", 0)
        if infra_pct > 90:
            self.alert_level.setText("Alerte: NIVEAU ELEVE")
            self.alert_level.setStyleSheet("color:#ff7c8a;font-weight:700;")
        elif infra_pct > 75:
            self.alert_level.setText("Alerte: NIVEAU MOYEN")
            self.alert_level.setStyleSheet("color:#ffd674;font-weight:700;")
        else:
            self.alert_level.setText("Alerte: NIVEAU BAS")
            self.alert_level.setStyleSheet("color:#7dffc8;font-weight:700;")
        self.live_congestion.setValue(int(max(0, min(100, infra_pct))))
        if infra_pct > 85:
            self.hero_subtitle.setText("Risque de congestion - recommander ouverture portiques")
        else:
            self.hero_subtitle.setText("Flux controle - supervision predictive stable")

    def show_optimization_result(self, text: str, iterations: List[Dict[str, float]]) -> None:
        self.optimization_output.setPlainText(text)
        self.simplex_iterations = iterations

    def append_logs(self, lines: List[str]) -> None:
        for line in lines:
            self.logs_text.append(line)

    def refresh_charts(self) -> None:
        if self.metrics:
            self.chart_canvas.render_overview(self.metrics, self.simplex_iterations)

    def start_live_pull(self) -> None:
        self.live_timer.start(400)

    def stop_live_pull(self) -> None:
        self.live_timer.stop()

    def _pull_live_stats(self) -> None:
        s = self.sim_view.get_stats()
        self.sim_stats_label.setText(
            "Stats live | supporters/min: "
            f"{s.supporters_per_min:.1f} | attente: {s.avg_wait:.2f} min | "
            f"congestion: {s.congestion_rate*100:.1f}% | portiques actifs: {s.active_gates} | "
            f"securite: {s.security_level*100:.0f}% | capacite restante: {s.remaining_capacity:.1f}%"
        )

    def _update_clock(self) -> None:
        self.clock_label.setText(datetime.now().strftime("%H:%M:%S"))

    def _go_to_page(self, name: str) -> None:
        target = self.pages[name]
        self.stack.setCurrentWidget(target)
        effect = QGraphicsOpacityEffect(target)
        target.setGraphicsEffect(effect)
        self._page_animation = QPropertyAnimation(effect, b"opacity", self)
        self._page_animation.setDuration(280)
        self._page_animation.setStartValue(0.18)
        self._page_animation.setEndValue(1.0)
        self._page_animation.start()
