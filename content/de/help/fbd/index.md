---
title: "Function Block Diagram Editor (FBD)"
summary: "Grafische Verschaltung von Funktionen, Funktionsbloecken und Variablen"
---

## Ueberblick

Das Function Block Diagram (FBD) ist eine der drei grafischen IEC-61131-3-
Sprachen, die ForgeIEC Studio unterstuetzt. Ein FBD-Programm besteht aus
**Funktions- und Funktionsblock-Aufrufen**, die ueber **explizite Drahtverbindungen**
(Wires) miteinander und mit Eingangs- bzw. Ausgangsvariablen verschaltet werden.
Im Gegensatz zum Ladder Diagram gibt es im FBD **keine Strom-Schienen** —
jede Verbindung ist ein einzelner Draht, der einen Output-Pin mit einem oder
mehreren Input-Pins koppelt.

## Editor-Layout

Der FBD-Editor ist ein dreiteiliges Widget:

```
+---------------------------------------------+
| Toolbar (Select | Wire | Block | Var | ...) |
+--------------------------------+------------+
|                                |            |
|       QGraphicsView            |  Variablen |
|       Grid + Zoom + Pan        |  -tabelle  |
|                                |  (rechts)  |
|                                |            |
+--------------------------------+------------+
```

* **Toolbar oben:** Werkzeugumschaltung (Select, Wire, Block einfuegen,
  In-/Out-Variable einfuegen, Kommentar, Zoom).
* **QGraphicsView:** Die eigentliche Zeichenflaeche mit Hintergrund-Grid
  (10 px fein, 50 px Major) und Maus-Pan (Mittlere Maustaste).
  Mausrad zoomt um den Cursor.
* **Variablentabelle rechts:** Andockbar, zeigt die lokalen Variablen
  der POU. Drag-and-Drop aus der Tabelle erzeugt ein
  In-/Out-Variable-Item im Editor.

## Werkzeuge

| Tool | Wirkung |
|---|---|
| **Select** | Auswahl, Verschieben, Loeschen von Items. |
| **Wire** | Klick auf einen Output-Port, dann Klick auf einen Input-Port — Verbindung wird angelegt. |
| **Block einfuegen** | Funktion oder Funktionsblock aus der Library platzieren. Die Pin-Liste (Inputs links, Outputs rechts) wird automatisch aus der Library-Definition uebernommen. |
| **InVar / OutVar einfuegen** | Eingangs- oder Ausgangsvariable als Item platzieren. Der Name wird ueber ein Eingabefeld gesetzt und kann eine GVL-, Anvil- oder Bellows-qualifizierte Variable sein. |
| **Kommentar** | Freitext-Notiz ohne Semantik. |

## Blocks und Pins

Ein **Block-Item** stellt einen Aufruf einer Funktion (`ADD`, `SEL`, ...) oder
eines Funktionsblocks (`TON`, `CTU`, ...) dar. Das Item zeigt im Header den
Typ-Namen, darunter den Instanz-Namen (nur bei FBs), und auf den Seitenraendern
die Ports:

```
        +---- TON -----+
        | tonA         |
   IN --| IN          Q|-- timeUp
   PT --| PT         ET|-- elapsed
        +--------------+
```

Inputs liegen **immer links**, Outputs **immer rechts**. Negierte Pins werden
mit einem kleinen Kreis am Port markiert.

## Library-Drag

Aus dem Library-Panel kann jeder Standard- oder User-Block per **Drag-and-Drop
direkt in den Editor** gezogen werden. Beim Loslassen wird die Pin-Liste der
Library-Definition entnommen, und bei Funktionsbloecken erzeugt der Editor
automatisch eine `VAR`-Instanz in der lokalen Variablen-Sektion.

## Round-Trip zu ST

Beim Compile uebersetzt der ForgeIEC-Compiler den FBD-Body in
Structured Text. Topologische Sortierung der Bloecke nach Datenfluss
bestimmt die Ausfuehrungsreihenfolge. Damit gilt: **jeder FBD-Body ist
semantisch gleichwertig zu einem ST-Body**, und die Wahl der Sprache ist
eine reine Lesbarkeitsfrage.

## Beispiel — Einschaltverzoegerung mit `TON`

Eine `TON` (on-delay timer) verzoegert ein Eingangssignal um eine
einstellbare Zeit. In FBD wuerden Sie

  * eine **InVariable** `start` an den `IN`-Pin der `TON`-Instanz draehten,
  * eine **InVariable** mit Wert `T#5s` an den `PT`-Pin,
  * den `Q`-Output mit einer **OutVariable** `lampe` verbinden.

In ST sieht das so aus:

```text
PROGRAM PLC_PRG
VAR
    start  AT %IX0.0 : BOOL;
    lampe  AT %QX0.0 : BOOL;
    tmr    : TON;
END_VAR

tmr(IN := start, PT := T#5s);
lampe := tmr.Q;
END_PROGRAM
```

Genau diese Form generiert der Compiler aus dem FBD-Diagramm — die
Variablen-Instanz `tmr` ist die `Block`-Box, und die beiden Wires sind die
beiden `:=`-Zuweisungen.

## Verwandte Themen

* [Library](../library/) — Welche Bloecke stehen im Block-Picker zur Verfuegung.
* [Variables Panel](../variables/) — Variablendeklaration und Adress-Pool.
* [Ladder Diagram](../ld/) — Strompfad-orientierte Schwester-Sprache.
