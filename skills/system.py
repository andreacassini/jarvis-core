from __future__ import annotations

from core.models import ToolSpec, Action


class SystemSkill:
    def specs(self):
        return [
            ToolSpec(
                type="system.help",
                description="Elenca capacita' e comandi disponibili.",
                params_schema={"type": "object", "properties": {}},
                risk="low",
            ),
            ToolSpec(
                type="system.status",
                description="Stato del sistema o di un target (pc/system).",
                params_schema={
                    "type": "object",
                    "properties": {"target": {"type": "string"}},
                },
                risk="low",
            ),
        ]

    def run(self, action: Action, context: dict) -> dict:
        if action.type == "system.help":
            return {
                "speech": (
                    "Sono Jarvis Core. Posso orchestrare skill modulari. "
                    "Esempi: 'apri chrome', 'stato', 'spegni pc'. "
                    "Quando e' ambiguo, faccio domande."
                )
            }
        if action.type == "system.status":
            target = action.params.get("target", "system")
            return {"speech": f"Tutto ok. Target richiesto: {target}."}
        return {"speech": "Azione system non gestita."}


SKILL = SystemSkill()
