---
title: "Open language backend: matiec → matiec++ → rustly evolution path"
date: 2026-05-14
summary: "Three IEC 61131-3 backends in parallel — in a clear order: matiec today, matiec++ next, rustly as the goal."
components: [studio]
---

{{< components "studio" >}}

## What it's about

ForgeIEC's codegen layer is not tied to a single compiler. We
separate the **language specification** (IEC 61131-3) from
the **implementation** (which compiler turns ST into machine
code) by design. The consequence: we can swap the compiler
backend without anything changing from the user's point of
view.

We use that pragmatically — not as an academic exercise. The
order is:

1. **matiec** — the established ST→C pipeline from the Beremiz
   universe. Today the default for every new ForgeIEC project.
   Documented per-construct in the new
   [IEC reference](/reference/iec61131-3/), including the
   known quirks.
2. **matiec++** — the C++ variant currently in preparation.
   Generates C++ instead of C, addressing several pain points
   of today's variant (cleaner type checks, better diagnostic
   messages, better generic handling). Plan documented in the
   internal codegen-v1 spec; sprint sequence a → a.5 → b → c
   → d → e → f.
3. **rustly** — pre-1.0 IEC compiler in Rust + LLVM. The
   strategic destination. Provides online change as a
   differentiator (matiec / matiec++ can't do that
   structurally), delivers modern diagnostic messages, and is
   the foundation for everything we want to do at compile
   time in the future (property checks, liveness analysis,
   formal verification).

**Exactly this order will be the evolution.** We don't migrate
up and down between backends; we walk along a monotonically
growing maturity chain.

## Why three backends?

Because none alone meets all three requirements:

| Requirement | matiec | matiec++ | rustly |
|---|---|---|---|
| Battle-tested in production | ✓ | (in development) | (pre-1.0) |
| IEC 61131-3 standard conformance | ✓ | ✓ | ✓ |
| Clean diagnostic messages | ✗ | (improved) | ✓ |
| Online change | ✗ | ✗ | ✓ |
| Property checks at compile | ✗ | (planned) | ✓ |
| Implementation language | C | C++ | Rust + LLVM |

We can run ForgeIEC with matiec in production today, deploy
projects with matiec++ next year and migrate to rustly in 2-3
years — without the user's ST source having to change. **ST
is the interface**; the compiler is interchangeable.

## What does that mean in practice?

- **Libraries become backend-aware**. The upcoming
  [library system](#) (`.forge_lib` file format, in planning)
  carries a backend marker per POU. A library can ship matiec,
  matiec++ and rustly implementations side-by-side; the
  consuming project picks what it needs.
- **The IEC reference is written compiler-agnostically** and
  documents matiec-specific quirks in a separate
  `matiec conformance` section per construct page. As matiec++
  and rustly land, additional conformance sections appear —
  the spec sections don't change.
- **The LLM auto-fix blocks (`llm_signals[]`)** are also
  per-backend annotated. A `where: matiec` signal doesn't fire
  when the project compiles on rustly.

## What's coming next

- Systematically build the existing matiec quirks into the
  IEC reference (already running — nine patterns documented,
  more on the way).
- Integrate the matiec++ backend as its own codegen layer in
  the editor. Sprint sequence is internal.
- Kick off the rustly evaluation as a third stream — captured
  in the memory entry `project_rusty_evaluation`.

Three backends aren't an adventure but a calm migration
strategy. What works today with matiec will work tomorrow with
matiec++ and the day after with rustly — just quieter, cleaner,
and with better tools.
