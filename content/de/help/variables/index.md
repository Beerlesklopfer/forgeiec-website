---
title: "Variablen-Verwaltung"
summary: "Das Variables-Panel als zentrale Sicht auf den FAddressPool — Spalten, Filter, Bulk-Operationen, Sicherheits-Schalter"
---

## Ueberblick

Das **Variables-Panel** ist die zentrale Sicht auf den **FAddressPool** —
die einzige Quelle der Wahrheit fuer alle Variablen eines ForgeIEC-Projekts.
Jede Variable existiert genau einmal im Pool, identifiziert ueber ihre
IEC-Adresse (`%IX0.0`, `%QW3`, ...). Container wie GVL, AnvilVarList,
HmiVarList oder POU-Interfaces sind nur **Sichten** auf diesen Pool — kein
Variable lebt in zwei Stores parallel.

```
FAddressPool  (Single Source of Truth)
   |
   +-- FAddressPoolModel  (Qt-Tabelle)
         |
         +-- FVariablesPanel  (Filter + Bulk-Ops + Clipboard)
               |
               +-- Tree-Filter setzt FilterMode + Tag
```

Das Panel oeffnet sich an der unteren Andockstelle des Hauptfensters und
spiegelt jede Aenderung sofort in alle anderen Sichten (POU-Editor,
ST-Compiler, PLCopen-XML-Save).

## Spalten

Die Tabelle hat **15 Spalten**, die sich ueber das Header-Kontextmenue
einzeln ein- und ausblenden lassen — jede POU-Editor-Instanz speichert
ihre Spalten-Sichtbarkeit unabhaengig.

| Spalte | Inhalt |
|---|---|
| **Name** | Programmer-sichtbarer Name. Bei qualifizierten Pool-Eintraegen mit voll-qualifiziertem Pfad: `Anvil.Pfirsich.T_1`, `Bellows.Stachelbeere.T_Off`, `GVL.Motor.K1_Mains`. |
| **Type** | IEC-Elementartyp oder benutzerdefinierter Typ. Array-Variablen erscheinen als `ARRAY [0..7] OF BOOL`. |
| **Direction** | IEC-Var-Klasse: `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` fuer POU-Locals; `in`/`out` fuer Pool-Globals (abgeleitet aus der Adresse `%I` vs. `%Q`). |
| **Address** | IEC-Adresse — Primaerschluessel. `%IX0.0` fuer Bit-Eingang, `%QW1` fuer Word-Ausgang, `%MX10.3` fuer Merker-Bit. |
| **Initial** | Initialwert (`FALSE`, `0`, `T#100ms`, `'OFF'`). Wird beim ersten Zykluslauf in die Variable geladen. |
| **Bus Device** | UUID des Bus-Devices (Modbus-Slave o.ae.), an das diese Variable gebunden ist — als ComboBox bedienbar. |
| **Bus Addr** | Modbus-Register-Offset relativ zum Slave (`0`, `1`, ...). |
| **R** (Retain) | Checkbox — bleibt der Wert bei einem Power-Cycle erhalten? |
| **C** (Constant) | Checkbox — IEC-Konstante (`VAR CONSTANT`), Wert nicht zur Laufzeit aenderbar. |
| **RO** (ReadOnly) | Checkbox — von Programm-Code aus nur lesbar. |
| **Sync** | Multi-Task-Sync-Klasse (`L`/`A`/`D`) — ergibt sich aus dem letzten Compile-Lauf des ST-Compilers. |
| **Used by** | Welche Tasks lesen/schreiben diese Variable, z.B. `PROG_Fast (R/W), PROG_Slow (R)`. |
| **Monitor** / **HMI** / **Force** | Sicherheits-Schalter pro Variable. **Cluster A** im Backlog — explizite Opt-ins, separat vom `hmiGroup`-Tag. Der ST-Compiler verifiziert vor der Codegen, dass Force/HMI nur auf Variablen wirkt, die das Flag tragen. |
| **Live** | Laufzeitwert beim Online-Modus (vom anvild-Live-Value-Store gespeist; ausgeblendet wenn keine Verbindung). |
| **Scope** | Oszilloskop-Sichtbarkeit als Checkbox — schickt die Variable in das Oszilloskop-Panel. |
| **Documentation** | Freitext-Kommentar. |

## Filter-Modi

Das Panel zeigt nicht den gesamten Pool auf einmal — der **Project-Tree
links** waehlt, welcher Ausschnitt sichtbar ist. Beim Klick auf einen
Tree-Knoten setzt das Hauptfenster `FilterMode` + Tag-Wert:

