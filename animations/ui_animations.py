from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QPoint, QPropertyAnimation
from PyQt6.QtWidgets import QWidget


def slide_in(widget: QWidget, start_offset: int = 40, duration_ms: int = 450) -> QPropertyAnimation:
    animation = QPropertyAnimation(widget, b"pos")
    end_pos = widget.pos()
    start_pos = QPoint(end_pos.x() + start_offset, end_pos.y())
    animation.setStartValue(start_pos)
    animation.setEndValue(end_pos)
    animation.setDuration(duration_ms)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    animation.start()
    return animation
