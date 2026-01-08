from __future__ import annotations

import re
from typing import List, Optional

from core.dialogue import DIALOGUE, Pending
from core.models import Action, Plan, ToolSpec

# Planner v1: modulare, basato su intent + sinonimi + chiarimenti.
# In futuro si puo' sostituire con tool-calling senza cambiare le skill.

VERB_OPEN = {"apri", "lancia", "avvia", "start"}
VERB_STATUS = {"stato", "status", "come va", "come sta"}
VERB_SHUTDOWN = {"spegni", "arresta", "shutdown"}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _extract_app(text: str) -> Optional[str]:
    t = _norm(text)
    match = re.search(r"\b(apri|lancia|avvia|start)\b\s+(?P<app>[a-z0-9._-]+)", t)
    return match.group("app") if match else None


def _mentions_pc(text: str) -> bool:
    t = _norm(text)
    return any(x in t for x in ["pc", "computer", "fisso", "windows"])


def plan(text: str, tool_specs: List[ToolSpec], session_id: str) -> Plan:
    t = _norm(text)

    pending = DIALOGUE.get_pending(session_id)
    if pending:
        if pending.missing == "confirm":
            confirm = any(x in t for x in ["confermo", "si", "ok"])
            if not confirm:
                DIALOGUE.clear_pending(session_id)
                return Plan(needs_clarification=True, question="Ok, annullato. Dimmi cosa vuoi fare.")
            params = dict(pending.params)
            params[pending.missing] = True
            DIALOGUE.clear_pending(session_id)
            return Plan(actions=[Action(type=pending.action_type, params=params)])

        params = dict(pending.params)
        params[pending.missing] = t
        DIALOGUE.clear_pending(session_id)
        return Plan(actions=[Action(type=pending.action_type, params=params)])

    if t in {"help", "aiuto"} or "cosa sai fare" in t:
        return Plan(actions=[Action(type="system.help", params={})])

    if any(v in t for v in VERB_STATUS):
        target = "pc" if _mentions_pc(t) else "system"
        return Plan(actions=[Action(type="system.status", params={"target": target})])

    if any(v in t for v in VERB_OPEN):
        app = _extract_app(t)
        if app:
            if not _mentions_pc(t):
                question = "Vuoi che lo faccia sul PC Windows fisso? (si/no)"
                DIALOGUE.set_pending(
                    session_id,
                    Pending(
                        action_type="pc.open_app",
                        params={"app": app},
                        missing="confirm",
                        question=question,
                    ),
                )
                return Plan(needs_clarification=True, question=question)
            return Plan(actions=[Action(type="pc.open_app", params={"app": app})])

    if any(v in t for v in VERB_SHUTDOWN) and _mentions_pc(t):
        question = "Azione critica: vuoi spegnere davvero il PC? (di: CONFERMO)"
        DIALOGUE.set_pending(
            session_id,
            Pending(
                action_type="pc.shutdown",
                params={},
                missing="confirm",
                question=question,
            ),
        )
        return Plan(needs_clarification=True, question=question)

    return Plan(needs_clarification=True, question="Non ho capito. Puoi riformulare?")
