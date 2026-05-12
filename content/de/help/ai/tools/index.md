---
title: "Was die KI kann"
summary: "Welche Aktionen kann der KI-Helfer im Editor ausfuehren — Uebersicht in Klartext"
---

## Lesen und Verstehen — immer erlaubt

Diese Aktionen kann der Helfer **immer** ausfuehren, ohne dass Sie was
einschalten muessen:

- **Projekt-Uebersicht** — Name, Anzahl POUs, Anzahl Variablen
- **POUs auflisten** — alle Programme + Function Blocks + Functions
- **POU lesen** — den ST-Code einer einzelnen POU ansehen
- **Variablen auflisten** — alle Pool-Variablen mit Adressen + Typen,
  gefiltert nach Bereich (Globale, POU-Locals, Bellows-Export, …)
- **Bus-Konfiguration** — Segmente, Devices, Variablen-Mapping
- **Aliase** — alle definierten Variablen-Namen + Adressen
- **Bibliothek** — alle Standard-FB-Bausteine (TON, CTU, R_TRIG, …)
  mit Parametern und ST-Beispielen

Damit kann der Helfer Ihre Codebasis **selber kennenlernen**, bevor
er Vorschlaege macht.

---

## Live-Beobachtung — immer erlaubt

Wenn die SPS laeuft, kann der Helfer die laufenden Werte abfragen:

- **Live-Snapshot** — alle ueberwachten Variablen auf einmal lesen
- **Einzelwert** — eine bestimmte Adresse abfragen
- **SPS-Status** — laeuft sie, wie viel Watch-Verkehr, letzter Upload
- **Cycle-Statistiken** — Task-Zeit, Jitter, min/max/Durchschnitt
- **SPS-Code-Status** — Run / Pause / Stopp
- **Aufzeichnung starten/stoppen** — Live-Werte fuer spaetere Analyse
- **Oszilloskop-Aufnahme** — Zeitreihe einer oder mehrerer Adressen,
  mit optionalem Trigger (Flanke, Schwellwert)

Damit kann der Helfer eine **Diagnose** machen: „Warum schaltet
`Motor_Bereit` nicht? Schau dir die letzten 5 Sekunden auf
dem Oszi an."

---

## Aenderungen — nur in der freigeschalteten Version

Folgende Aktionen aendern Ihr Projekt oder die SPS. Sie sind in der
**Standard-Version aus dem Internet abgeschaltet** und brauchen eine
spezielle Version mit `MCP_OVERRIDE_SECURITIES=ON`. Jede Aktion
gibt vorher eine Rueckfrage:

### Projekt-Aenderungen

- **Variable anlegen** — neue Pool-Variable mit Adresse + Typ
- **Variable umbenennen** oder verschieben — zwischen Pou-lokal,
  Globale, Bellows-Export
- **Variable loeschen** — bitte vorsichtig
- **POU anlegen** — neues Programm, Function Block oder Function
- **POU umbenennen** — Tree-sitter-basiert (Backend-Refactor folgt)
- **POU loeschen** — vorsichtig, Task-Bindings koennen
  dangling werden
- **POU-Body setzen** — den ST-Code austauschen
- **Flag setzen** — Bellows-Export, Retain, Constant, Monitor-Enable

### Kompilieren + Deployen

- **Pre-Compile-Check** — schnelle Syntax-Pruefung ohne g++
- **Vollstaendiger Compile** — wie der Build-Knopf in der Toolbar
- **Code generieren** — die generierten C-Dateien anschauen (ohne
  Deploy)
- **Deploy** — kompilieren, hochladen, SPS-Binary neustarten
- **Deploy-Status** — Phasen + g++ stderr beim letzten Deploy

### SPS-Steuerung

- **Start** — SPS-Run-Befehl
- **Stop** — SPS-Stop-Befehl, Ausgaenge gehen in Safe-State
- **Pause / Resume** — Cycle anhalten ohne komplettes Stop
- **Force** — eine Variable festsetzen (NUR ueber die GUI moeglich,
  **nicht** ueber die KI; siehe [Sicherheits-Modell](/help/ai/security/))

---

## Aufgaben + Task-Management

Der Helfer kann auch das Task-Setup veraendern:

- **Ressourcen auflisten** + **Task auflisten** in einer Ressource
- **Programm-Instanzen** einer Task lesen
- **Neue Task anlegen** mit Cycle-Time + Prioritaet
- **Programm-Instanz auf Task legen**
- **Cycle-Uebersicht** ueber alle Tasks

---

## Helfer fragt sich selbst aus

Wenn die KI nicht weiss was ein bestimmtes Werkzeug tut, kann sie
**ihre eigene Hilfe** abfragen:

- `forge.help` — Cheat-Sheet aller verfuegbaren Aktionen mit kurzen
  Beschreibungen, gruppiert nach Familie
- `forge.help_for(name)` — ausfuehrliche Anleitung zu einem
  bestimmten Werkzeug, mit Beispielen und Fehler-Klassen

Damit kann sich ein neues Modell nach einem Restart selbst
**neu orientieren** ohne dass Sie ihm erklaeren muessen wie ForgeIEC
funktioniert.

---

## Anvil / Bellows / HMI-Anbindung

Der Helfer kann auch die HMI-Bruecke (Bellows) und die SHM-IPC-Schicht
(Anvil) ansprechen:

- **Bellows-Gruppen + Variablen** auflisten und lesen
- **Anvil-Topics** auflisten + lesen
- **Anvil-Plugin-Status** + Health-Check
- **Modbus-Bridge-Status** (tongs-modbustcp)

Das ist Diagnose-Material wenn die HMI etwas anderes sieht als die
SPS.

---

## Editor-Bedienung

Ein paar Editor-Aktionen sind ebenfalls ueber die KI ansprechbar:

- **Editor beenden** — sauberer Stop ohne kill -9
- **Letzte Editor-Logs** ansehen — was hat der Editor selbst geloggt
- **Confirm-Antworten** abrufen / beantworten
- **Pending Confirmations** auflisten

---

## Weiter

- [Personas](/help/ai/agents/) — welcher Charakter darf welche der
  obigen Aktionen
- [Sicherheits-Modell](/help/ai/security/) — warum welche Aktion
  gegated ist
- [Zurueck zur AI-Uebersicht](/help/ai/)
