from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Pending:
    action_type: str
    params: Dict[str, Any]
    missing: str
    question: str


class DialogueState:
    def __init__(self) -> None:
        self._pending: Dict[str, Pending] = {}

    def set_pending(self, session_id: str, pending: Pending) -> None:
        self._pending[session_id] = pending

    def get_pending(self, session_id: str) -> Optional[Pending]:
        return self._pending.get(session_id)

    def clear_pending(self, session_id: str) -> None:
        self._pending.pop(session_id, None)


DIALOGUE = DialogueState()
