from __future__ import annotations

import importlib
import pkgutil
from typing import Dict, List, Protocol

from core.models import ToolSpec, Action


class Skill(Protocol):
    def specs(self) -> List[ToolSpec]:
        ...

    def run(self, action: Action, context: dict) -> dict:
        ...


def load_skills() -> List[Skill]:
    skills_pkg = importlib.import_module("skills")
    out: List[Skill] = []
    for mod_info in pkgutil.iter_modules(skills_pkg.__path__):
        if mod_info.ispkg:
            continue
        mod = importlib.import_module(f"skills.{mod_info.name}")
        if hasattr(mod, "SKILL"):
            out.append(getattr(mod, "SKILL"))
    return out


def build_spec_index(skills: List[Skill]) -> Dict[str, Skill]:
    index: Dict[str, Skill] = {}
    for skill in skills:
        for spec in skill.specs():
            index[spec.type] = skill
    return index
