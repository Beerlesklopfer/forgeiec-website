---
title: "IEC standard library as a learning reference with LLM auto-fix"
date: 2026-05-14
summary: "Every IEC 61131-3 function and function block with a textbook explanation, the matiec quirks, and a machine-readable auto-fix block for the AI assistant."
components: [studio]
---

{{< components "studio" >}}

## What it's about

PLC programmers face two very different learning paths even
today. Beginners want to understand **how a timer actually
works** (what is `IN`, what is `PT`, why do I have to declare
an instance?). Professionals want **the exact spec conformance**
(which operators does matiec accept? how does `MOD` behave on
negative operands?). And an LLM assistant wants to **translate
a compiler error message into an executable fix** without
guessing.

forgeiec.io now hosts an
[IEC 61131-3 reference](/reference/iec61131-3/) that serves
all three audiences in parallel.

## What's live in the first wave

As of 2026-05-14:

- **Structured layout**: 3 language families as top-level
  ([Textual](/reference/iec61131-3/textual/) — ST + IL,
  [Graphical](/reference/iec61131-3/graphical/) — LD + FBD,
  [Structured](/reference/iec61131-3/structured/) — SFC) plus
  [Common Elements](/reference/iec61131-3/common/) and
  [Standard Library](/reference/iec61131-3/standard-library/).
- **ST control flow** documented in full:
  [`IF` / `ELSIF` / `ELSE`](/reference/iec61131-3/textual/structured-text/control-flow/if-statement/),
  [`CASE`](/reference/iec61131-3/textual/structured-text/control-flow/case-statement/).
- **Function & FB calls**, two deep-dive pages:
  [FB instances vs. function calls](/reference/iec61131-3/textual/structured-text/function-calls/fb-instance-vs-function/)
  and [Positional vs. named parameters](/reference/iec61131-3/textual/structured-text/function-calls/positional-vs-named/).
- **Standard library**: first complete function block
  [TON — timer-on-delay](/reference/iec61131-3/standard-library/function-blocks/ton/)
  with pin layout, examples, semantics and a row of auto-fix
  signals.
- **Literals**: [Integer & hexadecimal](/reference/iec61131-3/textual/structured-text/literals/integer-literals/)
  including the two matiec quirks that cost us the morning of
  2026-05-14 in the Ackersteuerung project.

## The auto-fix block schema

Every page carries an `llm_signals[]` block in its front-matter:

```yaml
llm_signals:
  - error_pattern: "<substring or regex from compiler stderr>"
    where: FStCompiler | matiec | gcc | linker | runtime
    diagnosis: "<why this fires>"
    fix_strategy: "<what to do>"
    fix_example: |
      (* before *) ...
      (* after  *) ...
```

A consuming LLM (the ForgeIEC MCP `forge.help_for` tool, the
chat-tab assistant, or an external IDE plug-in) walks the
pages, collects the `error_pattern` strings, and matches them
against the live compiler output. On a match, the page's
`fix_strategy` + `fix_example` is the actionable answer. That
turns "error XYZ in POU PLC_PRG, line 17" into a concrete
`set_text_body` call — without guessing.

The `where` field constrains the matcher to a compiler layer
(local ST front-end, matiec, g++ on the PLC, linker, runtime).
The same construct can therefore appear with different fix
strategies depending on which layer fired the error.

## Real quirks from real projects

The first nine documented `error_pattern` entries **all come
from the 2026-05-14 Ackersteuerung cleanup** — none of them
are invented. Highlights:

- `Unexpected token: '01'` for `16#xx` in `CASE` labels —
  matiec's lexer parses `16#` as a type prefix and chokes on
  the hex digits. Workaround: decimal labels.
- `'BYTE' has no member named 'BYTE'` during g++ compile on
  the PLC — matiec emits `data__->BYTE` instead of an integer
  literal cast for `SHL(BYTE#1, …)`. Workaround: pre-compute
  the value or use `INT_TO_BYTE(1)`.
- `is a Function Block — declare instance first` — the
  classic LLM trap of calling `TON(IN:=x, PT:=t)` directly.
  Fix: declare an instance, then call the instance.

## What's coming next

The reference sprint runs over multiple sessions. Roadmap:

- More standard FBs (CTU, R_TRIG, RS, TOF, TP, …) following the
  TON template.
- Operator tables (arithmetic / bitwise / comparison /
  assignment + precedence).
- Iteration (`FOR`, `WHILE`, `REPEAT`).
- Common Elements: data types + variable scopes including
  ForgeIEC's Anvil/Bellows/GVL specifics.
- Variables & references: Anvil/Bellows namespacing, pool
  resolver rules.

If a construct you need is missing, say so and it jumps to the
top of the list.
