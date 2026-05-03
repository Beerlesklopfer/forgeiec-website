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

The main topics are listed in the [Help overview](/help/).

## In the editor

- **F1** on a focused element → context-sensitive help page
- **Help → Online Help** in the main menu → entry point (this page)
- **Help → About ForgeIEC** → version info + license
