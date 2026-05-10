from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class PDFReportGenerator:
    def create_report(
        self,
        output_path: Path,
        metrics: Dict[str, float],
        saturated_constraints: List[str],
        recommendations: List[str],
    ) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(str(output_path), pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("SONARGES SmartFlow Optimizer - Rapport Analytique", styles["Title"]))
        story.append(Paragraph(datetime.now().strftime("%d/%m/%Y %H:%M"), styles["Normal"]))
        story.append(Spacer(1, 12))

        table_data = [
            ["KPI", "Valeur"],
            ["Police (x1)", f"{metrics.get('x1', 0):.2f}"],
            ["Stewards (x2)", f"{metrics.get('x2', 0):.2f}"],
            ["Benevoles (x3)", f"{metrics.get('x3', 0):.2f}"],
            ["Flux maximal (Z)", f"{metrics.get('flow', 0):.2f}"],
            ["Budget utilise", f"{metrics.get('budget_used', 0):.2f}"],
        ]
        table = Table(table_data, colWidths=[240, 220])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f1e33")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f4f8fc")),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 12))

        sat = ", ".join(saturated_constraints) if saturated_constraints else "Aucune"
        story.append(Paragraph(f"<b>Contraintes saturees:</b> {sat}", styles["Normal"]))
        story.append(Spacer(1, 8))

        story.append(Paragraph("<b>Recommandations intelligentes:</b>", styles["Normal"]))
        for rec in recommendations:
            story.append(Paragraph(f"- {rec}", styles["Normal"]))

        doc.build(story)
        return output_path
