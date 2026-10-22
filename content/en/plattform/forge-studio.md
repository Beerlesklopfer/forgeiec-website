---
title: "Forge Studio"
description: "IEC 61131-3 development environment — ST today, LD/FBD/SFC in the next releases; native Qt6 interface"
weight: 1
---

## The Workbench

Forge Studio is the integrated development environment of the ForgeIEC platform.
This is where the PLC program is created — from the first draft to the finished
project. Like the workbench in a forge, Forge Studio keeps all tools within
reach: editor, compiler, debugger, and bus system configuration in a single
application.

---

## IEC 61131-3: ST today, one language per release

Structured Text is in productive use (pilot operation, release 0.2).
Each release adds one language: **0.3 LD, 0.4 FBD, 0.5 SFC**.
Programs in these languages are **not compiled yet**. 
IL (instruction list) was deprecated in IEC 61131-3 edition 3 (2013) and is no longer part of the current edition, IEC 61131-3:2025 (published May 2025). ForgeIEC does not develop it; it would also need its own translation path to assembler.
<!-- ENTWURF: Annex B der Norm einsehen, bevor es als Normaussage zitiert wird -->
See the [roadmap](/en/roadmap/).

- **Structured Text (ST)** — {{< status "use" >}} High-level language with syntax highlighting,
  auto-completion, and Tree-sitter-based parsing; own compiler core
  that also handles the object-oriented extensions (METHOD,
  INTERFACE, EXTENDS)
- **Ladder Diagram (LD)** — {{< status "plan" "planned: 0.3" >}} Familiar representation for switching logic,
  wired directly on screen
- **Function Block Diagram (FBD)** — {{< status "plan" "planned: 0.4" >}} Graphical editor with
  block library and drag-and-drop
- **Sequential Function Chart (SFC)** — {{< status "plan" "planned: 0.5" >}} Step sequence diagrams for
  sequential control with transitions and actions
- **Instruction List (IL)** — {{< status "rest" "deprecated" >}} not developed further and
  not compiled

---

## Syntax Highlighting with Tree-sitter

Forge Studio uses Tree-sitter for incremental parsing of source code.
This means:

- Precise syntax highlighting even with incomplete code
- Structural understanding of the program while typing
- Fast navigation between declarations and references
- No regular expressions — real grammar

---

## Bus System Integration

Bus system management following established IEC-61131-3 IDE conventions
is integrated directly into the development environment:

- Segment hierarchy with devices and variables in the project tree
- Automatic IEC address assignment without collisions
- Network scanner for device discovery
- Diff view for changes between editor and runtime system
- Automatic generation of the VAR_ANVIL transport layer

---

## Connection to the Runtime Environment

Forge Studio communicates via gRPC with the Anvil server (anvild):

- **Two-stage translation** — the Studio translates IEC code into
  C++ source and sends it encrypted to the controller; there the
  runtime builds it with g++ — so the controller needs `make` and
  `g++`, but no IEC compiler
- **Encrypted upload** — AES-256-GCM encrypted transfer to the
  target system
- **Live debugging** — watch and force variables in real time
  while the PLC is running
- **User management** — multi-user operation with permission system and
  industry-standard first-login workflow

---

## Standard Library

Complete IEC standard library in a SQLite database:

- Counters (CTU, CTD, CTUD)
- Timers (TON, TOF, TP)
- Edge detection blocks (R_TRIG, F_TRIG)
- Bistable elements (SR, RS)
- Type conversions and mathematical functions
- Extensible with user-defined blocks

---

## Technical Specifications

| Property | Value |
|----------|-------|
| **Language** | C++17 |
| **GUI Framework** | Qt 6 Widgets |
| **Syntax Engine** | Tree-sitter |
| **Communication** | gRPC (protobuf) |
| **Platforms** | Linux x86_64/ARM64, Windows x64 (installer on request) |
| **Licence** | AGPL-3.0-or-later (generated code: Apache-2.0) |

---

## Screens

{{< screenshot program="studio" name="editor-st" alt="ForgeIEC Studio with a Structured Text program in the editor" caption="The ST editor in the Studio's main window." >}}

{{< screenshot program="studio" name="variables" alt="Project variable list with filter bar" caption="Variables: filter by text, type, range and tag." >}}

{{< screenshot program="studio" name="library" alt="Block library with categories and documentation" caption="Library: blocks by category, search includes the documentation." >}}

{{< screenshot program="studio" name="oscilloscope" alt="Oscilloscope showing several variable traces" caption="Oscilloscope: timing, analog and normalized view." >}}

{{< screenshot program="fdd-editor" name="catalog" alt="FDD editor with a device description as a tree and an edit form" caption="The FDD editor: device descriptions as a tree, edited in a form." >}}

{{< screenshot program="studio" name="editor-sfc" alt="Sequential Function Chart (SFC) editor, planned for version 0.5" caption="Sequential Function Chart (SFC): planned for version 0.5, programs are not compiled yet." status="plan" >}}


<div style="text-align:center; padding: 2rem;">

**Forge Studio — The workbench for industrial automation.**

blacksmith@forgeiec.io

</div>
