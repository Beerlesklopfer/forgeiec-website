---
title: "Was die KI kann"
summary: "Welche Aktionen kann der KI-Helfer in ForgeIEC Studio ausführen — Übersicht in Klartext"
---

## Lesen und Verstehen — immer erlaubt

Diese Aktionen kann der Helfer **immer** ausführen, ohne dass Sie was
einschalten müssen:

- **Projekt-Übersicht** — Name, Anzahl POUs, Anzahl Variablen
- **POUs auflisten** — alle Programme + Function Blocks + Functions
- **POU lesen** — den ST-Code einer einzelnen POU ansehen
- **Variablen auflisten** — alle Pool-Variablen mit Adressen + Typen,
  gefiltert nach Bereich (Globale, POU-Locals, Bellows-Export, …)
- **Bus-Konfiguration** — Segmente, Devices, Variablen-Mapping
- **Aliase** — alle definierten Variablen-Namen + Adressen
- **Bibliothek** — alle Standard-FB-Bausteine (TON, CTU, R_TRIG, …)
  mit Parametern und ST-Beispielen

Damit kann der Helfer Ihre Codebasis **selber kennenlernen**, bevor
er Vorschläge macht.

---

## Live-Beobachtung — immer erlaubt

Wenn die SPS läuft, kann der Helfer die laufenden Werte abfragen:

- **Live-Snapshot** — alle überwachten Variablen auf einmal lesen
- **Einzelwert** — eine bestimmte Adresse abfragen
- **SPS-Status** — läuft sie, wie viel Watch-Verkehr, letzter Upload
- **Cycle-Statistiken** — Task-Zeit, Jitter, min/max/Durchschnitt
- **SPS-Code-Status** — Run / Pause / Stopp
- **Aufzeichnung starten/stoppen** — Live-Werte für spätere Analyse
- **Oszilloskop-Aufnahme** — Zeitreihe einer oder mehrerer Adressen,
  mit optionalem Trigger (Flanke, Schwellwert)

Damit kann der Helfer eine **Diagnose** machen: „Warum schaltet
`Motor_Bereit` nicht? Schau dir die letzten 5 Sekunden auf
dem Oszi an."

---

## Änderungen — nur in der freigeschalteten Version

Folgende Aktionen ändern Ihr Projekt oder die SPS. Sie sind in der
**Standard-Version aus dem Internet abgeschaltet** und brauchen eine
spezielle Version mit `MCP_OVERRIDE_SECURITIES=ON`. Jede Aktion
gibt vorher eine Rückfrage:

### Projekt-Änderungen

- **Variable anlegen** — neue Pool-Variable mit Adresse + Typ
- **Variable verschieben** zwischen Pou-lokal, Globale, Bellows-Export
- **Variable löschen** — bitte vorsichtig
- **POU anlegen** — neues Programm, Function Block oder Function
- **POU umbenennen** — AST-basiert via tree-sitter-st (Identifier-
  Sichten + Comment-Mentions; ohne Code-Body-Regex)
- **POU löschen** — vorsichtig, Task-Bindings können
  dangling werden
- **POU-Body setzen** — den ST-Code austauschen
- **Flag setzen** — Bellows-Export, Retain, Constant, Monitor-Enable

### Refaktorisieren (REF-1)

Tree-sitter-basierte Rename- und Find-References-Aktionen, immer mit
Preview + Apply-Workflow:

- **`refactor.find_references`** — alle Vorkommen einer Variable /
  POU / Anvil-Gruppe / Bellows-Gruppe + GVL-Namespace im Projekt
  finden
- **`refactor.preview`** — gezielten Rename oder Move vorbereiten;
  Antwort enthält eine `tx_id` + Liste der geplanten Änderungen mit
  Before/After + Confidence (exact / ambiguous)
- **`refactor.apply`** — Transaction ausführen, optional mit
  abgewählten Einzel-Änderungen (jede Zeile in der Preview hat
  eine eigene Checkbox im Output-Panel)
