---
title: "KI-Anbieter — ChatGPT, Claude, lokal"
summary: "Welche KI-Dienste funktionieren mit ForgeIEC und wie Sie diese einrichten"
---

## Welche Anbieter funktionieren?

Der KI-Helfer in ForgeIEC ist **nicht an einen einzigen Anbieter
gebunden**. Sie koennen frei waehlen:

| Variante | Anbieter | Wofuer geeignet |
|---|---|---|
| **Cloud** | ChatGPT (OpenAI) | Schnell, sehr starke Modelle, Daten gehen ins Internet |
| **Cloud** | Claude (Anthropic) | Sehr gut bei langen Aufgaben + Code-Review, Daten gehen ins Internet |
| **Lokal** | LM Studio / llama.cpp / Ollama | Daten bleiben im Haus, kostenlos, langsamer als Cloud |
| **Lokal** | Selbst gehostetes vLLM / Together-API-kompatibel | Wenn Sie Cloud-Modelle hinter Ihrer eigenen Firewall haben |

Der Editor erkennt automatisch ob ein **OpenAI- oder Anthropic-Format**
gesprochen wird — Sie muessen nichts umkonfigurieren.

---

## ChatGPT (OpenAI) anbinden

**Voraussetzung:** ein OpenAI-Account mit aufgeladenem Guthaben. Die
API ist getrennt vom ChatGPT-Web-Abo — Sie zahlen pro Token-Verbrauch,
nicht pauschal.

**Schritt 1 — API-Schluessel erstellen**

1. Im Browser auf `https://platform.openai.com/api-keys` anmelden.
2. `Create new secret key` druecken, einen Namen vergeben (z.B.
   `ForgeIEC-WS-Joerg`).
3. Der Schluessel beginnt mit `sk-...` und wird **nur ein einziges
   Mal** angezeigt — kopieren Sie ihn sofort in einen sicheren Ort
   (Passwort-Manager).

**Schritt 2 — in ForgeIEC Studio eintragen**

Im AI-Reiter, in der Profil-Konfiguration:

| Feld | Wert |
|---|---|
| API | `https://api.openai.com/v1` |
| API Key | `sk-...` (Ihr Schluessel) |
| Model | z.B. `gpt-4o`, `gpt-4o-mini`, `gpt-5` |

**Schritt 3 — Test-Anfrage**

```
Sage mir hallo.
```

Wenn alles passt, antwortet der Helfer. Falls Sie eine HTTP-401 oder
HTTP-429 Meldung im Output sehen: API-Key falsch oder Rate-Limit
ueberschritten.

**Kosten:** Pro Anfrage werden ein paar Cent abgebucht. Eine typische
Programmier-Sitzung kostet 0,10 - 1,00 USD je nach Modell.

---

## Claude (Anthropic) anbinden

**Voraussetzung:** Anthropic-Account mit Console-Zugang. Wie bei
OpenAI ist die API getrennt vom claude.ai-Web-Abo.

**Schritt 1 — API-Schluessel erstellen**

1. Im Browser auf `https://console.anthropic.com/settings/keys`
   anmelden.
2. `Create Key` druecken, Namen vergeben.
3. Schluessel beginnt mit `sk-ant-...` — kopieren in den Passwort-
   Manager.

**Schritt 2 — in ForgeIEC Studio eintragen**

| Feld | Wert |
|---|---|
| API | `https://api.anthropic.com` |
| API Key | `sk-ant-...` |
| Model | z.B. `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001` |

Der Editor erkennt automatisch am Hostnamen `api.anthropic.com` dass
hier das Anthropic-Format gilt — keine extra Einstellung noetig.

**Schritt 3 — Test-Anfrage**

Wie oben — sagen Sie hallo, sehen Sie die Antwort.

**Kosten:** Aehnlich OpenAI; Claude Opus ist etwas teurer aber bei
laengeren Aufgaben oft schneller fertig.

---

## Lokale KI (LM Studio, llama.cpp, Ollama)

**Wann sinnvoll?**