| FilterMode | Zeigt |
|---|---|
| `FilterAll` | Den gesamten Pool — keine Tag-Einschraenkung. |
| `FilterByGvl` | Variablen mit `gvlNamespace == tag` (z.B. nur `GVL.Motor`). |
| `FilterByAnvil` | Variablen mit `anvilGroup == tag` (eine Anvil-IPC-Gruppe). |
| `FilterByHmi` | Variablen mit `hmiGroup == tag` (eine Bellows-HMI-Gruppe). |
| `FilterByBus` | Variablen mit `busBinding.deviceId == tag` (alle Variablen eines Bus-Devices). |
| `FilterByModule` | Wie `FilterByBus`, zusaetzlich `moduleSlot` — Tag-Format `hostname:slot`. |
| `FilterByPou` | POU-Locals — Variablen mit `pouInterface == tag`. |
| `FilterCommentsOnly` | Nur Comment-Divider, ohne Variablen. |

## Filter-Achsen (kombinierbar)

Zusaetzlich zum Tree-Filter haengen ueber der Tabelle vier weitere
Achsen, die alle gleichzeitig wirken:

  - **Free-Text-Suche** ueber Name, Adresse und Tags — `to` findet `T_Off`.
  - **IEC-Type-Filter** als Combo (`all` / `BOOL` / `INT` / `REAL` / ...).
  - **Address-Range-Filter**: `all` / `%I` (Eingaenge) / `%Q` (Ausgaenge) /
    `%M` (Merker), bei `%M` weiter nach Wortbreite (`%MX` / `%MW` / `%MD` /
    `%ML`).
  - **TaggedOnly-Toggle** — versteckt alle Pool-Eintraege ohne irgendeinen
    Container-Tag (nuetzlich, um „verwaisten" Pool zu finden).

Alle Filter sind UND-verknuepft: was nicht in jeder aktiven Achse passt,
ist ausgeblendet.

## Multi-Select + Bulk-Operationen

Wie in jeder Qt-Tabelle: Shift-Klick und Strg-Klick selektieren Bereiche
bzw. einzelne Zeilen. Das Kontextmenue auf der Selektion bietet:

  - **Set Anvil Group...** — setzt `anvilGroup` auf allen markierten Vars.
  - **Set HMI Group...** — analog fuer `hmiGroup`.
  - **Set GVL Namespace...** — analog fuer `gvlNamespace`.
  - **Clear Tag** — entfernt den Tag des aktiven Filter-Modus.
  - **Toggle Monitor / HMI / Force** — Bulk-Toggle der Sicherheits-Schalter.

Alle Bulk-Edits laufen ueber `FAddressPoolModel::applyToRows`, ergeben
ein einziges `dataChanged`-Signal und sind als ein Undo-Step rueckgaengig.

## Clipboard (Copy / Cut / Paste)

Selektierte Variablen lassen sich kopieren — **mit allen Tags und Flags**
— und in einer anderen Sicht wieder einfuegen. Das Format:

  - **Custom-MIME** (`application/x-forgeiec-vars+json`) als Roundtrip-
    Vehikel mit voller Pool-Information.
  - **TSV-Plain-Text** als Fallback fuer Excel / Texteditor.

Beim **Paste** retargetiert das Panel die Container-Tags automatisch auf
den **aktiven Filter-Modus**: kopierst du aus `FilterByAnvil` (Gruppe
`Pfirsich`) und fuegst in `FilterByHmi` (Gruppe `Stachelbeere`) ein, so
trauen die Variablen ihre `anvilGroup` ab und bekommen `hmiGroup =
Stachelbeere`. Adressen und Namen werden bei Konflikten dedupliziert
(`T_1` → `T_1_1`).

## Drag/Drop in HmiVarList

Variablen aus dem Hauptpanel lassen sich per Drag in eine HmiVarList-POU
ziehen. Dabei setzt der Editor automatisch das **HMI-Export-Flag** der
Variable und traegt die HMI-Gruppe als Tag ein — der Export an Bellows
ist dann scharf.

## Per-Variable Sicherheits-Schalter

Drei Schalter pro Variable, die explizit aktiviert werden muessen:

  - **HMI** — erlaubt Bellows, die Variable zu lesen/schreiben.
  - **Monitor** — erlaubt Live-Beobachtung im Online-Modus.
  - **Force** — erlaubt das Erzwingen eines Werts zur Laufzeit.

Diese Flags sind **separat vom `hmiGroup`-Tag**. Der Tag beschreibt nur
Gruppenzugehoerigkeit; das Flag ist die Wirkungs-Aktivierung. Der
ST-Compiler prueft vor jeder Codegen, dass jeder Bellows- oder
Force-Zugriff auf eine entsprechend freigeschaltete Variable trifft —
sonst Compile-Fehler.

## Verwandte Themen

  - [Variable hinzufuegen](add/) — der `FAddVariableDialog` mit
    Range-Pattern und Array-Wrapper.
  - [Projekt-Dateiformat](../file-format/) — wie der Pool als
    `<addData>`-Block in PLCopen-XML persistiert wird.
  - [Bibliothek](../library/) — wie Funktionsbloecke ihre Instanzen im
    Pool sehen.