- **`refactor.cancel`** — geöffnete Transaction verwerfen
- **`refactor.list_transactions`** — offene Transactions sehen

### Kompilieren + Deployen

- **Pre-Compile-Check** (`codegen.lint`) — schnelle Syntax-Prüfung
  über alle ST-POUs. Liefert FStCompiler-Errors PLUS tree-sitter-
  `parse_diagnostics[]` (ERROR/MISSING-Nodes mit byte-Range für
  Editor-Highlight)
- **Vollständiger Compile** — wie der Build-Knopf in der Toolbar;
  läuft seit 2026-05 über den C++-Codegen-Pfad (FCxxProjectEmitter).
  Der alte matiec-/C-Pfad ist deprecated.
- **Code generieren** (`codegen.generate`) — die emittierten C++-
  Files (`Gen<POU>.h/.cpp` + `AnvilGen.h` + `BellowsGen.h` +
  `GvlGen.h` + `runtime_main.cpp` + `CMakeLists.txt`) anschauen
  ohne Deploy. Default-Target `cxx`; Aufruf mit `target='c'`
  liefert `FORGE_ERR_DEPRECATED`.
- **Deploy** — Files auf die SPS hochladen, dort via `cmake -B
  build && cmake --build build` bauen und das neue Binary starten
- **Deploy-Status** — Phasen + Build-Output beim letzten Deploy

### SPS-Steuerung

- **Start** — SPS-Run-Befehl
- **Stop** — SPS-Stop-Befehl, Ausgänge gehen in Safe-State
- **Pause / Resume** — Cycle anhalten ohne komplettes Stop
- **Force** — eine Variable festsetzen (NUR über die GUI möglich,
  **nicht** über die KI; siehe [Sicherheits-Modell](/help/ai/security/))

---

## Aufgaben + Task-Management

Der Helfer kann auch das Task-Setup verändern:

- **Ressourcen auflisten** + **Task auflisten** in einer Ressource
- **Programm-Instanzen** einer Task lesen
- **Neue Task anlegen** mit Cycle-Time + Priorität
- **Programm-Instanz auf Task legen**
- **Cycle-Übersicht** über alle Tasks

---

## Helfer fragt sich selbst aus

Wenn die KI nicht weiß was ein bestimmtes Werkzeug tut, kann sie
**ihre eigene Hilfe** abfragen:

- `forge.help` — Cheat-Sheet aller verfügbaren Aktionen mit kurzen
  Beschreibungen, gruppiert nach Familie
- `forge.help_for(name)` — ausführliche Anleitung zu einem
  bestimmten Werkzeug, mit Beispielen und Fehler-Klassen

Damit kann sich ein neues Modell nach einem Restart selbst
**neu orientieren** ohne dass Sie ihm erklären müssen wie ForgeIEC
funktioniert.

---

## Anvil / Bellows / HMI-Anbindung

Der Helfer kann auch die HMI-Brücke (Bellows) und die SHM-IPC-Schicht
(Anvil) ansprechen:

- **Bellows-Gruppen + Variablen** auflisten und lesen
- **Anvil-Topics** auflisten + lesen
- **Anvil-Plugin-Status** + Health-Check
- **Modbus-Bridge-Status** (tongs-modbustcp)

Das ist Diagnose-Material wenn die HMI etwas anderes sieht als die
SPS.

---

## Editor-Bedienung

Ein paar Editor-Aktionen sind ebenfalls über die KI ansprechbar:

- **Editor beenden** — sauberer Stop ohne kill -9
- **Letzte Studio-Logs** ansehen — was hat ForgeIEC Studio selbst geloggt
- **Confirm-Antworten** abrufen / beantworten
- **Pending Confirmations** auflisten

---

## Weiter

- [Personas](/help/ai/agents/) — welcher Charakter darf welche der
  obigen Aktionen
- [Sicherheits-Modell](/help/ai/security/) — warum welche Aktion
  gegated ist
- [Zurück zur AI-Übersicht](/help/ai/)
