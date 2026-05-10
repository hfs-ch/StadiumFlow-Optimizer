from __future__ import annotations

import sys

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
)

from controllers.app_controller import AppController


class SplashScreen(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background:#070b14;color:#d8f5ff;border:1px solid #244369;")
        self.setFixedSize(520, 260)
        layout = QVBoxLayout(self)
        title = QLabel("SONARGES SmartFlow Optimizer")
        title.setStyleSheet("font-size:24px;font-weight:700;color:#59d8ff;")
        subtitle = QLabel("FIFA 2030 Control Center")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(self.progress)
        self._value = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(18)

        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setStartValue(0.1)
        self.anim.setEndValue(1.0)
        self.anim.setDuration(900)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

    def _tick(self) -> None:
        self._value += 1
        self.progress.setValue(self._value)
        if self._value >= 100:
            self.timer.stop()
            self.accept()


class LoginScreen(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SONARGES Login")
        self.setStyleSheet("background:#090f1d;color:#d8f5ff;")
        self.setFixedSize(400, 250)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Connexion Centre de Controle"))
        form = QFormLayout()
        self.username = QLineEdit()
        self.username.setPlaceholderText("Operateur SONARGES")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Mot de passe")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Utilisateur", self.username)
        form.addRow("Mot de passe", self.password)
        layout.addLayout(form)
        self.login_btn = QPushButton("Acceder au systeme")
        self.login_btn.clicked.connect(self._try_login)
        layout.addWidget(self.login_btn)
        self.status = QLabel("")
        layout.addWidget(self.status)

    def _try_login(self) -> None:
        if self.username.text().strip() and self.password.text().strip():
            self.accept()
        else:
            self.status.setText("Veuillez renseigner les champs.")


def main() -> int:
    app = QApplication(sys.argv)

    splash = SplashScreen()
    if splash.exec() != QDialog.DialogCode.Accepted:
        return 0

    login = LoginScreen()
    if login.exec() != QDialog.DialogCode.Accepted:
        return 0

    controller = AppController()
    controller.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
