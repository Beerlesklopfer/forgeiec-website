---
title: "IEC 61131-3"
summary: "ForgeIEC's IEC 61131-3 dialect — every construct, with the IEC definition, the matiec implementation, and an LLM auto-fix block."
weight: 10
---

## IEC 61131-3 in ForgeIEC

ForgeIEC implements [IEC 61131-3 third edition (2013)](https://en.wikipedia.org/wiki/IEC_61131-3),
the international standard for PLC programming languages. The
ForgeIEC editor compiles ST and IL through **matiec** today, with
a [matiec++](#) and [rustly](#) backend in preparation. This
section documents every construct of the language with the
following layout:

1. **Definition** — the IEC standard's wording, paraphrased for
   beginners. One construct per page.
2. **Syntax** — the formal grammar plus a runnable example.
3. **Semantics** — what happens at run-time on the PLC.
4. **IEC reference** — chapter and section number in the standard.
5. **matiec conformance** — what the matiec compiler actually
   does with this construct, including known quirks and emit-bugs
   that an LLM should be aware of.
6. **ForgeIEC notes** — Anvil/Bellows namespace rules, pool-
   resolver behaviour, and editor integration.
7. **LLM auto-fix block** — every page carries an `llm_signals`
   array in its front-matter that maps a compiler error pattern
   to a remediation strategy. An LLM that hits a compile error
   greps these blocks for a matching `error_pattern` and applies
   the prescribed `fix_strategy` automatically.

---

## Chapter map

This index follows the chapter ordering of the IEC 61131-3 third
edition. The standard splits into "common elements" (lexical, data,
variables, POU model) and per-language chapters (ST, IL, LD, FBD,
SFC) plus the standard library of functions and FBs. ForgeIEC's
day-to-day weight is on **Structured Text**, so that branch is
the deepest; the other languages are documented at the level
needed to round-trip their constructs through the editor.

### [Common elements](common/)

Whitespace, identifiers, comments, literals, data types,
variables, POU model, [object-oriented extensions](common/object-oriented/),
configuration / resources / tasks.

### Programming languages

IEC 61131-3 groups the five PLC languages into three families. Each
family has its own sub-section here:

- **[Textual](textual/)** — [Structured Text (ST)](textual/structured-text/)
  and [Instruction List (IL)](textual/instruction-list/). ST is the
  default language for new POUs in ForgeIEC; most operator-facing
  diagnostic patterns and most LLM auto-fix recipes live there. IL
  is deprecated in the 2013 edition but matiec still accepts it.
- **[Graphical](graphical/)** — [Ladder Diagram (LD)](graphical/ladder-diagram/)
  and [Function Block Diagram (FBD)](graphical/function-block-diagram/).
  The editor exposes both as graph editors; the persisted form is
  PLCopen XML.
- **[Structured](structured/)** — [Sequential Function Chart (SFC)](structured/sequential-function-chart/),
  the orthogonal step-and-transition language that can host any of
  the four other languages inside its actions.

### [Standard Library](standard-library/)

Built-in functions (type-conversion, arithmetic, comparison,
selection, string, bit) and built-in function blocks (TON,
TOF, TP, CTU, CTD, CTUD, R_TRIG, F_TRIG, RS, SR).

---

## How to use the LLM auto-fix block

Each page's front-matter ends with an `llm_signals` array of the
form:

```yaml
llm_signals:
  - error_pattern: "Unexpected token: '01'"
    where: "FStCompiler"
    diagnosis: "matiec rejects hexadecimal literals (16#xx) inside CASE-OF case lists; it parses 16# as the BYTE type-prefix and then chokes on the digits."
    fix_strategy: "Replace 16#xx hex literals with their decimal equivalents (16#01 → 1, 16#02 → 2, 16#04 → 4, …)."
    fix_example: |
      (* before — fails: Unexpected token: '01' *)
      CASE iStep OF
          0: bMask := 16#01;
          1: bMask := 16#02;
      END_CASE;

      (* after — compiles *)
      CASE iStep OF
          0: bMask := 1;
          1: bMask := 2;
      END_CASE;
```

A consuming LLM (the ForgeIEC MCP `forge.help_for` call, the
chat-tab assistant, or an external IDE plug-in) walks the pages,
collects `llm_signals[].error_pattern` strings, and matches them
against the live compiler output. On a match, the page's
`fix_strategy` + `fix_example` is the actionable response. The
patterns are intentionally substring-matchable; complex regex is
allowed but discouraged.

The `where` field constrains the matcher to a layer:

| `where` value | Matches errors from |
|---|---|
| `FStCompiler` | the local ForgeIEC ST front-end (compile button) |
| `matiec` | matiec's ST→C translator (deploy stage) |
| `gcc` | the PLC-side g++ compile pass |
| `linker` | g++ link stage on the PLC |
| `runtime` | anvild / forgeiec-plc runtime errors at scan time |

When the same construct can fire at multiple layers, list one
`llm_signals` entry per layer so the matcher can disambiguate.
