---
title: "Testabdeckung"
summary: "Automatisierte Qualitätssicherung: 62 Testprogramme prüfen den ST-Sprachvorrat, die Standard-Bausteine und das Multi-Task-Threading"
---

ForgeIEC wird durch eine umfassende automatisierte Test-Suite abgesichert.
Die CI führt **62 Testprogramme** aus (CTest-Einträge, gezählt am
22.10.2026 in `tests/CMakeLists.txt`); sie decken den Structured-Text-
Sprachvorrat, die Standard-Funktionsbausteine und das
Multi-Task-Threading-System ab. Die drei wichtigsten Suiten:

## Test-Suiten im Überblick

| Suite | Tests | Prüft |
|-------|------:|--------|
| **FStCompilerTest** | 120 | ST-Sprachvorrat |
| **FStLibraryTest** | 7 | Standard-Bausteine (FBs + FCs) |
| **FCodeGeneratorThreadingTest** | 8 | Multi-Task-Scheduling + Lock-free Sync |

---

## 1. ST-Sprachvorrat (FStCompilerTest)

Die Tests prüfen jeden unterstützten IEC 61131-3 Structured Text
Sprachkonstrukt. Jeder Test kompiliert ein ST-Fragment durch den
FStCompiler und verifiziert den generierten C++-Code.

### 1.1 Zuweisungen

| Test | ST-Code | Prüft |
|------|---------|--------|
| `assignSimple` | `a := 42;` | Einfache Zuweisung |
| `assignExpression` | `a := b + 1;` | Ausdruck-Zuweisung |
| `assignExternal` | `ExtVar := 10;` | VAR_EXTERNAL Zugriff |
| `assignGvlQualified` | `GVL.ExtVar := 5;` | Qualifizierter GVL-Pfad |

### 1.2 Arithmetische Operatoren

| Test | ST-Code | C-Operator |
|------|---------|------------|
| `arithmeticAdd` | `a := b + 1;` | `+` |
| `arithmeticSub` | `a := b - 1;` | `-` |
| `arithmeticMul` | `a := b * 2;` | `*` |
| `arithmeticDiv` | `a := b / 2;` | `/` |
| `arithmeticMod` | `a := b MOD 3;` | `%` |
| `arithmeticPower` | `c := x ** 2.0;` | `EXPT()` |
| `arithmeticNegate` | `a := -b;` | `-(...)` |
| `arithmeticParentheses` | `a := (b + 1) * 2;` | Klammerung |

### 1.3 Vergleichsoperatoren

| Test | ST-Code | C-Operator |
|------|---------|------------|
| `compareEqual` | `flag := a = b;` | `==` |
| `compareNotEqual` | `flag := a <> b;` | `!=` |
| `compareLess` | `flag := a < b;` | `<` |
| `compareGreater` | `flag := a > b;` | `>` |
| `compareLessEqual` | `flag := a <= b;` | `<=` |
| `compareGreaterEqual` | `flag := a >= b;` | `>=` |

### 1.4 Boolesche Operatoren

| Test | ST-Code | C-Operator |
|------|---------|------------|
| `boolAnd` | `flag := flag AND flag;` | `&&` |
| `boolOr` | `flag := flag OR flag;` | `\|\|` |
| `boolXor` | `flag := flag XOR flag;` | `^` |
| `boolNot` | `flag := NOT flag;` | `!` |

### 1.5 Literale

| Test | ST-Code | Prüft |
|------|---------|--------|
| `literalInteger` | `a := 12345;` | Ganzzahl |
| `literalReal` | `c := 3.14;` | Fließkomma |
| `literalBoolTrue` | `flag := TRUE;` | Boolescher Wert |
| `literalBoolFalse` | `flag := FALSE;` | Boolescher Wert |
| `literalString` | `text := 'hello';` | Zeichenkette |
| `literalTime` | `counter := T#500ms;` | Zeitkonstante |

### 1.6 Kontrollstrukturen

**IF / ELSIF / ELSE / END_IF**

| Test | Prüft |
|------|--------|
| `ifSimple` | Einfache Bedingung |
| `ifElse` | If-Else-Verzweigung |
| `ifElsif` | Mehrfachverzweigung mit ELSIF |
| `ifNested` | Verschachtelte IF-Blöcke |

**FOR / WHILE / REPEAT**

| Test | Prüft |
|------|--------|
| `forSimple` | FOR idx := 0 TO 10 DO |
| `forWithBy` | FOR mit BY-Schrittweite |
| `whileLoop` | WHILE-Schleife |
| `repeatUntil` | REPEAT/UNTIL-Schleife |

**CASE**

| Test | Prüft |
|------|--------|
| `caseStatement` | CASE/OF mit mehreren Labels + switch/case/break |

**RETURN / EXIT**

| Test | Prüft |
|------|--------|
| `returnStatement` | RETURN → goto __end |
| `exitStatement` | EXIT innerhalb FOR → break |

