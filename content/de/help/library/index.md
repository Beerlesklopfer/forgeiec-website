---
title: "Bibliothek (Funktionsbloecke + Funktionen)"
summary: "IEC 61131-3 Standard-Bibliothek + ForgeIEC-Erweiterungen + benutzerdefinierte Bloecke"
---

## Ueberblick

Die ForgeIEC-Bibliothek ist die zentrale Sammlung aller wiederverwendbaren
Bausteine, die ein Anwendungsprogramm in einem `.forge`-Projekt aufrufen
kann — sowohl die nach IEC 61131-3 standardisierten Funktionsbloecke
und Funktionen als auch projekt-eigene und ForgeIEC-spezifische
Erweiterungen.

Sie wird angezeigt im **Library-Panel** (Standard-Andockstelle: rechte
Seitenleiste). Druecken Sie **F1** im Library-Panel, um direkt diese Seite
zu oeffnen.

```
Library
+-- Standard Function Blocks    (Bistable, Edge, Counter, Timer, ...)
+-- Standard Functions          (Arithmetic, Comparison, Bitwise, ...)
+-- User Library                (projekt-eigene Bausteine)
```

Die Bibliothek hat heute **knapp 100 Bloecke** und **gut 30 Funktionen**.
Jeder Eintrag traegt:

  - **Name** (z.B. `TON`, `JK_FF`)
  - **Pin-Liste** (Inputs + Outputs mit Typ + Position)
  - **Typ** (`FUNCTION_BLOCK` mit Zustand, oder `FUNCTION` zustandslos)
  - **Beschreibung** + **Hilfetext** mit Anwendungs-Hinweisen
  - **Code-Beispiel** (im Library-Help-Panel sichtbar)

## Kategorien-Baum

### Standard Function Blocks

| Gruppe | Bloecke |
|---|---|
| **Bistable** | `SR`, `RS` — Setze/Ruecksetze mit Vorrang |
| **Edge Detection** | `R_TRIG`, `F_TRIG` — steigende/fallende Flanke |
| **Counters** | `CTU`, `CTD`, `CTUD` — Zaehler vorwaerts / rueckwaerts / beides |
| **Timers** | `TON`, `TOF`, `TP` — Einschalt-/Ausschaltverzoegerung / Impulszeit |
| **Motion** | Profile, Rampen, Trajektorien (in Vorbereitung) |
| **Signal Generation** | Generator-FBs fuer Test- und Pruefsignale |
| **Function Manipulators** | Hold, Latch, History |
| **Closed-Loop Control** | PID, Hysterese, Zwei-Punkt |
| **Application** *(ForgeIEC)* | `JK_FF`, `DEBOUNCE` — anwendungsnahe Bausteine, die sich in der Praxis als „universell hilfreich" erwiesen haben |

### Standard Functions

| Gruppe | Inhalt |
|---|---|
| **Arithmetic** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` (auf jedem ANY_NUM-Typ) |
| **Comparison** | `EQ`, `NE`, `LT`, `LE`, `GT`, `GE` |
| **Bitwise** | `AND`, `OR`, `XOR`, `NOT` (auf ANY_BIT-Typen — siehe `help/st`) |
| **Bit Shift** | `SHL`, `SHR`, `ROL`, `ROR` |
| **Selection** | `SEL`, `MAX`, `MIN`, `LIMIT`, `MUX` |
| **Numeric** | `ABS`, `SQRT`, `LN`, `LOG`, `EXP`, `SIN`, `COS`, `TAN`, `ASIN`, `ACOS`, `ATAN` |
| **String** | `LEN`, `LEFT`, `RIGHT`, `MID`, `CONCAT`, `INSERT`, `DELETE`, `REPLACE`, `FIND` |
| **Type Conversion** | `BOOL_TO_INT`, `REAL_TO_DINT`, `STRING_TO_INT`, ... |

### User Library

Eigene Funktionsbloecke und Funktionen aus dem laufenden Projekt — alles,
was als `FUNCTION_BLOCK` oder `FUNCTION` deklariert wurde, wandert
automatisch in diese Kategorie und kann genauso wie die Standard-Bloecke
ueberall im Projekt aufgerufen werden.

## Library-Panel — Bedienung

| Aktion | Effekt |
|---|---|
| **Suche** (Lupe oben) | Filtert die Tree-Ansicht nach Block-Namen — findet `TON` ueber Eingabe von `to`. |
| **Doppelklick** auf einen Block | Oeffnet die Block-Hilfe in einem Detail-Panel mit Pin-Beschreibung + Code-Beispiel. |
| **Drag** auf den ST-Editor | Fuegt den Block-Aufruf an der Cursor-Position ein, inklusive Instanz-Deklaration in der lokalen `VAR_INST`-Sektion. |
| **Rechtsklick** > „Insert Call..." | Genauso wie Drag, aber via Kontextmenue. |
| **F1** auf einem Block | Oeffnet diese Seite. |

## Beispiel 1 — Tasterentprellung mit `DEBOUNCE`

`DEBOUNCE` filtert kurze Stoerimpulse aus einem mechanischen Tasterkontakt
heraus. `Q` wechselt erst, wenn `IN` ueber die gesamte `T_Debounce`-Dauer
stabil bleibt — sowohl bei steigender als auch bei fallender Flanke.

### Pin-Layout

| Pin | Richtung | Typ | Bedeutung |
|---|---|---|---|
| `IN`         | INPUT  | `BOOL` | Roher Eingang (typisch `%IX`, prellt mechanisch) |
| `tDebounce`  | INPUT  | `TIME` | Mindeststabilzeit (typisch `T#10ms`...`T#50ms`) |
| `Q`          | OUTPUT | `BOOL` | Entprellter Ausgang |

