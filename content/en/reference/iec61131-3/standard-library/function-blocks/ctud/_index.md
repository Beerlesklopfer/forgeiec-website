---
title: "CTUD — Counter Up/Down"
summary: "Bidirectional counter — combines CTU and CTD in one FB."
weight: 38
iec_chapter: "Annex F.6.3"
construct_kind: "function-block"
keywords: ["CTUD", "counter", "up", "down", "CU", "CD", "QU", "QD"]
---

## Pin layout

| Direction | Name | Type | Description |
|---|---|---|---|
| Input | `CU` | `BOOL` | Count Up — increment on rising edge |
| Input | `CD` | `BOOL` | Count Down — decrement on rising edge |
| Input | `R` | `BOOL` | Reset — when TRUE, CV := 0 (priority over LD) |
| Input | `LD` | `BOOL` | Load — when TRUE, CV := PV |
| Input | `PV` | `INT` | Preset Value used by both LD and QU |
| Output | `QU` | `BOOL` | TRUE when CV >= PV |
| Output | `QD` | `BOOL` | TRUE when CV <= 0 |
| Output | `CV` | `INT` | Current Value |

## Semantics

```text
R = TRUE              : CV := 0    (priority)
LD = TRUE             : CV := PV
CU rising and not R/LD: CV := CV + 1
CD rising and not R/LD: CV := CV - 1
QU := CV >= PV
QD := CV <= 0
```

If CU and CD both rise on the same scan, matiec applies CU
first then CD — net effect is no change. Don't rely on this
ordering across other implementations.

## Example

```iec-st
VAR
    netCount : CTUD;
END_VAR

netCount(CU := xUp,
         CD := xDown,
         R  := xReset,
         LD := xLoad,
         PV := 100);

iCurrent := netCount.CV;
xAtTop   := netCount.QU;
xAtBottom := netCount.QD;
```

## IEC reference

IEC 61131-3 third edition (2013), Annex F.6.3.

## matiec conformance

Implemented per the standard.
