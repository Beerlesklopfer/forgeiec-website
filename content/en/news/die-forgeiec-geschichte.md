---
title: "From the first byte: the ForgeIEC story"
date: 2026-05-13
weight: 1
summary: "How an OpenPLC fork became an independent IEC 61131-3 platform — and why"
components: [studio, anvild, bellowsd, tongs]
---

{{< components "studio,anvild,bellowsd,tongs" >}}

## 2018: The beginning — OpenPLC

The first commit in this repository is dated **14 June 2018**.
Back then the project is not called ForgeIEC but **OpenPLC v3
beta 1** — an open PLC runtime by **Thiago Alves**, written in
C/C++ with a web-based configuration UI in Python/Flask.

OpenPLC offers a clear value: you can run IEC 61131-3 code
(Structured Text + the four other languages) on regular Linux
hardware, without a CoDeSys licence, without vendor lock-in.
That was revolutionary. Modbus master, GPIO, Raspberry Pi
support — all there.

What OpenPLC does not have: a serious **editor**. The web UI is
fine for small projects, but at industrial complexity it falls
behind.

---

## 2019–2024: The latency years

Between 2019 and early 2025 not much happens: small bug fixes
(Modbus buffer overflow, libmodbus fork, web-server tweaks),
but no big leap. That is the reality of open-source projects —
as long as nobody invests, it stagnates.

In those years we learn: **the foundation holds**. The matiec
compiler toolchain is solid, the IEC code generator works, the
runtime runs reliably on x86 + ARM. What is missing is everything
**around** it — editor, bus system, diagnostic tools,
manufacturer-data integration.

---

## 2026-03-01: The big rebuild begins

With commit
[`82780f7`](https://git.forgeiec.io/ForgeIEC/forgeiec-studio/commit/82780f7)
on **1 March 2026** the next step arrives: a **standalone C++/Qt6
editor** is introduced into the repository. Native desktop
application, no browser, no Python/Flask in the UI path anymore.

Same day, the next chunk: **gRPC client in the editor**, plus the
backend is renamed to `forgeiecd` (commit
[`93ed9c9`](https://git.forgeiec.io/ForgeIEC/forgeiec-studio/commit/93ed9c9)).
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
  monitor, HMI export gated individually per variable. Later
  this becomes the 3-layer security architecture.
- **8 May** — **MCP platform**: spec written, sprint MCP-1
  (prompts in QSettings).
- **9 May** — **live diagnostic pipeline** — FB-member resolution,
  FLiveValueStore lifecycle fix.
- **10 May** — **headless mode + devloop CLI** — for CI/build
  servers. `codegen.deploy` becomes scriptable.
- **11 May** — **MCP-3.6**: chat tab becomes internal MCP client.
- **12 May** — **MCP-4a + 4b phases A–D**: remote bind, bearer
  auth, trust store, mTLS, Caretaker model.

That completes the **technical leap**: ForgeIEC is no longer a
"better CoDeSys" but a **platform of its own** with federation,
AI integration and verifiable security layers.

---

## Today, 13 May 2026: where we stand

The platform is split into subsystems, each with its own spec
in the
[`documentation/architecture/`](https://github.com/Beerlesklopfer/ForgeIEC-Studio/tree/development/documentation/architecture)
directory:

| Subsystem | Spec | Role |
|---|---|---|
| **ForgeIEC Studio** | `mcp-platform-v1.md` | IDE — editor + AI assistant + MCP server |
| **anvild** | `anvil-platform-v2.md` | PLC runtime + plug-in platform + online change |
| **Anvil (IPC)** | (in anvil-platform-v2 §13) | Zero-copy shared memory between subsystems |
| **tongs-* (bridges)** | `tongs-platform-v1.md` | Fieldbus plug-ins with fault model + FDD diag bits |
| **Bus system** | `bus-system-v1.md` | Segments/devices/IEC access |
| **Editor data model** | `editor-data-v1.md` | FAddressPool SSoT + .forge format |
| **Codegen** | `codegen-v1.md` | C output + matiec interop |

All specs RFC 2119 normative. Code + spec move together — every
change passes through the same review process.

---

## What ForgeIEC does differently

| Others | ForgeIEC |
|---|---|
| Proprietary PLC IDEs | Fully open source (AGPL-3.0) |
| Vendor lock-in for devices | Manufacturer FDDs as first-class citizens |
| AI only as a code-completion plug-in | AI as an equal MCP client with audit log |
| Force settings without protection layer | 4-layer defence per variable |
| Monolithic runtime | Modular bridge family with separate daemons |
| Closed-source binaries | Build from source reproducible, signed via APT |

---

## Where it's going

On the sprint plan:

- **Caretaker toggle UI** in Preferences — today still QSettings
  editing
- **`team.revoke_peer` fully**, `team.rotate_cert`,
  `team.export_setup` — last third of MCP-4b phase D
- **Anvil platform v2**: online change during a running PLC cycle,
  plug-in architecture for custom boundary types
- **Codegen v1 → v2**: migration of C code generation to
  Rust+LLVM (rusty backend) — determinism guarantees + online-
  change preparation
- **Hearth** — the next subsystem block for IIoT subscribers
  (Mosquitto cloud, time-series DB)
- **Tongs EtherCAT, Tongs Profibus, Tongs EtherNet/IP** fully
  implemented

The common thread: **an open, honest platform** that can handle
industrial reality — no marketing varnish, but load-bearing
architecture decisions that live in the spec and are
verifiable in the source.

---

## Read on

- [Architecture + Security](/help/ai/architecture/) — the depth
  tour for auditors
- [Download](/download/) — all components via the APT repository
- [Source tree](https://github.com/Beerlesklopfer/ForgeIEC-Studio)
- Earliest roots:
  [Thiago Alves' OpenPLC v3](https://www.openplcproject.com/) —
  where it all began
