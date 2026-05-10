from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from PyQt6.QtCore import QPointF, QTimer
from PyQt6.QtGui import QColor, QBrush, QPen, QPolygonF
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView


@dataclass
class SimulationStats:
    supporters_per_min: float = 0.0
    avg_wait: float = 0.0
    congestion_rate: float = 0.0
    active_gates: int = 16
    security_level: float = 0.0
    remaining_capacity: float = 0.0


class StadiumSimulationView(QGraphicsView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setMinimumHeight(340)
        self.scene.setSceneRect(0, 0, 920, 300)
        self.setStyleSheet("background:#0b1020;border:1px solid #2a4268;border-radius:14px;")

        self.gates: List[QGraphicsRectItem] = []
        self.supporters: List[QGraphicsEllipseItem] = []
        self.scan_rings: List[QGraphicsEllipseItem] = []
        self.floor_lines: List[QGraphicsPolygonItem] = []
        self.stats = SimulationStats()
        self.arrival_rate = 120
        self._tick = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_frame)
        self._init_map()

    def _init_map(self) -> None:
        self.scene.clear()
        self.gates.clear()
        self.scan_rings.clear()
        self.floor_lines.clear()

        # 3D-like top-down perspective floor (presentation immersive)
        floor = QPolygonF(
            [
                QPointF(25, 40),
                QPointF(895, 40),
                QPointF(850, 286),
                QPointF(70, 286),
            ]
        )
        self.scene.addPolygon(floor, QPen(QColor("#1f3555"), 2), QBrush(QColor(8, 20, 40, 200)))

        for i in range(7):
            inset = i * 10
            line_poly = QPolygonF(
                [
                    QPointF(40 + inset, 65 + i * 24),
                    QPointF(880 - inset, 65 + i * 24),
                    QPointF(840 - inset, 82 + i * 24),
                    QPointF(80 + inset, 82 + i * 24),
                ]
            )
            band = self.scene.addPolygon(line_poly, QPen(QColor("#183352")), QBrush(QColor(15, 34, 58, 80)))
            self.floor_lines.append(band)

        gate_w = 40
        for i in range(16):
            x = 70 + i * (gate_w + 8)
            gate = self.scene.addRect(x, 246, gate_w, 32, QPen(QColor("#284967")), QBrush(QColor("#19d17f")))
            self.gates.append(gate)

        # Radar rings for control-room effect
        for size in (40, 80, 120):
            ring = self.scene.addEllipse(16 - size / 2, 16 - size / 2, size, size, QPen(QColor(88, 212, 255, 90), 1))
            self.scan_rings.append(ring)

    def start(self, arrival_rate: int, security_level: float) -> None:
        self.arrival_rate = arrival_rate
        self.stats.security_level = security_level
        self.timer.start(120)

    def stop(self) -> None:
        self.timer.stop()

    def _spawn_supporters(self, count: int) -> None:
        for _ in range(count):
            lane = random.randint(0, 8)
            y = 58 + lane * 20 + random.uniform(-3, 3)
            size = 5 + lane * 0.45
            person = self.scene.addEllipse(76, y, size, size, QPen(QColor("#31c4ff")), QBrush(QColor("#8ee9ff")))
            self.supporters.append(person)

    def _update_frame(self) -> None:
        self._tick += 1
        spawn = max(1, int(self.arrival_rate / 200))
        self._spawn_supporters(spawn)
        self._animate_radar()

        exited = 0
        for person in list(self.supporters):
            depth = max(0.5, person.rect().height() / 8)
            person.moveBy(random.uniform(2.0, 4.0) * depth, random.uniform(-0.5, 0.5))
            if person.rect().x() + person.pos().x() > 860:
                self.scene.removeItem(person)
                self.supporters.remove(person)
                exited += 1

        density = len(self.supporters) / 180.0
        self.stats.congestion_rate = min(1.0, density)
        self.stats.avg_wait = round(0.5 + density * 5.5, 2)
        self.stats.supporters_per_min = round(exited * 25.0, 1)
        self.stats.active_gates = 16 if density < 0.8 else 12
        self.stats.remaining_capacity = round(max(0.0, 1.0 - density) * 100, 1)
        self._refresh_gates()

    def _refresh_gates(self) -> None:
        for i, gate in enumerate(self.gates):
            if i >= self.stats.active_gates:
                gate.setBrush(QBrush(QColor("#5f1f2b")))
            elif self.stats.congestion_rate < 0.45:
                gate.setBrush(QBrush(QColor("#19d17f")))
            elif self.stats.congestion_rate < 0.75:
                gate.setBrush(QBrush(QColor("#f2b538")))
            else:
                gate.setBrush(QBrush(QColor("#eb4d4b")))
            if self._tick % 8 == 0 and self.stats.congestion_rate > 0.7:
                gate.setPen(QPen(QColor("#ffd6d6"), 2))
            else:
                gate.setPen(QPen(QColor("#284967"), 1))

    def _animate_radar(self) -> None:
        pulse = (self._tick % 24) / 24.0
        alpha = int(60 + 160 * pulse)
        for index, ring in enumerate(self.scan_rings):
            ring.setPen(QPen(QColor(88, 212, 255, max(20, alpha - index * 35)), 1))

    def get_stats(self) -> SimulationStats:
        return self.stats
