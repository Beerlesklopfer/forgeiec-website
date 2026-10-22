---
title: "From the first byte: the ForgeIEC story"
date: 2026-05-13
weight: 1
summary: "How a fork of OpenPLC became an independent IEC 61131-3 platform — and why"
components: [studio, anvild, tongs]
---

{{< components "studio,anvild,tongs" >}}

{{< callout type="note" title="Revised in October 2026" >}}
This post describes the state of May 2026. In October 2026 it was
brought up to date: matiec has been replaced, the security figures
are unified, and the origin is described without a year.
{{< /callout >}}

## The beginning — a fork of OpenPLC

ForgeIEC started as a **fork of OpenPLC** — the open PLC runtime by
**Thiago Alves** and its contributors, written in C/C++ with a
web-based configuration UI in Python/Flask.
<!-- ENTWURF: Year of the fork open — git shows the author's own work only from February 2026 (audit W-17); the owner says 2018. No year until there is evidence. -->

OpenPLC offers a clear value: you can run IEC 61131-3 code on
regular Linux hardware, without a commercial editor licence,
without vendor lock-in. Modbus master, GPIO, Raspberry Pi
support — all there.

What OpenPLC does not have: a serious **editor**. The web UI is
fine for small projects, but at industrial complexity it falls
behind.

OpenPLC continues to be developed by its community; ForgeIEC takes
over that foundation and builds on it. ForgeIEC has since replaced
the matiec compiler with an **own, object-oriented-capable core**
that translates ST into C++ and also handles METHOD, INTERFACE and
EXTENDS.

---

## 2026-03-01: The big rebuild begins

With commit `82780f7`
on **1 March 2026** the next step arrives: a **standalone C++/Qt6
editor** is introduced into the repository. Native desktop
application, no browser, no Python/Flask in the UI path anymore.

Same day, the next chunk: **gRPC client in the editor**, plus the
backend is renamed to `forgeiecd` (commit `93ed9c9`).
The old HTTP web server gives way to a modern **gRPC pipeline**
with streaming + protocol versioning.

The next days move fast:

- **3 March** — bus system, model/view refactor, F-prefix renames
  (commit `dd85396`)
- **4 March** — EtherCAT + Profibus bridges, CMake migration
- **5 March** — Hugo website added as submodule
- **6 March** — **DEL → Anvil**: the shared-memory IPC subsystem
  gets its industrial name (commit `3fc636c`)
- **7 March** — **Forge Studio branding**, bridge family renamed
  `anvil-*`, dirty-bit management, BusModel MVC

In **one week** a web-UI toolbox turns into a **standalone
desktop editor with modern architecture**.

---

## March–April 2026: the architecture consolidates

Several weeks of deep refactor work follow:

- **Debian packages + CPack** (26 March) — no more manual install
  script
- **Multi-task scheduler** (11 April) — IEC tasks now really run
  in parallel, pthread-based
- **Bus-panel merge** (13 April) — separated views on the same
  model unified
- **-1416 LOC refactor** (16 April) — FBusDeviceDialog removed,
  bus columns consolidated
- **`FVariableBase` + `FLocatedVariable` → `FVariable`** (26 April)
  — the central variable type is unified

Here happens what you as a user **don't** see: the **data model**
is rebuilt to carry real industrial complexity. `FAddressPool` as
single source of truth, pool variables as the only container,
old POU varlists only as mirrors.

This is the foundation that lets the AI layer operate reliably
later — it sees a **consistent model**, not a collection of
legacy data structures.

---

## May 2026: security + AI

With the data model stable, the big-ticket sprints can land:

- **2 May** — **per-variable safety flags** (cluster A): force,
  monitor, HMI export gated individually per variable. This later
  becomes the force lock: locked three times — in codegen, in the
  runtime and in the editor; for the AI a fourth lock in the MCP
  server is added.
- **8 May** — **MCP platform**: spec written, sprint MCP-1
  (prompts in QSettings).
- **9 May** — **live diagnostic pipeline** — FB-member resolution,
  FLiveValueStore lifecycle fix.
- **10 May** — **headless mode + devloop CLI** — for CI/build
  servers. `codegen.deploy` becomes scriptable.
- **11 May** — **MCP-3.6**: chat tab becomes internal MCP client.
- **12 May** — **MCP-4a + 4b phases A–D**: remote bind, bearer
  auth, trust store, mTLS, Caretaker model.

That completes the **technical leap**: ForgeIEC is no longer just
an open IEC 61131-3 editor but a **platform of its own** with
federation, AI integration and verifiable security layers.

---

## Today, 13 May 2026: where we stand

The platform is split into seven building blocks, each with its own spec
in the `documentation/architecture/` directory of the source
tree:

| Subsystem | Spec | Role |
|---|---|---|
| **ForgeIEC Studio** | `mcp-platform-v1.md` | IDE — editor + AI assistant + MCP server |
| **Anvil server (anvild)** | `anvil-platform-v2.md` | PLC runtime + plug-in platform + online change |
| **Anvil (IPC)** | (in anvil-platform-v2 §13) | Zero-copy shared memory between subsystems |
| **tongs-* (bridges)** | `tongs-platform-v1.md` | Fieldbus plug-ins with fault model + FDD diag bits |
| **Bus system** | `bus-system-v1.md` | Segments/devices/IEC access |
| **Editor data model** | `editor-data-v1.md` | FAddressPool SSoT + .forge format |
| **Codegen** | `codegen-v1.md` | own ST core → C++ |

All specs RFC 2119 normative. Code + spec move together — every
change passes through the same review process.

---

## What ForgeIEC does differently

| Others | ForgeIEC |
|---|---|
| Proprietary PLC IDEs | AGPL-3.0-or-later; your project (generated code, runtime API, libanvil) under Apache-2.0 |
| Vendor lock-in for devices | Manufacturer FDDs as first-class citizens |
| AI only as a code-completion plug-in | AI as an equal MCP client with audit log |
| Force settings without protection layer | Force locked three times (codegen, runtime, editor), a fourth lock for the AI |
| Monolithic runtime | Modular bridge family with separate daemons |
| Closed-source binaries | Signed packages from an automated CI; source code on request |

---

## Where it's going

On the sprint plan:

- **Caretaker toggle UI** in Preferences — today still QSettings
  editing
- **`team.revoke_peer` fully**, `team.rotate_cert`,
  `team.export_setup` — last third of MCP-4b phase D
- **Anvil platform v2**: online change during a running PLC cycle,
  plug-in architecture for custom boundary types
<!-- ENTWURF: The May plan listed a migration of code generation to Rust+LLVM (rusty) here. Whether that is still planned is the owner's decision (audit W-16); not mentioned until then. -->
- **Hearth** — the operator interface; available today as a preview
  over the Anvil bus
- **Tongs LoRaWAN** (focus), then **Tongs EtherCAT, Tongs
  Profibus, Tongs EtherNet/IP** fully implemented

The common thread: **an open, honest platform** that can handle
industrial reality — no marketing varnish, but load-bearing
architecture decisions that live in the spec and are
verifiable in the source code (access on request).

---

## Read on

- [Architecture + Security](/en/help/ai/architecture/) — the depth
  tour for auditors
- [Download](/en/download/) — all components via the APT repository
- Source tree: `ForgeIEC/forgeiec-studio` in the Forgejo — access
  once your SSH public key is enabled
- Earliest roots:
  [OpenPLC by Thiago Alves](https://www.openplcproject.com/) —
  where it all began
