from __future__ import annotations

from typing import Any, Dict, List, Optional, Literal

from pydantic import BaseModel, Field


class UserQuery(BaseModel):
    text: str
    session_id: str = "default"


class Action(BaseModel):
    type: str
    params: Dict[str, Any] = Field(default_factory=dict)


class Plan(BaseModel):
    actions: List[Action] = Field(default_factory=list)
    needs_clarification: bool = False
    question: Optional[str] = None


class ToolSpec(BaseModel):
    type: str
    description: str
    params_schema: Dict[str, Any]
    risk: Literal["low", "medium", "high"] = "low"
