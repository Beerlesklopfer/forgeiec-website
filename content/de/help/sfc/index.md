---
title: "Sequential Function Chart Editor (SFC)"
summary: "Schritt-Übergangs-Modell für Ablaufsteuerungen und Modi-Maschinen"
---

## Überblick

Sequential Function Chart (SFC) ist die dritte grafische IEC-61131-3-Sprache
und beschreibt **zustandsorientierte Abläufe** über ein Schritt-Übergangs-
Modell — formal verwandt mit dem Petri-Netz. Ein SFC-Diagramm besteht aus
einer Folge von **Schritten** (Steps), die über **Übergänge** (Transitions)
mit Bedingungen verbunden sind. Aktiv ist immer eine Teilmenge der Schritte;
ein Schritt wird verlassen, sobald der nachfolgende Übergang TRUE wird.

SFC ist die natürliche Sprache für **Ablaufsteuerungen, Modi-Maschinen
und Batch-Prozesse** — alles, was sich als „erst dies, dann jenes, außer
wenn ..." formulieren lässt.

## Editor-Layout

Der SFC-Editor folgt dem gleichen dreiteiligen Schema wie FBD und LD:
Toolbar oben, QGraphicsView mit Grid + Zoom + Pan, Variablentabelle rechts.
Die Toolbar bietet Werkzeuge für alle SFC-Element-Typen.

## Element-Typen

### Schritt (Step)

Ein Schritt ist eine **Rechteck-Box** mit Namen. Solange er aktiv ist,
laufen seine zugeordneten Aktionen.

* **Initial-Schritt:** Der Einstiegspunkt der POU. Wird beim Programmstart
  aktiv. Im Editor mit **doppelter Umrandung** dargestellt.
* **Folgeschritte:** Mit einfacher Umrandung. Werden aktiv, wenn der
  vorausgehende Übergang feuert.

Ports: oben (IN, vom vorherigen Übergang), unten (OUT, zum nächsten
Übergang), rechts (Verbindung zu Action-Blöcken).

### Übergang (Transition)

Ein Übergang ist ein **kurzer horizontaler Balken** auf der vertikalen
Verbindungslinie zwischen zwei Schritten. Rechts neben dem Balken steht
die **Bedingung** — entweder als ST-Ausdruck (z.B. `tmr.Q AND xReady`)
oder als Output eines Funktionsblocks.

Wird die Bedingung TRUE, deaktiviert sich der vorausgehende Schritt und
der nachfolgende wird aktiv.

### Action-Block

Ein Action-Block beschreibt, **was während eines aktiven Schritts
passiert**. Er besteht aus zwei Zellen: links der **Qualifier**, rechts
der **Action-Name** (Verweis auf eine ST-Aktion oder eine
Output-Variable).

| Qualifier | Bedeutung |
|---|---|
| `N` | Non-stored — läuft, solange der Schritt aktiv ist (Default). |
| `P` | Pulse — einmalig für einen Zyklus bei Schritt-Aktivierung. |
| `S` | Set — wird gesetzt und bleibt aktiv über Schrittwechsel hinweg. |
| `R` | Reset — beendet eine zuvor mit `S` gesetzte Aktion. |
| `L` | Limited — läuft maximal die angegebene Zeitdauer. |
| `D` | Delayed — startet erst nach der angegebenen Verzögerung. |

Pro Schritt können mehrere Action-Blöcke angedockt sein.

### Divergenz und Konvergenz

Eine **Divergenz** verzweigt den Ablauf in mehrere Pfade, eine
**Konvergenz** führt sie wieder zusammen. SFC kennt zwei Sorten:

* **Selection (OR-Verzweigung):** Genau **einer** der Pfade wird
  betreten — abhängig davon, welche Übergangsbedingung zuerst TRUE
  wird. Dargestellt als **einfacher horizontaler Balken**.
* **Parallel (AND-Verzweigung):** **Alle** Pfade werden gleichzeitig
  aktiv und laufen unabhängig voneinander. Erst wenn alle den
  Konvergenz-Punkt erreicht haben, geht der Ablauf weiter.
  Dargestellt als **doppelter horizontaler Balken**.

### Sprung (Jump)

Ein Sprung-Item ist ein **abwärts gerichteter Pfeil** mit dem Namen
des Ziel-Schritts. Er springt aus dem aktuellen Pfad an einen benannten
Schritt — typisch für „zurück zum Start" am Ende einer Sequenz oder
für Fehler-Behandlung („spring zu `Step_Error`").

## Anwendung

SFC eignet sich immer dann, wenn ein Programm einen klaren **zeitlichen
Ablauf** hat:

* **Maschinenmodi** — Init → Idle → Running → Cleanup → Idle.
* **Batch-Prozesse** — Befüllen → Heizen → Mischen → Entleeren.
* **Sicherheitsabläufe** — Stop-Sequenzen mit definierter Reihenfolge
  abfahren („zuerst Heizung aus, dann Pumpe aus, dann Hauptschütz").
* **Verfahrenstechnik** — Reaktionsschritte mit Wartezeiten und
  Bedingungen.

Im Vergleich zu einer ST-Implementierung gleicher Funktion ist die
SFC-Variante deutlich besser ablesbar — die Reihenfolge der Schritte
und die Verzweigungsbedingungen sind grafisch unmittelbar sichtbar,
während in ST eine `CASE state OF`-Konstruktion dieselbe Information
nur indirekt vermittelt.

## Verwandte Themen

* [Function Block Diagram](../fbd/) — für die Logik **innerhalb**
  einer Aktion oder einer Transition-Bedingung.
* [Ladder Diagram](../ld/) — alternative grafische Sprache für
  einfachere Verriegelungen.
* [Library](../library/) — Timer (`TON`, `TP`) sind oft Bestandteil
  von Transition-Bedingungen.