### Code-Beispiel

PROGRAM-Body, der einen Drucktaster auf `%IX0.0` entprellt und das
entprellte Signal als single-shot Flanke an einen Selbsthalte-Schuetz
weitergibt:

```text
PROGRAM PLC_PRG
VAR
    button_raw      AT %IX0.0 : BOOL;       (* prellender Schuetzkontakt *)
    button_clean    : BOOL;                  (* nach DEBOUNCE *)
    button_pressed  : BOOL;                  (* single-shot pro Tastendruck *)
    relay_lamp      AT %QX0.0 : BOOL;        (* Lampe als Selbsthalte *)
    fbDeb           : DEBOUNCE;              (* Instanz *)
    fbTrig          : R_TRIG;                (* Flankendetektor *)
END_VAR

fbDeb(IN := button_raw, tDebounce := T#20ms);
button_clean := fbDeb.Q;

fbTrig(CLK := button_clean);
button_pressed := fbTrig.Q;

(* Selbsthaltung: Toggle bei jeder steigenden Flanke *)
IF button_pressed THEN
    relay_lamp := NOT relay_lamp;
END_IF;
END_PROGRAM
```

`DEBOUNCE` ist intern aus zwei `TON`-Bausteinen aufgebaut (high und low
Richtung) — einer schaltet `Q` erst nach `T_Debounce` aktivem `IN` auf
TRUE, der andere erst nach `T_Debounce` inaktivem `IN` auf FALSE. Das macht
den Filter symmetrisch: weder Kontakt-Bouncing beim Druecken noch beim
Loslassen erzeugt einen Stoerimpuls.

> **Typischer Einsatz:** mechanische Taster, Endschalter, kontaktbehaftete
> Sensoren. Fuer „Single-Shot pro Tastendruck" — wie oben — schalten Sie
> einen `R_TRIG` an `Q` nach.

## Beispiel 2 — Selbsthaltung mit Mode-Umschalter (`JK_FF`)

`JK_FF` ist ein Toggle-Flipflop mit eingebauter Tasterentprellung. Auf
jede stabile steigende Flanke an `xButton` toggelt `Q` zwischen TRUE und
FALSE — so dass aus einem einfachen Drucktaster ein „Ein/Aus"-Schalter wird,
**ohne** dass der Anwender im PLC-Programm DEBOUNCE + R_TRIG + Toggle-
Logik selbst zusammenstecken muss.

### Pin-Layout

| Pin | Richtung | Typ | Bedeutung |
|---|---|---|---|
| `xButton`    | INPUT  | `BOOL` | Roher Tasterkontakt (prellt) |
| `tDebounce`  | INPUT  | `TIME` | Entprell-Zeit (typisch `T#20ms`) |
| `J`          | INPUT  | `BOOL` | „Set" (zwingt `Q` auf TRUE solange aktiv) |
| `K`          | INPUT  | `BOOL` | „Reset" (zwingt `Q` auf FALSE solange aktiv) |
| `Q`          | OUTPUT | `BOOL` | Aktueller Zustand |
| `Q_N`        | OUTPUT | `BOOL` | Negierter Zustand (`NOT Q`) |
| `xStable`    | OUTPUT | `BOOL` | TRUE waehrend `xButton` ueber `tDebounce` stabil ist |

### Code-Beispiel

