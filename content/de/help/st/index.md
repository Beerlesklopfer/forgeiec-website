---
title: "Structured Text Editor"
summary: "ST-Editor + Sprachfundamente: IEC 61131-3 Statements, Bit-Zugriff, qualifizierte Pool-Referenzen"
---

## Überblick

**Structured Text (ST)** ist die Pascal-ähnliche Hochsprache der
IEC 61131-3 und der Standard-Editor für PROGRAM-, FUNCTION_BLOCK- und
FUNCTION-POUs in ForgeIEC. Der Editor ist eine `QWidget`-basierte
Komposition aus Variablentabelle und Code-Bereich, gekoppelt durch einen
vertikalen Splitter.

```
+----------------------------------------+
| Variablentabelle                       |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT/VAR_INST)    |
+========================================+  <- QSplitter (vertikal)
| Code-Bereich                           |  <- FStCodeEdit
| (Tree-Sitter highlighting + Folding +  |
|  Ctrl-Space Completion)                |
+----------------------------------------+
```

## Editor-Layout

| Bereich | Inhalt |
|---|---|
| **Variablentabelle** (oben) | Deklarationen mit Spalten Name, Typ, Initialwert, Adresse, Kommentar. Änderungen synchronisieren sich live in den `VAR ... END_VAR`-Block des Codes. |
| **Code-Bereich** (unten) | ST-Quelltext zwischen den Variablensektionen. Zeilenfolding über den Tree-Sitter-AST, Zeilennummern, Cursor-Line-Highlight. |
| **Search Bar** (Ctrl-F / Ctrl-H) | Eingeblendet über dem Code-Bereich, mit Replace-Modus für Such-und-Ersetzen. |

Der Splitter speichert seine Position pro POU im Layout-State.

## Tree-Sitter Syntax-Highlighting

Statt eines regex-basierten `QSyntaxHighlighter` parst ForgeIEC den
ST-Quelltext mit **Tree-Sitter** zu einem AST und färbt anhand von
Capture-Queries:

  - **Keywords** (`IF`, `THEN`, `FOR`, `FUNCTION_BLOCK`, ...): Magenta
  - **Datentypen** (`BOOL`, `INT`, `REAL`, `TIME`, ...): Türkis
  - **Strings + Zeitliterale** (`'abc'`, `T#20ms`): Grün
  - **Kommentare** (`(* ... *)`, `// ...`): Grau, kursiv
  - **PUBLISH / SUBSCRIBE**: Anvil-Erweiterungs-Keywords, eigener Stil

Vorteil: Highlighting bleibt korrekt bei komplexen Konstrukten
(verschachtelte Kommentare, Zeit-Literale, qualifizierte Referenzen),
und derselbe AST liefert die foldbaren Bereiche für Code-Folding.

## Code-Completion (Ctrl-Space)

Drücken von **Ctrl-Space** oder das Tippen von zwei Zeichen öffnet das
Completion-Popup. Der Completer kennt:

  - **IEC-Keywords** (`IF`, `CASE`, `FOR`, `WHILE`, `RETURN`, ...)
  - **Datentypen** (`BOOL`, `INT`, `DINT`, `REAL`, `STRING`, `TIME`, ...)
  - **Lokale Variablen** der aktuellen POU
  - **POU-Namen** des Projekts (PROGRAM, FUNCTION_BLOCK, FUNCTION)
  - **Library-Blöcke** (`TON`, `R_TRIG`, `JK_FF`, `DEBOUNCE`, ...)
  - **Standard-Funktionen** (`ABS`, `SQRT`, `LIMIT`, `LEN`, ...)

Änderungen am Variablen-Pool (`poolChanged`-Signal) werden mit 100 ms
Debounce in das Completion-Modell übernommen — neue Pool-Einträge sind
dadurch fast augenblicklich verfügbar, ohne dass jede Tastatur-Eingabe
einen Vollscan auslöst.

## Sprachfundamente (IEC 61131-3)

### Statements

