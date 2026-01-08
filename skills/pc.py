from __future__ import annotations

from connectors import windows_agent
from core.models import ToolSpec, Action


class PcSkill:
    def specs(self):
        return [
            ToolSpec(
                type="pc.open_app",
                description="Apri un'applicazione sul PC Windows fisso.",
                params_schema={
                    "type": "object",
                    "properties": {"app": {"type": "string"}},
                    "required": ["app"],
                },
                risk="medium",
            ),
            ToolSpec(
                type="pc.shutdown",
                description="Spegne il PC Windows fisso (richiede conferma).",
                params_schema={
                    "type": "object",
                    "properties": {"confirm": {"type": "boolean"}},
                    "required": ["confirm"],
                },
                risk="high",
            ),
        ]

    def run(self, action: Action, context: dict) -> dict:
        res = windows_agent.execute(action)
        if action.type == "pc.open_app":
            app = action.params.get("app", "")
            return {
                "speech": f"Ok. Richiesta apertura '{app}' inviata al PC.",
                "details": res,
            }
        if action.type == "pc.shutdown":
            return {
                "speech": "Ok. Richiesta di spegnimento inviata al PC.",
                "details": res,
            }
        return {"speech": "Azione PC non gestita."}


SKILL = PcSkill()
