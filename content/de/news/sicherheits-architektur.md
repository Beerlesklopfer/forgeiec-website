---
title: "Sicherheits-Architektur: Force dreifach gesperrt"
date: 2026-05-08
summary: "Force-Gate per Variable, Confirmation State Machine, Build-time-Gating — wie ForgeIEC verhindert dass eine KI oder ein Fehlklick reale Hardware bewegt"
components: [studio, anvild]
---

{{< components "studio,anvild" >}}

## Worum es geht

In der Automatisierung ist der gefährlichste Befehl der **Force**:
ein Output-Pin manuell auf TRUE pinnen, unabhängig vom Programm.
Das bewegt am Ausgang **echte Hardware** — einen Motor, ein
Ventil, eine Sicherheitsfunktion.

ForgeIEC behandelt Force-Setzungen entsprechend: **per-Variable
gegated und dreifach gesperrt** — beim Codegen, in der Runtime und im
Editor, in unabhängigen Subsystemen; für die KI kommt eine vierte
Sperre im MCP-Server hinzu. Eine KI kann **nicht** forcen. Ein
Fehlklick im UI braucht zwei separate Confirms. Und ein
Production-Build der Runtime hat die Force-Bridge gar nicht
mitcompiliert.

---

## Layer 1 — Codegen-TOML

Schon beim Kompilieren der PLC-Binary entscheidet der Editor pro
Variable ob `force_enabled` in den `bellows_descriptor.toml`
geschrieben wird. Variablen ohne Flag landen **nicht** in der
Force-Bridge:

- Im Variables-Tab gibt es eine `F`-Checkbox pro Variable
- Default: AUS (force nicht erlaubt)
- Anschalten ist eine Modell-Änderung, die das Projekt dirty
  macht → muss gespeichert + neu deployed werden

Damit ist die Force-Berechtigung am **Quellcode** verankert.
Operator + Audit können genau sehen welche Variablen
forcierbar sind.

---

## Layer 2 — anvild RPC

Die anvild-Runtime prüft beim `ForceVariable`-gRPC-Endpoint den
Build-Mode der laufenden PLC-Binary. Wenn die Binary **nicht**
mit Force-Bridge gebaut wurde, lehnt anvild Force-Anfragen ab —
unabhängig davon was das UI sagt.

Production-Builds der Runtime werden ohne `-DFORCING_ENABLED`
ausgeliefert. Selbst wenn ein Angreifer Studio kompromittiert,
kann er auf der echten SPS keine Force-Setzung durchsetzen weil
der Code-Pfad nicht existiert.

---

## Layer 3 — Editor-UI

Die F-Checkbox wird **automatisch greyout** wenn die PLC-Binary
kein Force unterstützt. Plus: die Build-Mode-Information läuft
durch `anvild::server_info` zum Editor — `editor_build.
force_available` ist `true|false`.

Operator sieht im UI sofort: hier läuft eine sichere
Production-Binary, Force ist nicht möglich. Kein
„Klick-und-hoffen"-Trial-and-Error.

---

## Layer 4 — MCP

Für die **KI-Schicht** gibt es eine vierte Schicht obendrauf:
es gibt **kein** `force.*`-MCP-Tool, weder im Default-Build noch
im Override-Build. Eine KI kann den `forced=true|false`-Status
**lesen** (per `monitor.snapshot`), aber **nicht setzen**.

Begründung in der Spec (mcp-platform-v1 §7.4): „Ein KI-Agent
darf solche Side-Effects nicht selbsttätig auslösen — selbst
wenn er glaubt es wäre richtig."

---

## Plus: Confirmation State Machine für alle Änderungen

Force ist nur die strengste Variante. Generell läuft **jede
schreibende Aktion** der KI durch eine State Machine:

1. Tool-Aufruf liefert `FORGE_ERR_CONFIRMATION_REQUIRED` zurück
2. Operator sieht im Chat: was passieren soll + Kontext
3. Bestätigung via `editor.confirm` setzt den Tool-Lauf fort
4. Audit-Log mit Zeitstempel, Tool, Args, Choice

```
Confirmation required:
  Tool: project.write.add_variable
  Question: Add bellows.Bellows.LED_00 (iec_type=BOOL)?
  Options: yes / cancel
```

Auch in den Geschwindigkeits-Modus (auto-confirm) muss bewusst
eingeschaltet werden — mit einer extra Sicherheits-Warnung. In
Produktion: aus lassen. Plus Notbremse als roter Not-Aus-Pilzkopf-
Taster nach DIN EN ISO 13850.

---

## Was die Commits getragen haben

- `9cc6dcd` — per-Variable Force-Gate, 3-Layer-Defense komplett
- `dbfd62a` — Confirmation State Machine (FConfirmationStateMachine)
  + projekt.* lifecycle + Audit-Log
- `4ce57bf` — codegen.deploy-Gate erfordert
  `MCP_OVERRIDE_SECURITIES`, kein Runtime-Switch
- `f43c9d7` — industrial E-Stop + Danger-Mode-Settings mit
  expliziter Warnung
- `0699954` — Danger-Mode-auto-confirm + per-settings tool-loop-
  limit
- `b489428` — anvild-Build-Info-Propagation via `server_info` ⇒
  Editor-seitige Force-greyout-Logik

Plus Architektur-Spec: `documentation/architecture/mcp-platform-v1.md`
§9 (Sicherheits-Modell) + tongs-platform-v1 §5 (Fault-Model für
Bus-Bridges).

---

## Wo Sie das nutzen

| Sie wollen | Konfiguration |
|---|---|
| Produktiv-SPS, KI nur lesend | Standard-APT-Install, kein Override-Flag |
| Entwicklung mit Force-Test | Force-Variablen einzeln F-checken, Dev-Build der Runtime |
| Tausch-Werkstatt: Cert-Lifecycle automatisierbar | Danger-Mode pro Persona — siehe [Bedienung](/help/ai/chat/) |
| Test-Loop ohne UI-Klick für 50 Variablen | Danger-Mode + erhöhtes Tool-Turn-Limit |
| Lehrling einlernen | Trainee-Persona, immer alle Confirms |

---

## Wo es konkret nachzulesen ist

- [Sicherheits-Modell (Anwender)](/help/ai/security/)
- [Architektur + Sicherheit (Auditor)](/help/ai/architecture/)
- [Personas — wer darf was](/help/ai/agents/)
