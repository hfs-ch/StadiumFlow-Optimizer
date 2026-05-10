from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget


class ExportManager:
    def export_excel(self, path: Path, metrics: Dict[str, float]) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(
            [
                {"Indicateur": "x1_police", "Valeur": metrics.get("x1", 0)},
                {"Indicateur": "x2_stewards", "Valeur": metrics.get("x2", 0)},
                {"Indicateur": "x3_benevoles", "Valeur": metrics.get("x3", 0)},
                {"Indicateur": "flux_maximal", "Valeur": metrics.get("flow", 0)},
                {"Indicateur": "budget_utilise", "Valeur": metrics.get("budget_used", 0)},
                {"Indicateur": "infrastructure_pct", "Valeur": metrics.get("infra_pct", 0)},
            ]
        )
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Synthese")
        return path

    def export_dashboard_png(self, path: Path, widget: QWidget) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        pixmap = QPixmap(widget.size())
        widget.render(pixmap)
        pixmap.save(str(path), "PNG")
        return path
