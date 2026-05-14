---
title: "IEC-Standard-Library als Lern-Referenz mit LLM-Auto-Fix"
date: 2026-05-14
summary: "Jede Funktion und jeder Funktionsbaustein der IEC 61131-3 mit Lehrbuch-Erklaerung, matiec-Quirks und einem maschinenlesbaren Auto-Fix-Block fuer den AI-Assistenten."
components: [studio]
---

{{< components "studio" >}}

## Worum es geht

PLC-Programmierer haben es bis heute mit zwei sehr unterschiedlichen
Lernpfaden zu tun. Anfaenger wollen verstehen **wie ein Timer
ueberhaupt funktioniert** (was ist `IN`, was ist `PT`, warum muss
ich eine Instanz deklarieren?). Profis wollen **die exakte
Spec-Konformitaet nachschlagen** (welche Operatoren akzeptiert
matiec? Wie verhaelt sich `MOD` bei negativen Operanden?). Und
ein LLM-Assistent will **eine Compiler-Fehlermeldung in eine
ausfuehrbare Korrektur uebersetzen** ohne zu raten.

Auf forgeiec.io gibt es jetzt eine
[IEC 61131-3 Reference](/reference/iec61131-3/), die alle drei
Zielgruppen parallel bedient.

## Was bisher live ist

Erste Welle, Stand 2026-05-14:

- **Strukturierter Aufbau**: 3 Sprachfamilien als Top-Level
  ([Textual](/reference/iec61131-3/textual/) — ST + IL,
  [Graphical](/reference/iec61131-3/graphical/) — LD + FBD,
  [Structured](/reference/iec61131-3/structured/) — SFC) plus
  [Common Elements](/reference/iec61131-3/common/) und
  [Standard Library](/reference/iec61131-3/standard-library/).
- **ST Control Flow** voll dokumentiert:
  [`IF` / `ELSIF` / `ELSE`](/reference/iec61131-3/textual/structured-text/control-flow/if-statement/),
  [`CASE`](/reference/iec61131-3/textual/structured-text/control-flow/case-statement/).
- **Function & FB calls** mit zwei Tiefenartikeln:
  [FB-Instanz vs. Function-Call](/reference/iec61131-3/textual/structured-text/function-calls/fb-instance-vs-function/)
  und [Positional vs. Named Parameters](/reference/iec61131-3/textual/structured-text/function-calls/positional-vs-named/).
- **Standard Library**: erster vollstaendiger Funktionsbaustein
  [TON — Timer-On-Delay](/reference/iec61131-3/standard-library/function-blocks/ton/)
  mit Pin-Layout, Beispielen, Semantik und Reihe von Auto-Fix-Eintraegen.
- **Literals**: [Integer & Hexadecimal](/reference/iec61131-3/textual/structured-text/literals/integer-literals/)
  inklusive der zwei matiec-Quirks die uns am 2026-05-14 in der
  Ackersteuerung den Tag gekostet haben.

## Das Auto-Fix-Block-Schema

Jede Konstrukt-Seite traegt im Frontmatter einen
`llm_signals[]`-Block. Format:

```yaml
llm_signals:
  - error_pattern: "<substring oder regex aus dem Compiler-stderr>"
    where: FStCompiler | matiec | gcc | linker | runtime
    diagnosis: "<warum dieser Fehler feuert>"
    fix_strategy: "<was zu tun ist>"
    fix_example: |
      (* before *) ...
      (* after  *) ...
```

Ein konsumierender LLM (der ForgeIEC-MCP-Tool `forge.help_for`,
der Chat-Tab-Assistent oder ein externes IDE-Plug-in) walked
die Pages, sammelt die `error_pattern`-Strings und matched gegen
die Live-Compiler-Ausgabe. Match → die Page's `fix_strategy` +
`fix_example` ist die actionable Antwort. Damit wird aus
„Fehler XYZ in POU PLC_PRG, Zeile 17" eine konkrete
`set_text_body`-Operation — ohne Raten.

Das `where`-Feld constraint den Matcher auf eine Compiler-
Schicht (lokaler ST-Frontend, matiec, g++ auf der PLC, Linker,
Runtime). Damit kann derselbe Konstrukt mehrfach auftauchen mit
verschiedenen Fix-Strategien je nachdem, wo der Fehler feuert.

## Echte Quirks aus echten Projekten

Die ersten neun dokumentierten `error_pattern`-Eintraege kommen
**alle aus dem Ackersteuerung-Cleanup vom 2026-05-14** — nichts
ist erfunden. Beispiele:

- `Unexpected token: '01'` bei `16#xx` in `CASE`-Labels —
  matiec-Lexer parst `16#` als Type-Prefix und scheitert an den
  Hex-Ziffern. Workaround: dezimale Labels.
- `'BYTE' has no member named 'BYTE'` beim g++-Compile auf der
  PLC — matiec emittiert `data__->BYTE` statt einer
  Literal-Konversion fuer `SHL(BYTE#1, …)`. Workaround:
  vorberechnen oder `INT_TO_BYTE(1)` benutzen.
- `is a Function Block — declare instance first` — der
  Klassiker fuer LLMs, die `TON(IN:=x, PT:=t)` direkt aufrufen
  wollen. Fix: erst Instanz deklarieren, dann die Instanz
  aufrufen.

## Was als naechstes kommt

Der Reference-Sprint laeuft ueber mehrere Sessions. Roadmap:

- Weitere Standard-FBs (CTU, R_TRIG, RS, TOF, TP, …) nach dem
  TON-Muster.
- Operatoren-Tabelle (arithmetic / bitwise / comparison /
  assignment + precedence).
- Iteration (`FOR`, `WHILE`, `REPEAT`).
- Common Elements: Datentypen + Variablen-Scopes mit ForgeIEC's
  Anvil/Bellows/GVL-Spezifika.
- Variables & References: Anvil/Bellows-Namespacing,
  Pool-Resolver-Regeln.

Wenn dir ein Konstrukt fehlt, das du gerade brauchst — sag
Bescheid und es springt in die Prio-Liste.