| Statement | Form |
|---|---|
| **Zuweisung** | `var := expression;` |
| **IF / ELSIF / ELSE** | `IF cond THEN ... ELSIF cond THEN ... ELSE ... END_IF;` |
| **CASE** | `CASE x OF 1: ... ; 2,3: ... ; ELSE ... END_CASE;` |
| **FOR** | `FOR i := 1 TO 10 BY 1 DO ... END_FOR;` |
| **WHILE** | `WHILE cond DO ... END_WHILE;` |
| **REPEAT** | `REPEAT ... UNTIL cond END_REPEAT;` |
| **EXIT / RETURN** | Schleife verlassen / POU verlassen |

### Expressions

Standard-Operatoren mit IEC-Präzedenz: `**`, unäres `+/-/NOT`, `* / MOD`,
`+ -`, Vergleiche, `AND / &`, `XOR`, `OR`. Klammern wie in Pascal.
Implizite numerische Typkonvertierungen sind nicht erlaubt — `INT_TO_DINT`,
`REAL_TO_INT` etc. sind explizit aufzurufen.

### Bit-Zugriff auf ANY_BIT-Typen

`var.<bit>` extrahiert oder setzt ein einzelnes Bit, direkt auf
`BYTE`/`WORD`/`DWORD`/`LWORD`-Variablen:

```text
status.0 := TRUE;             (* Bit 0 setzen *)
alarm := flags.7 OR flags.3;  (* Bits lesen *)
```

Der Compiler übersetzt das in saubere Bit-Maskierung mit `AND`/`OR`/Shift,
ohne Helfer-Variablen.

### 3-Level qualifizierte Referenzen

`<Category>.<Group>.<Variable>` greift direkt auf Pool-Einträge zu, ohne
GVLs explizit deklarieren zu müssen:

| Prefix | Quelle |
|---|---|
| `Anvil.X.Y`   | Pool-Eintrag mit `anvilGroup="X"` |
| `Bellows.X.Y` | Pool-Eintrag mit `hmiGroup="X"` |
| `GVL.X.Y`     | Pool-Eintrag mit `gvlNamespace="X"` |
| `HMI.X.Y`     | Synonym für `Bellows.X.Y` |

`Anvil.X.Y` und `Bellows.X.Y` können unabhängig voneinander auf
unterschiedliche Pool-Einträge zeigen — der Compiler emittiert getrennte
C-Symbole, sobald die IEC-Adressen sich unterscheiden.

### Adressierte Variablen (`AT %...`)

Located variables binden eine Deklaration an eine IEC-Adresse:

```text
button_raw    AT %IX0.0  : BOOL;
motor_speed   AT %QW1    : INT;
flag_persist  AT %MX10.3 : BOOL;
```

Adresse ist Primärschlüssel im Pool — siehe
[Projekt-Dateiformat](../file-format/).

## Code-Beispiele

### Beispiel 1 — TON-Aufruf mit Library-Block

```text
PROGRAM PLC_PRG
VAR
    start_button   AT %IX0.0  : BOOL;
    motor_run      AT %QX0.0  : BOOL;
    fbDelay        : TON;
END_VAR

fbDelay(IN := start_button, PT := T#3s);
motor_run := fbDelay.Q;
END_PROGRAM
```

`fbDelay` ist eine Instanz des Library-FB `TON`. Nach 3 Sekunden
gehaltenem `start_button` schaltet `motor_run` auf TRUE.

### Beispiel 2 — Bellows-Read mit Force auf Output

```text
PROGRAM Lampen
VAR
    relay_lamp  AT %QX0.1 : BOOL;
END_VAR

(* HMI-Bedienpanel kann Bellows.Pfirsich.T_1 schreiben *)
relay_lamp := Bellows.Pfirsich.T_1 OR Anvil.Sensors.contact_door;
END_PROGRAM
```

`Bellows.Pfirsich.T_1` und `Anvil.Sensors.contact_door` sind 3-Level-
Referenzen, die der Compiler ohne GVL-Deklaration auflöst — vorausgesetzt,
beide Tags sind im Adress-Pool gepflegt und der HMI-Export für die
Gruppe `Pfirsich` ist aktiv.

## Verwandte Themen

- [Bibliothek](../library/) — verfügbare Funktionsblöcke + Funktionen
- [Instruction List](../il/) — alternativer Text-Editor (akkumulator-basiert)
- [Projekt-Dateiformat](../file-format/) — wie ST-Code in `.forge` gespeichert wird
