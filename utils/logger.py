from __future__ import annotations

from datetime import datetime
from typing import List


class AppLogger:
    def __init__(self) -> None:
        self._messages: List[str] = []

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._messages.append(f"[{timestamp}] {message}")

    def dump(self) -> str:
        return "\n".join(self._messages)

    def list_messages(self) -> List[str]:
        return self._messages.copy()
