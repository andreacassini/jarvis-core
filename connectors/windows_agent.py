from __future__ import annotations

from core.models import Action


def execute(action: Action) -> dict:
    return {
        "executed": False,
        "note": "Windows Agent non configurato (simulazione).",
        "action": action.model_dump(),
    }
