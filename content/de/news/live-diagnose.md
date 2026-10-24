---
title: "Live-Diagnose: Monitor + Oszilloskop für IEC 61131-3"
date: 2026-05-10
summary: "Variablen-Live-Werte, FB-Member-Auflösung, Oszilloskop mit Trigger, CSV-Aufnahme, gemessener Jitter — Inbetriebnahme-Werkzeuge auf Industrie-Niveau"
components: [studio, anvild]
---

{{< components "studio,anvild" >}}

## Worum es geht

Bei einer Inbetriebnahme verbringen Sie 90 % der Zeit mit
**Beobachten**: Welche Variable hat welchen Wert, wann schaltet
welcher Timer, warum bleibt der Motor stehen? ForgeIEC Studio hat
dafür einen kompletten Diagnose-Stack — Live-Werte am Variablen-
Tab, ein Oszilloskop mit Trigger für Zeitreihen, und ehrliche
Aussagen über das Sampling-Limit.

---

## Live-Werte überall im Editor

- **Variablen-Tab** zeigt Live-Werte pro Pool-Variable, geteilt
  zwischen UI + KI-Helfer (gleiche Datenquelle).
- **POU-Locals** im Live-Snapshot — auch verschachtelte FB-
  Outputs wie `kr_main.StepTimer.Q` werden aufgelöst und sichtbar
  gemacht.
- **Force-Status** pro Variable zeigt `forced=true/false` im
  Snapshot — auch über `monitor.snapshot` MCP-Tool abrufbar.
- **Detach beim Projekt-Wechsel**: kein „Geister-Watch" mehr — der
  `FLiveValueStore` räumt sauber auf wenn Sie ein Projekt
  schließen oder ein anderes öffnen.

Hintergrund: Live-Werte gehen über gRPC vom anvild-Daemon zum
Studio; bei der Migration weg von einem alten Zenoh/Spark-Setup
ist die ganze Pipeline robuster + schneller geworden.

---

## Oszilloskop mit Trigger

Klassische SPS-Diagnose-Frage: „Warum schaltet `Motor_Bereit` nicht,
obwohl alle Bedingungen erfüllt sein müssten?"

Antwort: Oszilloskop-Aufnahme — Pre-Trigger-Fenster + Trigger auf
Flanke / Schwellwert / Vergleich:

```
oscilloscope.capture {
  channels: ["MX0.0 LED_00", "%MD200 Druck_1"]
  duration_ms: 5000
  pre_trigger_ms: 1000
  trigger: { pool_address: "%MX0.0", condition: "rising", threshold: 0.5 }
}
```

Liefert eine Zeitreihe mit relativen `t_us`-Werten und Statistiken
pro Kanal (mean, min, max, p95, p99). CSV-Export über
`oscilloscope.export_csv` — für Excel + Loganalyse + Reports.

Plus: **Streaming-Modus** mit `oscilloscope.start_streaming` +
`stop_streaming` für lange Sessions, die nicht in einem einzelnen
Capture passen.

---

## Aufnahme-Workflow

`monitor.start_recording` startet eine Watch-Aufnahme im
Hintergrund — alle überwachten Variablen werden mitprotokolliert.
`stop_recording` schließt die CSV-Datei ab. Praktisch für
„24h-Lauf am Wochenende" oder „neue Anlage 4 Stunden beobachten
und dann auswerten".

---

## Cycle-Stats + ehrliche Mess-Limits

`monitor.cycle_stats` liefert Task-Cycle-Statistiken — min, max,
Durchschnitt, Jitter. Plus eine **Jitter-Baseline-Spec** im
Repository unter `tests/data/runtime/jitter_baseline.json`,
gemessen mit einem dedizierten Test-Skript
(`test/qa/measure_jitter.py`).

Sampling-Untergrenze ist die **kürzeste Task-Cycle-Zeit** —
ForgeIEC kommuniziert das explizit in der `monitor.read_value`-
Antwort und im KI-Init-String:

> „Die kleinste Task-Cycle-Zeit ist die Sampling-Untergrenze.
> Erwartete Pulsdauer = TimerKonstante + 1 Task-Cycle (Schalt-
> verzögerung über TON-Reset-Pattern)."

Kein „infinite resolution"-Marketing-Nebel, sondern ehrliche
Physik.

---

## FB-Member-Auflösung — auch verschachtelt

Bisher in vielen IDEs nicht selbstverständlich: dass ein
`MyTimer.Q` oder `kr_main.StepTimer.Q` im Live-Snapshot sichtbar
ist, ohne dass Sie pro FB-Instanz manuell eine Watch anlegen
müssen. ForgeIEC Studio:

- Auf der Bridge-Seite (anvild) emittiert der Codegen automatisch
  FB-Member-Outputs in den Monitor-Stream.
- Editor-seitig zeigt `monitor.snapshot` und der Variables-Tab den
  vollen Pfad aufgelöst an.
- Bezeichner sind tree-sitter-getypt, also auch in
  Live-Monitor-Filtern und Oszi-Channel-Selectoren autocompletable.

---

## Was die Commits getragen haben

- `b94251a`, `a41f12b` — FB-Member-Outputs im Live-Snapshot
- `7fd5476` — setWatchInterval-Loss-Fix + Scope-gRPC-Migration
- `9b3db68`, `5a777e7` — Jitter-Baseline-Tool + quantitatives
  Mess-Skript
- `db4d84c` — `oscilloscope.*` (5 Tools)
- `b221ebf` — `monitor.start_recording` + `stop_recording`
- `193bf3d` — `FLiveValueStore` lifecycle: clearAllWatches +
  Detach bei Pool-Switch
- `3c61445` — `tasks.cycle_overview` + `bellows.protocol_status`
- `f7546bc` — Multi-Source-Watches + FB-Outputs-Helper

---

## Wo Sie das nutzen

| Frage | Werkzeug |
|---|---|
| „Steht ein Schalter auf TRUE?" | Variables-Tab Live-Spalte |
| „Welche Werte hatte LED_04 in den letzten 5 Sek?" | `oscilloscope.capture` |
| „Wann genau schaltet `Motor_Bereit`?" | Oszi mit rising-edge-Trigger |
| „Wie lange läuft der Task im Worst-Case?" | `monitor.cycle_stats` |
| „Was hat sich im Wochenend-Lauf verändert?" | `start_recording` + CSV-Auswertung |

---

## Wo es konkret nachzulesen ist

- [Was die KI kann](/help/ai/tools/) — Live-Beobachtung-Sektion
- [MCP für Applikationsingenieure](/help/mcp/programmers/) — SSE-
  Stream-Doku
