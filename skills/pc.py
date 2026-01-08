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

    executed = res.get("executed", False)
    note = (res.get("note") or "").lower()

    # ❌ FALLIMENTO
    if not executed:
        if "non configurato" in note or "not configured" in note:
            return {
                "speech": (
                    "Non posso eseguire questa azione perché l'agente Windows "
                    "non è configurato o il PC non è raggiungibile. "
                    "Quando vuoi, posso aiutarti a configurarlo."
                ),
                "details": res,
            }

        if "timeout" in note or "unreachable" in note:
            return {
                "speech": (
                    "Ho provato a contattare il PC, ma al momento non risponde. "
                    "Potrebbe essere spento o fuori rete."
                ),
                "details": res,
            }

        return {
            "speech": (
                "Ho capito cosa vuoi fare, ma non sono riuscito a eseguire "
                "l'azione per un problema tecnico."
            ),
            "details": res,
        }

    # ✅ SUCCESSO REALE
    if action.type == "pc.open_app":
        app = action.params.get("app", "")
        return {
            "speech": f"Ho aperto {app} sul PC fisso.",
            "details": res,
        }

    if action.type == "pc.shutdown":
        return {
            "speech": "Il PC fisso si sta spegnendo ora.",
            "details": res,
        }

    return {"speech": "Azione PC non gestita.", "details": res}


SKILL = PcSkill()