- Daten duerfen nicht ins Internet
- Keine API-Kosten pro Anfrage
- Sie haben eine starke Grafikkarte (mind. 8 GB VRAM fuer kleinere
  Modelle, 24+ GB fuer 30B-Modelle)
- Sie wollen probieren ohne Account einzurichten

**Variante A — LM Studio** (am einfachsten)

1. LM Studio von `https://lmstudio.ai` herunterladen + installieren.
2. Ein Modell im LM-Studio-Browser auswaehlen, z.B.
   `qwen3-coder-30b-a3b-instruct` fuer Coding-Aufgaben.
3. Im Tab `Developer` einen lokalen Server starten — standardmaessig
   auf `http://localhost:1234`.
4. In ForgeIEC Studio:

   | Feld | Wert |
   |---|---|
   | API | `http://localhost:1234/v1` |
   | API Key | (leer lassen oder beliebig) |
   | Model | so wie in LM Studio angezeigt |

**Variante B — llama.cpp-Server**

`llama-server -m model.gguf --port 1234` — gleiche API-URL wie LM
Studio.

**Variante C — Ollama**

1. `ollama serve` starten, Modell laden (`ollama pull qwen2.5-coder`).
2. Adresse: `http://localhost:11434/v1` (OpenAI-kompatibles Endpoint).

**Modell-Empfehlung fuers SPS-Coding (Stand 2026-05):**

- Bei lokalem Betrieb mind. ein **Code-spezialisiertes 30B-Modell**
  (z.B. Qwen-3-Coder-30B-A3B, DeepSeek-Coder-V2-Lite)
- Kleinere Modelle (7B-14B) machen viele Fehler in IEC-ST-Syntax und
  loopen oft

---

## Welcher Provider fuer welche Aufgabe?

| Sie wollen … | Empfehlung |
|---|---|
| Schnelle einfache Hilfe (eine Variable anlegen) | gpt-4o-mini oder Claude-Haiku |
| Komplexes Programmieren (mehrere POUs, Refactor) | Claude-Opus oder gpt-4o |
| Code-Review mit ausfuehrlichem Feedback | Claude-Opus |
| Daten muessen im Haus bleiben | LM Studio + Qwen-Coder-30B |
| Lange Diagnose-Sitzung mit vielen Werten | Claude-Sonnet (1M Context) oder gpt-5 |
| Erste Schritte ohne Geld auszugeben | LM Studio mit kleinem Modell |

---

## Mehrere Anbieter parallel?

Ja. Sie koennen pro Persona einen **eigenen Anbieter** einstellen:

- Blacksmith Master → gpt-4o (schnell, gutes Coding)
- Reviewer → claude-opus-4-7 (gruendlich)
- Monitor → lokales kleines Modell (sicher, kostenlos)

Wechseln Sie im AI-Reiter zwischen den Karteikarten — die Einstellungen
bleiben pro Persona gespeichert.

---

## Sicherheit + Datenschutz

**Cloud-Anbieter:**
- Ihre Anfragen + die ST-Code-Ausschnitte die der Helfer schickt
  laufen ueber das Internet zum jeweiligen Anbieter.
- Wenn das fuer Ihr Projekt nicht akzeptabel ist → lokale KI.
- API-Schluessel niemals an Kollegen weiterreichen oder in Git
  einchecken.

**Lokale KI:**
- Daten verlassen Ihren Rechner nicht.
- Auch der API-Key ist optional / egal (kein echter Server pruefen
  ihn).

**In allen Faellen:**
- ForgeIEC Studio selbst speichert keine Anfragen oder Antworten in
  der Cloud.
- Chat-Historie wird lokal in
  `~/.config/ForgeIEC/Chats/<persona>.jsonl` gespeichert.
- Das Audit-Log unter `~/.config/ForgeIEC/mcp_audit.log` protokolliert
  jede schreibende Aktion mit Zeitstempel — unabhaengig vom Anbieter.

---

## Weiter

- [Personas](/help/ai/agents/) — Charaktere
- [Bedienung im Alltag](/help/ai/chat/) — Eingabe + Notbremse
- [Sicherheits-Modell](/help/ai/security/)
- [Zurueck zur AI-Uebersicht](/help/ai/)
