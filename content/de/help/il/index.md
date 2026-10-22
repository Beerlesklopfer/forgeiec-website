---
title: "Instruction List Editor"
summary: "IL-Editor: akkumulator-basierte IEC 61131-3 Sprache mit CR-Register"
---

## Überblick

**Instruction List (IL)** ist die assemblernahe Textsprache der
IEC 61131-3 und die historisch erste der fünf IEC-Sprachen. Programme
bestehen aus einer Folge von Instruktionen, die ein einzelnes
internes **Akkumulator-Register** — das *Current Result* (`CR`) —
manipulieren. Jede Zeile ist eine Anweisung der Form

```
[Label:] Operator [Modifier] [Operand] (* Kommentar *)
```

und liest oder schreibt entweder den Akkumulator selbst oder eine
externe Variable.

In ForgeIEC wird IL über den `FIlEditor` editiert — Layout und Tooling
sind analog zum [ST-Editor](../st/) aufgebaut.

## Editor-Layout

```
+----------------------------------------+
| Variablentabelle                       |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT)             |
+========================================+  <- QSplitter (vertikal)
| Code-Bereich                           |  <- FStCodeEdit
| (tree-sitter-il grammar) |
+----------------------------------------+
```

| Bereich | Inhalt |
|---|---|
| **Variablentabelle** (oben) | Deklarationen mit Name, Typ, Initialwert, Adresse, Kommentar — synchron zum `VAR ... END_VAR`-Block. |
| **Code-Bereich** (unten) | IL-Quelltext mit Tree-Sitter-Highlighting (`tree-sitter-il`-Grammatik). |
| **Search Bar** (Ctrl-F / Ctrl-H) | Such- und Ersetzleiste. |

Online-Mode + Inline-Wert-Overlay funktionieren identisch zum ST-Editor.

## Akkumulator-Modell

Der Akkumulator (`CR`) hält das Zwischenergebnis der laufenden
Auswertung. Eine typische Sequenz:

  1. `LD x` — lädt `x` in den Akkumulator (`CR := x`)
  2. `AND y` — verknüpft den Akkumulator mit `y` (`CR := CR AND y`)
  3. `ST z` — speichert den Akkumulator nach `z` (`z := CR`)

Damit ist IL eine **stack-freie, ein-Register-Maschine** — sehr nahe an
den früher dominierenden Mikrocontroller-Plattformen, für die die
Sprache 1993 standardisiert wurde.

## Wichtigste Operatoren

| Gruppe | Operatoren | Wirkung |
|---|---|---|
| **Laden / Speichern** | `LD`, `LDN`, `ST`, `STN` | Akkumulator setzen / nach Variable speichern (`N` = negiert) |
| **Set / Reset** | `S`, `R` | Bit setzen / rücksetzen (BOOL-Variable, falls `CR` = TRUE) |
| **Bit-Logik** | `AND`, `OR`, `XOR`, `NOT` | Akkumulator mit Operand verknüpfen |
| **Arithmetik** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` | Akkumulator + Operand → Akkumulator |
| **Vergleich** | `GT`, `GE`, `EQ`, `NE`, `LE`, `LT` | Vergleichsergebnis nach `CR` |
| **Sprung** | `JMP`, `JMPC`, `JMPCN` | Sprung zu Label (`C` = wenn `CR` = TRUE) |
| **Aufruf** | `CAL`, `CALC`, `CALCN` | Funktionsblock-Instanz aufrufen |
| **Rückkehr** | `RET`, `RETC`, `RETCN` | POU verlassen |

## Modifier

Ein Operator kann durch Suffix-Modifier verfeinert werden:

| Modifier | Bedeutung |
|---|---|
| `N` | **Negation** des Operanden (`LDN x` lädt `NOT x`) |
| `C` | **Conditional** — Operation nur, wenn `CR` = TRUE (`JMPC label`) |
| `(`...`)` | **Klammer-Modifier** — Auswertung verzögern, bis `)` schließt |

Die Klammer-Form ermöglicht zusammengesetzte Ausdrücke ohne
Zwischen-Variablen:

```
LD   a
AND( b
OR   c
)
ST   result            (* result := a AND (b OR c) *)
```

## Wann IL statt ST?

ST ist heute die Default-Wahl. IL bleibt sinnvoll, wenn:

  - **Mikrocontroller-Performance** den Ausschlag gibt — IL bildet sich
    in den meisten matiec-Backends 1:1 auf Maschinen-Befehle ab, ohne
    Zwischen-Optimierungen.
  - **Altsysteme** kompatibel zu pflegen sind (S5/S7-AWL-portierte Logik,
    älterer ABB-/Beckhoff-Bestand).
  - **Sehr knappe Logik-Blöcke** — Selbsthaltungen, Verriegelungen,
    Edge-Conditions sind in IL oft zwei Zeilen kürzer als in ST.

Für alles andere ist ST lesbarer und einfacher zu warten.

## Code-Beispiel — Selbsthaltung mit Schließer/Öffner

Klassische **Schütz-Selbsthaltung** in IL: Tastendruck `start` schaltet
das Schütz `K1` an, der Stop-Taster `stop` (Öffner, low-aktiv)
schaltet ab. Logik:

```
K1 := (start OR K1) AND NOT stop
```

In IL:

```
PROGRAM Selbsthaltung
VAR
    start  AT %IX0.0 : BOOL;       (* Schliesser-Taster *)
    stop   AT %IX0.1 : BOOL;       (* Oeffner-Taster, low-aktiv *)
    K1     AT %QX0.0 : BOOL;       (* Schuetz *)
END_VAR

    LD    start
    OR    K1                    (* CR := start OR K1 *)
    ANDN  stop                  (* CR := CR AND NOT stop *)
    ST    K1                    (* K1 := CR *)
END_PROGRAM
```

Vier Instruktionen, ein Register, kein temp-Speicher. Genau die
Konstruktionen, für die IL ursprünglich entworfen wurde.

## Verwandte Themen

- [Structured Text](../st/) — die Pascal-ähnliche Schwester-Sprache
- [Bibliothek](../library/) — Funktionsblöcke, die per `CAL` aufrufbar sind
- [Projekt-Dateiformat](../file-format/) — IL-Body in `<body><IL>...`
