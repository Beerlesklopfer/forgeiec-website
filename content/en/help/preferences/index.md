---
title: "Preferences"
summary: "Central editor configuration dialog: Editor, Runtime, PLC, AI Assistant"
---

## Overview

The **Preferences dialog** is the single entry point for all editor-global
settings — everything that is *not* part of the open project but rather
configures the editor itself, the connection to a runtime, and post-upload
behaviour.

Open the dialog through **`Edit > Preferences...`** (some themes place it
under `Tools > Preferences...` instead). Press **F1** while the dialog has
focus to open this page directly.

```
Preferences
+-- Editor          (font, tab width, line numbers)
+-- Runtime         (anvild host/port, Anvil debug, network scanner)
+-- PLC             (build mode, auto-start, persist, monitoring)
+-- AI Assistant    (LLM endpoint, tokens, temperature)
```

## Editor

Controls how text appears in the ST code editor and every other text
input field.

| Field | Meaning |
|---|---|
| **Font**         | Font family. Pre-filtered to monospaced fonts (recommended: `JetBrains Mono`, `Cascadia Code`, `Consolas`). |
| **Font size**    | Font size in points. Default `10`. |
| **Tab width**    | Number of spaces per tab stop. Default `4`. |
| **Show line numbers** | Shows running line numbers in the gutter of the code editor. |

## Runtime

Connection to an **anvild** daemon and IPC diagnostics.

| Field | Meaning |
|---|---|
| **Host**         | PLC hostname or IP. Default `localhost`. |
| **Port**         | anvild gRPC port. Default `50051`. |
| **User**         | User name for token authentication. |
| **Anvil Debug**  | IPC diagnostic level (`Off`, `Errors only`, `Verbose`). Adds extra stats to the anvild log — useful to track down Iceoryx topic drift in production. |

In addition: **Auto-Connect on start** automatically connects to the
last successfully connected anvild on editor startup — handy on a
dedicated engineering laptop.

The **Network Scanner** block on the same tab scans the LAN for Modbus
TCP devices (port 502) and ForgeIEC runtimes (port 50051) and inserts
hits into the bus configuration.

## PLC

Controls what happens after an **Upload** to the PLC.

| Field | Meaning |
|---|---|
| **Compile Mode** | `Development` (live monitoring + forcing enabled) or `Production` (stripped binary, no debug bridges — security boundary). |
| **PLC autostart**| Automatically starts the PLC runtime after a successful upload, skipping the confirmation dialog. |
| **Persist enabled** | Enables periodic persistence of `VAR_PERSIST`/`RETAIN` variables to `/var/lib/anvil/persistent.dat`. Values survive a runtime restart. |
| **Persist polling interval** | Seconds between automatic save passes (default `5 s`). |
| **Monitor history** | Number of samples per variable in the oscilloscope recorder (default `1000`). |
| **Monitor interval**| Sample interval in milliseconds for live monitoring (default `100 ms`). |

## Library

Sync behaviour for the standard library between the editor resource and
the PLC-side library path — see [Library](../library/) for the full
drift model. Two modes:

  - **Auto-Push off** (default) — on connect the editor only logs a
    hint in the Output panel when drift is detected. Push happens
    manually via `Tools > Sync Library`.
  - **Auto-Push on** — on every detected drift the editor pushes its
    local library version automatically. Useful in a single-programmer
    setup.

## AI Assistant

Optional code completion against a local OpenAI-compatible LLM server
(LM Studio, Ollama, llama.cpp, vLLM).

| Field | Meaning |
|---|---|
| **Enable AI Assistant** | Toggles inline completion. |
| **API Endpoint**        | OpenAI-compatible endpoint, e.g. `http://localhost:1234/v1`. |
| **Max Tokens**          | Per-request response limit. Default `2048`. |
| **Temperature**         | `Precise (0.1)`, `Balanced (0.3)`, `Creative (0.7)`, `Wild (1.0)`. |

## UX state (auto-persisted)

The following fields are stored in the background **without** going
through the Preferences dialog, so the editor reopens in the exact
state in which you left it:

  - Window geometry + window state (`windowGeometry`, `windowState`)
  - Splitter and header positions (`splitterState`, `headerState`)
  - Output panel height (`outputPanelHeight`)
  - Last opened project (`lastProject`) and the recent-files list
  - Session state: open POU tabs, active tab, cursor and scroll
    position per POU

## Settings storage

Settings are stored via Qt's `QSettings`, platform-specific:

| Platform | Path |
|---|---|
| **Windows** | Registry: `HKCU\Software\ForgeIEC\ForgeIEC Studio` |
| **Linux**   | `~/.config/ForgeIEC/ForgeIEC Studio.conf` |
| **macOS**   | `~/Library/Preferences/io.forgeiec.studio.plist` |

Deleting that file / registry key resets all settings to default —
useful after a botched upgrade.

## Planned extensions

Backlog (cluster R phase 3): the Output panel will get its own severity
colours (error red, warning yellow, info white) and a configurable font
size. Both options will then appear here on a new `Output` tab.

## Related topics

  - [Library](../library/) — sync behaviour between editor and runtime.
  - [Bus configuration](../bus-config/) — project-scoped settings that
    do *not* live here but on the bus segment / device itself.
