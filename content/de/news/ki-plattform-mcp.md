---
title: "Der KI-Helfer im Editor: vom Chat zur Plattform"
date: 2026-05-12
summary: "Eingebauter AI-Assistent mit ~80 Werkzeugen, Multi-Persona-Workflow und offenem Anschluss fuer Claude Desktop, VS Code, ChatGPT"
components: [studio, anvild]
---

{{< components "studio,anvild" >}}

## Warum das wichtig ist

KI-Code-Assistenz ist im Software-Bereich angekommen — in der
Industrieautomatisierung bisher nicht. Der Grund: SPS-Code wirkt
auf reale Hardware, jede falsche Variable bewegt einen Motor oder
oeffnet ein Ventil. Cloud-LLMs als „Code-completion auf SPS"
funktioniert ohne strenge Sicherheits-Schicht nicht.

ForgeIEC Studio loest das mit **MCP (Model Context Protocol)** als
Schnittstelle zwischen LLM und Editor. Das LLM ruft typisierte
Werkzeuge — keine freien Shell-Befehle — und jeder Schritt der
Aenderungen verursacht laeuft durch eine Operator-Bestaetigung.

Damit ist ForgeIEC der erste IEC-61131-3-Editor mit einer
**ernsthaft tragfaehigen** KI-Integration.

---

## Was die KI praktisch tut

Sechs Tool-Familien decken die Editor-Bedienung ab:

| Familie | Was die KI sieht / tut |
|---|---|
| `project.*` | POU-Inventur lesen, Variablen anlegen, POU-Body schreiben, Bus-Topologie inspizieren |
| `codegen.*` | Kompilieren, generieren, deployen, Status-Pollen mit g++-stderr-Tail |
| `monitor.*` | Live-Snapshot + Einzel-Werte + Cycle-Stats + Code-State |
| `oscilloscope.*` | Zeitreihen-Aufnahme mit Trigger, Stream-API, CSV-Export |
| `tasks.*` | Resource/Task/Programm-Instance lesen + schreiben |
| `library.*` | Standard-FB-Bausteine (TON, CTU, R_TRIG, ...) lookup mit ST-Beispielen |
| `bellows.*`, `anvil.*` | HMI-Gateway + Anvil-Topics inspizieren |
| `editor.*` | Sauberer Quit, Logs, Confirm-Antworten |
| `forge.help` | Selbst-Doku — die KI fragt sich selber aus |

Gesamt ueber **80 Tools**, alle JSON-Schema-getypt und durch
`forge.help_for(name)` mit Beispielen + Fehlerklassen
selbstbeschreibend.

---

## Fuenf Personas, ein Chat-Reiter

Statt einer einzigen statischen Sitzung gibt es **rollenbasierte
Personas** im AI-Reiter:

- **Blacksmith Master** — der Vorarbeiter, darf alles
- **Reviewer** — read-only, kann nichts kaputt machen
- **Doc** — schreibt Variablen-Kommentare + Doku
- **Monitor** — beobachtet Live-Anlagen, nichts veraendert
- **Trainee** — wie Vorarbeiter, aber jede Aktion einzeln
  bestaetigt — ideal fuer Einarbeitung

Jede Persona hat **eigenen API-Endpoint + Modell** — so kann
GPT-4o den Code schreiben und Claude-Opus dazu den Review machen.

Mehr: [Personas im Einzelnen](/help/ai/agents/).

---

## Offen — kein Vendor-Lock-in

Der Editor implementiert die **Server-Seite** von MCP. Jeder
MCP-konforme Client kann sich verbinden — der eingebaute Chat-
Reiter ist nur einer davon:

- **Claude Desktop** (Mac, Windows, Linux)
- **VS Code** mit MCP-Extension
- **Claude Code (CLI)**
- **ChatGPT** mit MCP-Connector
- **mcp-inspector** als Debug-Tool
- **Eigene Skripte** per `curl` + JSON-RPC

Sie tragen URL + Bearer-Token aus ForgeIEC Studio in den jeweiligen
Client ein — fertig. Anbindung an
[ChatGPT / Claude / lokal](/help/ai/providers/) ist dokumentiert.

---

## Sicherheit: Drei Schichten, sichtbar

Die KI ist secure-by-default. Drei aufeinander aufbauende
Schichten muessen passiert werden:

