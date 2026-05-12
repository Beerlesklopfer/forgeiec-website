---
title: "Partners"
summary: "Who's helping build — and which areas we are looking for contributors"
---

## Who fits a partnership

ForgeIEC does not grow through marketing agreements but through
people who bring **code, hardware, or practical knowledge**. We
look for partners with demonstrable open-source engagement and
concrete contributions to one of the subsystems.

| Criterion | What we want to see |
|---|---|
| **Demonstrable OSS contributions** | Commits / PRs / bug reports in existing projects — not just usage |
| **Public profile** | GitHub, GitLab, Codeberg, Forgejo — any hosting |
| **Domain expertise** | Industrial automation, fieldbuses, IEC 61131-3, embedded systems, or related |
| **Long-term perspective** | Platform building is a marathon — we are not looking for short engagements |

Open source as a marketing label without code contribution does
**not** fit our model.

---

## Areas where we are looking for contributors

### 🔧 Bus bridges (tongs-*)

{{< components "tongs,anvild" >}}

- **tongs-ethercat** — DC sync, slave state machine, ENI XML import
- **tongs-profibus** — DP master, GSD import toolchain
- **tongs-ethernetip** — CIP connections, EDS import
- **tongs-can** — CANopen + J1939

If you know one of these stacks well — ideal spot. Skeleton +
fault model + IPC wire format are in place; the protocol-specific
part is missing.

### 🛠️ Studio editor features

{{< components "studio" >}}

- **FBD/LD/SFC editors** — today the focus is on ST. Graphical
  languages need their own tree-sitter grammars + canvas renderers.
- **Vendor catalog** — FDDs for more manufacturers (today:
  Weidmueller). If you work with GSDML/EDS/ESI converters — useful.
- **Internationalisation** — Studio + website are currently
  translated to EN/DE/FR/ES/ZH/JA/TR/AR; some languages are only
  machine-pre-filled.

### 🌬️ HMI integration (bellowsd)

{{< components "bellowsd" >}}

- **OPC-UA companion specs** — bellowsd today supports generic
  OPC-UA nodes. Companion-spec adapters (e.g. PackML, OPC-UA
  Robotics) are welcome.
- **HMI frameworks** — `Hearth` is planned as the IIoT subscriber
  layer. If you work with MQTT, time-series DBs (InfluxDB,
  TimescaleDB) or Grafana pipelines, you can shape the architecture
  here.

### 🔥 Runtime + determinism (anvild)

{{< components "anvild" >}}

- **Real-time Linux tuning** — PREEMPT_RT kernel, CPU pinning,
  cache locality for sub-millisecond cycle times
- **Rust+LLVM codegen (rusty)** — planned migration of the layer-1
  codegen away from matiec/C output to Rust+LLVM. Determinism
  guarantees + online-change preparation.
- **Hardware targets** — Raspberry Pi, BeagleBone, industrial x86,
  ARM SBCs. Testing + performance profiling on real hardware.

### 📚 Education + documentation

{{< components "studio" >}}

- **Tutorials** — from "first Knight Rider in 5 minutes" to
  "complete machine control with OPC-UA + EtherCAT"
- **Example projects** — today only 2 demos live in the tree.
  More is always better.
- **Teaching curriculum** — universities wanting to use ForgeIEC
  as a teaching IDE. We deliver Studio for free; lecturers bring
  the IEC curriculum.

---

## What partners get back

| Offer | Concretely |
|---|---|
| **Source access** | Everything is OSS — source on GitHub + Forgejo |
| **Early access** | Development branch is at feature-status level (see [News](/news/)) — partners see changes on push day |
| **Code-review access** | PRs are reviewed by the core team, feedback in hours instead of weeks |
| **Roadmap input** | Sprint planning happens openly via GitHub issues + architecture specs |
| **Technical advice** | Architecture discussion via issues, mail, or direct contact |
| **Branding** | Partners listed on this page (once the first ones arrive) |

We do **not** sell premium licences and we promise **no** service-
contract privileges — every feature is part of the AGPL-3.0
distribution. Partnership means **close contact + early access +
participation**, not "paid special menu".

---

## Currently registered partners

As of 2026-05: no external partners yet — the platform is in the
build-up sprint, partner onboarding starts once the first subsystem
APIs (bridge SDK, FDD format) stabilise.

If you want to be among the first: get in touch (see below).

---

## How to apply

Send us:

1. **Who are you?** — person / organisation, background
2. **Where have you contributed?** — links to OSS projects,
   concrete commits / PRs / issues
3. **Which area?** — see the list above (bus bridges / editor /
   HMI / runtime / education) — please be specific
4. **What would your first step be?** — no plan document needed,
   a paragraph is enough

Reply: blacksmith@forgeiec.io.

---

## See also

- [News](/news/) — what the last sprints delivered
- [Architecture + Security](/help/ai/architecture/) — spec depth
  for security reviewers
- [Download](/download/) — all components + source tree
