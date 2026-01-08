from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from core.models import UserQuery, ToolSpec, Action, Plan
from core.planner import plan as plan_request
from core.policy import check
from core.registry import build_spec_index, load_skills

app = FastAPI(title="Jarvis Core (Modular)")

SKILLS = load_skills()
SPEC_INDEX = build_spec_index(SKILLS)
ALL_SPECS: List[ToolSpec] = [spec for skill in SKILLS for spec in skill.specs()]


class QueryResponse(BaseModel):
    ok: bool
    speech: str
    plan: Plan
    results: List[Dict[str, Any]] = Field(default_factory=list)


@app.get("/v1/specs", response_model=List[ToolSpec])
def specs() -> List[ToolSpec]:
    return ALL_SPECS


@app.get("/v1/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


def _run_action(action: Action, session_id: str) -> Dict[str, Any]:
    skill = SPEC_INDEX.get(action.type)
    if not skill:
        return {"speech": f"Nessuna skill per azione '{action.type}'.", "ok": False}
    return skill.run(action, {"session_id": session_id})


@app.post("/v1/query", response_model=QueryResponse)
def query(q: UserQuery) -> QueryResponse:
    plan = plan_request(q.text, ALL_SPECS, q.session_id)
    if plan.needs_clarification:
        return QueryResponse(
            ok=True,
            speech=plan.question or "Mi serve un chiarimento.",
            plan=plan,
            results=[],
        )

    if not plan.actions:
        return QueryResponse(
            ok=False,
            speech="Nessuna azione selezionata.",
            plan=plan,
            results=[],
        )

    results: List[Dict[str, Any]] = []
    speeches: List[str] = []

    for action in plan.actions:
        allowed, reason = check(action)
        if not allowed:
            return QueryResponse(
                ok=False,
                speech=reason or "Azione bloccata dalla policy.",
                plan=plan,
                results=[],
            )
        res = _run_action(action, q.session_id)
        results.append(res)
        if isinstance(res, dict) and "speech" in res:
            speeches.append(str(res["speech"]))

    speech = " ".join(speeches).strip() or "Ok."
    return QueryResponse(ok=True, speech=speech, plan=plan, results=results)