1. **Build-time Gate** — die Standard-Distribution aus dem APT-Repo
   ist read-only. Schreibende Aktionen erfordern einen separat
   gebauten Editor. Das ist eine echte Trennung, kein Hakchen.
2. **Confirmation State Machine** — jede schreibende Aktion
   liefert `FORGE_ERR_CONFIRMATION_REQUIRED` zurueck, der Operator
   bestaetigt per `editor.confirm`. Keine stille Hintergrund-
   Aenderung.
3. **Operator-Sichtbarkeit** — jede Aktion im Chat-Verlauf
   sichtbar, Audit-Log mit Zeitstempel.

Force-Setzungen (Hardware-Output pinnen) sind **explizit nicht**
ueber MCP zugaenglich — das bleibt Operator-Hoheit ueber die GUI.

Mehr: [Sicherheits-Modell](/help/ai/security/) und
[Architektur-Tiefe](/help/ai/architecture/).

---

## Anti-Loop-Hilfen — weil LLMs nicht perfekt sind

LLMs verirren sich in Endlos-Schleifen wenn sie einen Fehler nicht
verstehen. ForgeIEC Studio adressiert das mit **actionable
Error-Messages**: jeder Compile-Fehler liefert nicht nur „Expected
:= or ("-Mathematik, sondern den konkreten MCP-Call zum Beheben.
Beispiel:

> „X is a Function Block — declare instance first.
> Action: project.write.add_variable scope_kind=pou iecType=TON"

Plus konfigurierbare **Tool-Schritte-Grenze** (default 10 Schritte
pro User-Anfrage) und ein Geschwindigkeits-Modus mit
**Notbremse-Knopf** (roter Industrie-Pilz-Taster) wenn die KI
trotzdem aus dem Ruder laeuft.

---

## Was die Commits getragen haben

Die KI-Plattform ist nicht ein Big-Bang, sondern eine Reihe von
Sprints die aufeinander aufbauen:

- **MCP-1**: Prompts in QSettings + editierbarer System-Prompt
- **MCP-2**: Confirmation State Machine + project lifecycle
- **MCP-3a..i**: Tool-Familien gestaffelt — JSON-RPC, library,
  tasks, bellows, anvil, monitor, oscilloscope, catalog, codegen
- **MCP-3.5**: Multi-Agent-Dock — 5 Default-Personas
- **MCP-3.6**: Chat-Tab als interner MCP-Client (statt externem
  Tool)
- **MCP-4a**: Remote-Bind + HTTPS + Bearer-Auth pro Profil
- **MCP-4b**: Federation + Trust (siehe
  [eigener Post](/news/federation-team-trust/))
- **MCP-6**: project.write.* Phase-2 + runtime.* + state-machine-
  Integration
- **MCP-8**: Namespace-aware writes (pou/gvl/bellows/anvil-Triplet)
- **MCP-9**: Persistence + diagnostics + triplet convention

Source: `documentation/architecture/mcp-platform-v1.md` (~2300 LOC
formale Spec, RFC-2119-Sprache).

---

## Wo Sie das nutzen

| Setup | Wofuer |
|---|---|
| **Lokales Coding** | Cloud-LLM oder lokales Modell, Personas im AI-Reiter |
| **Code-Review** | Reviewer-Persona, read-only — keine Gefahr |
| **Inbetriebnahme** | Monitor-Persona auf Produktions-SPS — nur Beobachtung |
| **Einarbeitung** | Trainee-Persona, jede Aktion einzeln bestaetigen |
| **CI-Build-Server** | Headless-Studio + curl + JSON-RPC aus dem Build-Skript |
| **Multi-LLM-Cooperation** | GPT als Kritiker, Claude als Coder, jeder mit eigener Persona |

---

## Wo es konkret nachzulesen ist

- [KI-Helfer-Anwender-Doku](/help/ai/)
- [Personas](/help/ai/agents/), [Bedienung](/help/ai/chat/),
  [Was die KI kann](/help/ai/tools/)
- [Providers — ChatGPT, Claude, lokal](/help/ai/providers/)
- [MCP fuer Applikationsingenieure](/help/mcp/programmers/)
- [MCP fuer IT + Betrieb](/help/mcp/it/)