### 1.7 Funktionsbausteine (FB-Aufrufe)

| Test | Prüft |
|------|--------|
| `fbCallWithInputs` | `MyTon(IN := flag, PT := T#500ms);` |
| `fbCallWithOutputAssign` | `MyTimer(IN := flag, Q => flag);` — OUT => Zuweisung |

### 1.8 Array-Zugriffe

| Test | Prüft |
|------|--------|
| `arrayReadSubscript` | `a := arr[3];` |
| `arrayWriteSubscript` | `arr[5] := 42;` |
| `arrayComputedIndex` | `a := arr[idx + 1];` |
| `arrayInForLoop` | Array-Zugriff in FOR-Schleife |

---

## 2. Standard-Bibliothek (FStLibraryTest)

Datengetriebene Tests prüfen die Blöcke aus der
Standard-Bibliothek (`standard_library.sql`) automatisch.

### 2.1 Funktionsbausteine (13 FBs)

| Test | Prüft |
|------|--------|
| `fbSingleInstance` | Jeder FB einzeln instanziierbar und aufrufbar |
| `fbDoubleInstance` | Zwei Instanzen desselben FB-Typs gleichzeitig |
| `fbOutputRead` | Alle Ausgänge nach dem Aufruf lesbar |

**Abgedeckte FBs:** SR, RS, R_TRIG, F_TRIG, CTU, CTD, CTUD, TON, TOF, TP,
RTC, SEMA, RampGen

### 2.2 Funktionen (119 FCs)

| Test | Prüft |
|------|--------|
| `fcCall` | Jede FC mit korrekten Parametern aufrufbar (104 getestet) |
| `fcInExpression` | FC-Rückgabewert in Ausdrücken verwendbar |

**Abgedeckte Kategorien:**

- **Arithmetik:** ADD, SUB, MUL, DIV, MOD, EXPT, ABS
- **Vergleich:** EQ, NE, LT, GT, LE, GE
- **Trigonometrie:** SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2
- **Logarithmus:** EXP, LN, LOG, SQRT
- **Selektion:** SEL, MUX, LIMIT, MIN, MAX, MOVE, CLAMP
- **String:** LEN, LEFT, RIGHT, MID, CONCAT, INSERT, DELETE, REPLACE, FIND
- **Bitshift:** SHL, SHR, ROL, ROR
- **Typkonvertierung:** 60+ Konvertierungsfunktionen (BOOL_TO_INT, INT_TO_REAL, ...)
- **ForgeIEC-Erweiterungen:** LERP, MAP_RANGE, HYPOT, DEG, RAD, IK_2Link,
  CABS, CADD, CMUL, CSUB, CARG, CCONJ, CPOLAR, CRECT

---

## 3. Multi-Task-Threading (FCodeGeneratorThreadingTest)

8 Tests prüfen das vollständige Multi-Task-Scheduling-System gemäß
der Design-Spezifikation (MT-spec, docs/design/multi-task-scheduler.md).

| Test | Prüft |
|------|--------|
| `singleProgramDefaultTask` | Ein PROGRAM ohne explizite Task → DefaultTask-Synthese, kein Threading |
| `twoProgramsTwoTasks` | Zwei Tasks → RESOURCE0_start__, Legacy-Shim config_run__, beide Task-Threads |
| `crossPrimitiveAtomicEmission` | Geteilte INT-Variable → `std::atomic<>` Location-Storage, `__GET_EXTERNAL_ATOMIC` im Body |
| `crossStructuredDoubleBuffer` | Geteilter STRUCT → `__DBUF_[2]` + `thread_local __snap_` + Double-Buffer copy-in/out |
| `localVarNoSync` | Variable nur in einem Task → normales `__SET_EXTERNAL`, kein Atomic |
| `conflictTwoWriters` | Zwei Tasks schreiben dieselbe Variable → Compile-Warnung |
| `singleProgramDefaultTask` | Backward-Kompatibilität: bestehende Projekte laufen unverändert |

### Multi-Task-Architektur

```
Primary Task (Task 0)          Secondary Tasks (1..N)
    |                               |
    | config_run__()                | RESOURCE0_task_thread__()
    |   ├─ sync_in                  |   ├─ dbuf_rd (copy-in)
    |   ├─ TASK0_body__()           |   ├─ TASKn_body__()
    |   └─ sync_out                 |   └─ dbuf_wr (copy-out)
    |                               |
    | [unter bufferLock]            | [lock-free]
```

**Sync-Mechanismen:**
- **CrossPrimitive** (BOOL, INT, REAL, ...): `std::atomic<T>` auf der Location-Variable, `__GET_EXTERNAL_ATOMIC` / `__SET_EXTERNAL_ATOMIC` im Body-Code
- **CrossStructured** (STRUCT, ARRAY, STRING): Double-Buffer `__DBUF_[2]` mit atomarem Write-Index, `thread_local` Snapshots `__snap_` für Set-Konsistenz

---

