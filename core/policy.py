from __future__ import annotations

from core.models import Action


def check(action: Action) -> tuple[bool, str]:
    if action.type == "pc.shutdown":
        if action.params.get("confirm") is not True:
            return False, "Mi serve una conferma esplicita (CONFERMO)."
    return True, ""
