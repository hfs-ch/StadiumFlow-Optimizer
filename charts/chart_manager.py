from __future__ import annotations

from typing import Dict, List

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class ChartManager(FigureCanvasQTAgg):
    def __init__(self, parent=None) -> None:
        self.figure = Figure(figsize=(8, 5), facecolor="#0b1020")
        super().__init__(self.figure)
        self.setParent(parent)

    def render_overview(self, metrics: Dict[str, float], history: List[Dict[str, float]]) -> None:
        self.figure.clear()
        ax1 = self.figure.add_subplot(221)
        ax2 = self.figure.add_subplot(222)
        ax3 = self.figure.add_subplot(223)
        ax4 = self.figure.add_subplot(224)

        self._style_axis(ax1)
        self._style_axis(ax2)
        self._style_axis(ax3)
        self._style_axis(ax4)

        names = ["Police", "Stewards", "Benevoles"]
        values = [metrics.get("x1", 0), metrics.get("x2", 0), metrics.get("x3", 0)]
        ax1.bar(names, values, color=["#00c2ff", "#00ffc8", "#66b2ff"])
        ax1.set_title("Repartition personnel", color="#d7f6ff")

        budget_parts = [
            1500 * values[0],
            800 * values[1],
            200 * values[2],
        ]
        ax2.pie(budget_parts, labels=names, autopct="%1.1f%%", colors=["#00c2ff", "#00ffc8", "#66b2ff"])
        ax2.set_title("Diagramme budget", color="#d7f6ff")

        if history:
            iterations = [h["iteration"] for h in history]
            z_values = [h["z"] for h in history]
            ax3.plot(iterations, z_values, marker="o", color="#00ffc8", linewidth=2)
        ax3.set_title("Evolution du flux", color="#d7f6ff")
        ax3.set_xlabel("Iteration", color="#8dc9e6")
        ax3.set_ylabel("Z", color="#8dc9e6")

        heatmap = np.array([[values[0], values[1]], [values[2], metrics.get("flow", 0)]], dtype=float)
        ax4.imshow(heatmap, cmap="viridis", aspect="auto")
        ax4.set_title("Heatmap saturation", color="#d7f6ff")
        ax4.set_xticks([0, 1], labels=["Zone A", "Zone B"])
        ax4.set_yticks([0, 1], labels=["Portiques", "Flux"])

        self.figure.tight_layout()
        self.draw()

    @staticmethod
    def _style_axis(axis) -> None:
        axis.set_facecolor("#121a2f")
        axis.tick_params(colors="#8dc9e6")
        for spine in axis.spines.values():
            spine.set_color("#2a4268")
