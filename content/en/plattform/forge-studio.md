---
title: "Forge Studio"
description: "IEC 61131-3 development environment — all five languages, native Qt6 interface"
weight: 1
---

## The Workbench

Forge Studio is the integrated development environment of the ForgeIEC platform.
This is where the PLC program is created — from the first draft to the finished
project. Like the workbench in a forge, Forge Studio keeps all tools within
reach: editor, compiler, debugger, and bus system configuration in a single
application.

---

## All Five IEC 61131-3 Languages

One editor for all languages — seamless switching, shared variables,
unified project structure:

- **Structured Text (ST)** — High-level language with syntax highlighting,
  auto-completion, and Tree-sitter-based parsing
- **Instruction List (IL)** — Assembly-like language with intelligent
  editing and language switching to/from ST
- **Function Block Diagram (FBD)** — Graphical editor with
  block library and drag-and-drop
- **Ladder Diagram (LD)** — Familiar representation for switching logic,
  wired directly on screen
- **Sequential Function Chart (SFC)** — Step sequence diagrams for
  sequential control with transitions and actions

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

The CoDeSys-compatible bus system management is integrated directly into
the development environment:

- Segment hierarchy with devices and variables in the project tree
- Automatic IEC address assignment without collisions
- Network scanner for device discovery
- Diff view for changes between editor and runtime system
- Automatic generation of the VAR_ANVIL transport layer

---

## Connection to the Runtime Environment

Forge Studio communicates via gRPC with the Anvil runtime environment:

- **Compilation on the workstation** — the IEC compiler (iec2c) runs
  locally, only the generated C code is transferred to the PLC
- **Encrypted upload** — AES-256-GCM encrypted transfer to the
  target system
- **Live debugging** — watch and force variables in real time
  while the PLC is running
- **User management** — multi-user operation with permission system and
  CoDeSys-compatible first login

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
| **Platforms** | Linux x86_64, ARM64 |
| **License** | Open Source |

---

<div style="text-align:center; padding: 2rem;">

**Forge Studio — The workbench for industrial automation.**

blacksmith@forgeiec.io

</div>