Eine Lampensteuerung mit drei Tastern: `T1` schaltet die Lampe um (Toggle),
`T_Mains` erzwingt sie an (z.B. „Hauptlicht ueberall AN"), `T_Off` schaltet
alles aus:

```text
PROGRAM PLC_PRG
VAR
    bButtons     AT %IX0.0 : ARRAY [0..3] OF BOOL;
    relay_lamp   AT %QX0.0 : BOOL;
    fbToggle     : JK_FF;
END_VAR

fbToggle(
    xButton    := bButtons[0],   (* Toggle-Taster T1 *)
    tDebounce  := T#20ms,
    J          := bButtons[1],   (* Hauptlicht AN, solange gedrueckt *)
    K          := bButtons[2]    (* Hauptlicht AUS, solange gedrueckt *)
);

relay_lamp := fbToggle.Q;
END_PROGRAM
```

Die Wahrheits-Tabelle der `J`/`K`-Eingaenge:

| `J` | `K` | Verhalten |
|---|---|---|
| FALSE | FALSE | Toggle bei jedem entprellten Tastendruck |
| TRUE  | FALSE | Q := TRUE (Set, ueberschreibt Toggle) |
| FALSE | TRUE  | Q := FALSE (Reset, ueberschreibt Toggle) |
| TRUE  | TRUE  | undefiniert — vermeiden |

`xStable` kann genutzt werden, um „Taster wird gerade gehalten"-Logik zu
implementieren (z.B. eine LED, die das Druecken visualisiert ohne auf den
Toggle-Effekt warten zu muessen).

## Library-Sync zwischen Editor und PLC

Die Standard-Bibliothek liegt in beiden Lagen:

  - **Editor-Seite:** `editor/resources/library/standard_library.json`
    (im `.exe` einkompiliert via Qt-Resource-System).
  - **PLC-Seite:** anvild-Submodul, dieselbe JSON-Datei. Wird beim
    `make` der hochgeladenen C-Quellen eingebunden.

Der **Library-Sync** vergleicht die SHA-256 der beiden Versionen beim
Verbindungsaufbau. Bei Drift erscheint ein Hinweis im Output-Panel; die
Reaktion ist konfigurierbar:

  - `Preferences > Library > Auto-Push` aus (Default): manueller Push
    ueber `Tools > Sync Library`. Schuetzt eine produktive Runtime davor,
    versehentlich von einem aelteren Editor-Stand ueberschrieben zu
    werden.
  - `Preferences > Library > Auto-Push` an: bei jedem Drift schickt der
    Editor seine Library-Version automatisch — nuetzlich in Entwicklungs-
    Setups, wo nur ein Programmierer arbeitet.

## ForgeIEC-Erweiterungen

Die folgenden Bausteine sind nicht in IEC 61131-3 standardisiert, aber im
Standard-Bibliotheks-Set enthalten, weil sich ihr Einsatz in der Praxis
als universell hilfreich erwiesen hat:

| Block | Zweck |
|---|---|
| `JK_FF` | Toggle-Flipflop mit eingebauter Tasterentprellung (siehe Beispiel 2). |
| `DEBOUNCE` | Symmetrische Tasterentprellung (siehe Beispiel 1). |

Diese Bausteine liegen in der Kategorie *Standard Function Blocks /
Application* und sind durch das `isStandard: true`-Flag in der JSON-
Source als „nicht-deletbar" markiert (d.h. sie koennen nicht versehentlich
ueber das Library-Panel geloescht werden).

## Eigene Bausteine in die User-Library

Jede `FUNCTION_BLOCK`- und `FUNCTION`-Deklaration im aktuellen Projekt
landet automatisch unter **User Library**. Reihenfolge der Sichtbarkeit:

  1. **Im Library-Panel:** sofort nach Anlegen + Speichern der POU.
  2. **Im Code-Completer (Ctrl-Space):** sofort.
  3. **Im FBD/LD-Editor als Block:** sofort.
  4. **Auf der PLC** nach `Compile + Upload`.

Wenn Sie einen Baustein in mehreren Projekten verwenden wollen, kopieren
Sie die POU per `File > Export POU...` als `.forge-pou`-Datei und
importieren Sie sie im Zielprojekt — eine projektuebergreifende
„Workspace-Library" gibt es heute noch nicht (im Backlog).

## Verwandte Themen

- [Structured Text Syntax](../st/) — wie ein Block-Aufruf in ST aussieht.
- [Function Block Diagram Editor](../fbd/) — wie ein Block grafisch
  ausverdrahtet wird.
- [Variables Panel](../variables/) — wie der Pool die Block-Instanzen sieht.
