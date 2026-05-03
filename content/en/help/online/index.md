---
title: "Online Help"
summary: "Entry point for context-sensitive help from the ForgeIEC editor"
---

## Online Help — What is it?

The online help is the context-sensitive help layer of the ForgeIEC
editor. Pressing **F1** in the editor opens your browser directly on the
help page for the currently focused element (dialog, panel, variable
table, codegen action, ...).

## URL scheme

All help pages live under a uniform scheme:

```
https://forgeiec.io/<language>/help/<topic>/
```

- `<language>` follows the editor locale (de, en, fr, es, ja, tr, zh, ar);
  defaults to `de` when no localized page exists
- `<topic>` is a slug that is the same across languages and not translated

So you can open a help page directly in your browser without launching
the editor.

## Available topics

### Editor & languages

- [Structured Text (ST)](/en/help/st/) — ST editor + language foundations, bit access, qualified pool references
- [Instruction List (IL)](/en/help/il/) — accumulator-based IEC language with CR register
- [Function Block Diagram (FBD)](/en/help/fbd/) — graphical wiring of functions, function blocks and variables
- [Ladder Diagram (LD)](/en/help/ld/) — power-rail metaphor: contacts and coils
- [Sequential Function Chart (SFC)](/en/help/sfc/) — step-transition model for sequencers and mode machines

### Model & variables

- [Variables management](/en/help/variables/) — the Variables panel as central view onto the FAddressPool: columns, filters, bulk operations, safety switches
- [Library](/en/help/library/) — IEC 61131-3 standard library + ForgeIEC extensions + user-defined blocks
- [Properties panel](/en/help/properties-panel/) — inline editor for the bus element selected in the Project tree
- [Preferences](/en/help/preferences/) — central configuration dialog: editor, runtime, PLC, AI Assistant

### Bus & hardware

- [Bus configuration](/en/help/bus-config/) — PLCopen XML schema for industrial fieldbus configuration

### Project

- [Project file format (.forge)](/en/help/file-format/) — anatomy of a ForgeIEC project file: PLCopen XML with ForgeIEC extensions

### General

- [Test coverage](/en/help/tests/) — 117 automated tests for the IEC language feature set, standard blocks and multi-task threading
- [Open Source philosophy](/en/help/open-source/) — background: more than software, a societal idea

## In the editor

- **F1** on a focused element → context-sensitive help page
- **Help → Online Help** in the main menu → entry point (this page)
- **Help → About ForgeIEC** → version info + license
