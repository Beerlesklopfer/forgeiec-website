---
title: "Variable hinzufuegen"
summary: "Der FAddVariableDialog — alle Felder in einem Modal, Range-Pattern fuer Bulk-Erzeugung, Array-Wrapper"
---

## Ueberblick

Der **FAddVariableDialog** ist das modale Fenster, mit dem eine neue
Variable in einer POU oder im Pool angelegt wird. Er sammelt alle Felder
in einem Schritt und zeigt darunter eine **Live-Vorschau** der
entstehenden IEC-ST-Deklaration — was du tippst, siehst du sofort als
fertigen `VAR ... END_VAR`-Schnipsel.

Der Dialog laeuft in zwei Modi:

  - **Add-Mode**: Felder leer, eine neue Variable wird beim OK angelegt.
    Aufruf ueber das Plus-Symbol im Variables-Panel oder Strg+N im
    POU-Editor.
  - **Edit-Mode**: Doppelklick auf eine bestehende Variable im Panel —
    dasselbe Dialog, alle Felder vorbelegt.

## Felder

| Feld | Pflicht | Bedeutung |
|---|---|---|
| **Name** | ja | Programmer-sichtbarer Name. Validiert gegen IEC-Identifier-Regeln (Buchstabe + Buchstaben/Ziffern/`_`). Fuer Bulk-Erzeugung mit Range-Pattern (siehe unten). |
| **Type** | ja | Combo mit IEC-Elementartypen, Standard-FBs, Project-FBs, User-Datentypen. Array-Erzeugung uebernimmt die Wrapper-Checkbox. |
| **Direction** | je nach POU | Var-Klasse — siehe unten. |
| **Initial** | nein | Initialwert (`FALSE`, `0`, `T#100ms`, `'OFF'`). |
| **Address** | nein | Nur fuer VarList-POUs. Leer = `pool->nextFreeAddress` weist beim Anlegen automatisch zu. |
| **Retain** | nein | Checkbox — RETAIN-Wert ueberlebt Power-Cycle. |
| **Constant** | nein | Checkbox — `VAR CONSTANT`, nicht zur Laufzeit aenderbar. |
| **Array-Wrapper** | nein | Wrapt den ausgewaehlten Type in ein `ARRAY [..] OF`. |
| **Documentation** | nein | Freitext-Kommentar, landet als `<documentation>` im PLCopen-XML. |

## Range-Pattern fuer Bulk-Erzeugung

Statt `LED_0`, `LED_1`, ... `LED_7` einzeln anzulegen, kannst du im
Name-Feld ein **Bereichs-Muster** angeben:

| Eingabe | Wirkung |
|---|---|
| `LED_0..7` | Erzeugt acht Variablen `LED_0` bis `LED_7`. |
| `LED_0-7` | Synonym, gleicher Effekt. |
| `Sensor_1..3` | Erzeugt drei Variablen `Sensor_1` bis `Sensor_3`. |

Bei jedem Bulk-Anlegen wird die Adresse fortlaufend hochgezaehlt, sofern
sie gesetzt ist: `%QX0.0` → `%QX0.0`, `%QX0.1`, ..., `%QX0.7`.

## Array-Wrapper-Checkbox

Wenn du **eine** Variable als Array deklarieren willst, aktiviere die
Array-Checkbox. Dann erscheinen zwei SpinBoxen fuer den Indexbereich
und der Type wird zur Laufzeit als `ARRAY [..] OF <Typ>` wrapt.

| Type-Combo | Array-Checkbox | Indexbereich | Resultierende Deklaration |
|---|---|---|---|
| `INT` | aus | — | `: INT;` |
| `INT` | an | `0..7` | `: ARRAY [0..7] OF INT;` |
| `BOOL` | an | `1..16` | `: ARRAY [1..16] OF BOOL;` |
| `T_Motor` (User-Struct) | an | `0..3` | `: ARRAY [0..3] OF T_Motor;` |

Der Wrapper sitzt **bewusst** an der Checkbox, nicht in der Type-Combo —
so bleibt die Combo uebersichtlich und Array-of-everything ist ohne
Combo-Suche moeglich.

## Type-Combo

Die Combo aggregiert vier Quellen in einer einzigen Liste:

  1. **IEC-Elementartypen**: `BOOL`, `BYTE`, `WORD`, `DWORD`, `LWORD`,
     `INT`, `DINT`, `LINT`, `UINT`, `UDINT`, `ULINT`, `REAL`, `LREAL`,
     `TIME`, `DATE`, `TIME_OF_DAY`, `DATE_AND_TIME`, `STRING`, `WSTRING`.
  2. **Standard-FBs** der Bibliothek: `TON`, `TOF`, `TP`, `R_TRIG`,
     `F_TRIG`, `CTU`, `CTD`, `CTUD`, `SR`, `RS`, ...
  3. **Project-Function-Blocks** — alle FBs aus dem aktuellen Projekt
     (User-Library).
  4. **User-Datentypen** aus `<dataTypes>`: STRUCTs, Enumerationen, Aliase.

ARRAY-Templates erscheinen **nicht** in der Combo — die kommen ueber die
Wrapper-Checkbox.

## Direction (Var-Klasse) je nach POU

Welche Direction-Werte angeboten werden, haengt am POU-Typ:

| POU-Typ | Verfuegbare Direction |
|---|---|
| `PROGRAM` / `FUNCTION_BLOCK` / `FUNCTION` | `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` |
| `GlobalVarList` (GVL) | Fest `VAR_GLOBAL` — Combo ausgeblendet. |
| `AnvilVarList` | Fest `VAR_GLOBAL` (auto-generiert) — Combo ausgeblendet. |
| `Pool-Globals` (ohne POU-Container) | Keine Direction — die Adresse `%I`/`%Q` legt sie implizit fest. |

## Edit-Modus

Doppelklick auf eine bestehende Variable im Variables-Panel oeffnet
denselben Dialog. Alle Felder sind vorbelegt; bei OK werden die
Aenderungen ueber `pou->renameVariable` / `pool->rebind` durchgereicht
(damit die `byAddress`-Indizes synchron bleiben). Der Dialog kennt den
Edit-Modus an `existing != nullptr`.

## Beispiel — 8 LEDs als Block

Acht Ausgangs-LEDs als Pool-Variablen anlegen, in einem Schritt:

  - **Name**: `LED_0..7`
  - **Type**: `BOOL`
  - **Direction**: ausgeblendet (Pool-Global)
  - **Address**: `%QX0.0` (Auto-Increment)
  - **Initial**: `FALSE`

OK erzeugt acht Pool-Eintraege:

```text
LED_0  AT %QX0.0 : BOOL := FALSE;
LED_1  AT %QX0.1 : BOOL := FALSE;
LED_2  AT %QX0.2 : BOOL := FALSE;
LED_3  AT %QX0.3 : BOOL := FALSE;
LED_4  AT %QX0.4 : BOOL := FALSE;
LED_5  AT %QX0.5 : BOOL := FALSE;
LED_6  AT %QX0.6 : BOOL := FALSE;
LED_7  AT %QX0.7 : BOOL := FALSE;
```

Anschliessend lassen sich die acht Variablen im Variables-Panel
selektieren und per Bulk-Operation einer HMI-Gruppe zuweisen — z.B.
`Set HMI Group... → Frontpanel`.

## Verwandte Themen

  - [Variablen-Verwaltung](../) — das Variables-Panel mit Spalten,
    Filtern und Bulk-Operationen.
  - [Projekt-Dateiformat](../../file-format/) — wie der Pool als
    `<addData>`-Block in PLCopen-XML persistiert wird.
