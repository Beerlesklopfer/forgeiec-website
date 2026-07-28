---
title: "Partners"
summary: "Forging the future of automation together"
---

## Partnership at ForgeIEC

ForgeIEC is an open-source project built on the conviction that
industrial automation must be accessible to everyone. We are
looking for partners who share this vision and are ready to
actively shape the future of automation.

---

## Our source repositories

The code base lives in the **Forgejo** at `git.forgeiec.io`.
The repositories are not publicly browsable. Access — read and
write alike — goes through SSH: send us your SSH public key and we
enable it. You can then review the code before applying.

| Repository | What's inside | Forgejo |
|---|---|---|
| **forgeiec-studio** | C++/Qt6 IDE + bus config + MCP server | [git.forgeiec.io/ForgeIEC/forgeiec-studio](https://git.forgeiec.io/ForgeIEC/forgeiec-studio) |
| **anvil** | Rust/Tokio PLC runtime + bridge subprocess manager | [git.forgeiec.io/ForgeIEC/anvil](https://git.forgeiec.io/ForgeIEC/anvil) |
| **bellows** | OPC-UA / HMI gateway | [git.forgeiec.io/ForgeIEC/bellows](https://git.forgeiec.io/ForgeIEC/bellows) |
| **forgeiec-website** | Hugo site you're reading right now | [git.forgeiec.io/ForgeIEC/forgeiec-website](https://git.forgeiec.io/ForgeIEC/forgeiec-website) |

Each repo contains its own `documentation/architecture/`
sub-directory or spec collection — anyone wanting to dive deeper
finds the normative RFC 2119 specs at full length.

---

## Requirements

### Proven open-source engagement

Applicants must already have demonstrated that they support the
idea of open source. That means:

- **Demonstrable contributions** to existing open-source projects
  (commits, pull requests, bug reports, documentation)
- **Public profile** on platforms such as GitHub, GitLab, or
  Codeberg
- **Active participation** in open-source communities — not just
  use but co-creation

We believe actions speak louder than words. Whoever sees open
source merely as a marketing instrument without contributing
themselves does not fit our philosophy.

### Shared values

- **Transparency** — open communication, traceable decisions
- **Collaboration** — code reviews, shared architecture
  discussions, knowledge sharing
- **Quality** — documented tests, clean code, industrial-grade
  reliability
- **Long-term thinking** — partnership is not a sprint but a
  marathon

---

## Areas where we are looking for contributors

If the requirements above fit you — these are the subsystems
where we are particularly looking for fellow builders:

### 🔧 Bus bridges (tongs-*)

{{< components "tongs,anvild" >}}

- **tongs-ethercat** — DC sync, slave state machine, ENI XML
  import
- **tongs-profibus** — DP master, GSD import toolchain
- **tongs-ethernetip** — CIP connections, EDS import
- **tongs-can** — CANopen + J1939

Skeleton + fault model + IPC wire format are in place — the
protocol-specific part is missing.

### 🛠️ Studio editor features

{{< components "studio" >}}

- **FBD/LD/SFC editors** — today the focus is on ST. Graphical
  languages need their own tree-sitter grammars + canvas renderers.
- **Vendor catalog** — FDDs for more manufacturers (today:
  Weidmueller). GSDML/EDS/ESI converters welcome.
- **Internationalisation** — Studio + website are translated into
  EN/DE/FR/ES/ZH/JA/TR/AR; some languages are only machine
  pre-filled.

### 🌬️ HMI integration (bellowsd)

{{< components "bellowsd" >}}

- **OPC-UA companion specs** — bellowsd today supports generic
  OPC-UA nodes. Companion-spec adapters (e.g. PackML, OPC-UA
  Robotics) welcome.
- **HMI frameworks** — `Hearth` is planned as the IIoT subscriber
  layer. If you work with MQTT, time-series DBs (InfluxDB,
  TimescaleDB) or Grafana pipelines, you can help shape the
  architecture here.

### 🔥 Runtime + determinism (anvild)

{{< components "anvild" >}}

- **Real-time Linux tuning** — PREEMPT_RT kernel, CPU pinning,
  cache locality for sub-millisecond cycle times
- **Rust+LLVM codegen (rusty)** — planned migration of the layer-1
  codegen away from matiec/C output to Rust+LLVM. Determinism
  guarantees + online-change preparation.
- **Hardware targets** — Raspberry Pi, BeagleBone, industrial
  x86, ARM SBCs.

### 📚 Education + documentation

{{< components "studio" >}}

- **Tutorials** — from "first Knight Rider in 5 minutes" to
  "complete machine control with OPC-UA + EtherCAT"
- **Example projects** — today only 2 demos live in the tree
- **Teaching curriculum** — universities wanting to use ForgeIEC
  as a teaching IDE. We deliver Studio for free; lecturers bring
  the IEC curriculum.

---

## What we offer

### Access to the ForgeIEC platform

- Early access to new features and development branches
- Direct line to the core team
- Possibility to actively shape the roadmap

### Joint development

- Shared work on industrial fieldbus drivers
- Integration of vendor-specific hardware
- Development of industry-specific extensions

### Technical support

- Prioritised bug fixing
- Architecture advice for own extensions
- Help integrating into existing systems

---

## Forms of partnership

### Technology partner

Manufacturers of automation components who want to integrate
their hardware in ForgeIEC. Joint driver development, device
configurations, and test procedures.

### Integration partner

Systems integrators and engineering offices that use ForgeIEC in
customer projects. Practical knowledge flows back into the
development.

### Education partner

Universities and training institutions that use ForgeIEC in
teaching. Free access for the education sector — the next
generation of automation engineers should learn with open tools.

---

## Currently registered partners

As of 2026-05: no external partners yet — the platform is in
build-up sprint, partner onboarding begins once the first
subsystem APIs (bridge SDK, FDD format) stabilise.

If you want to be among the first: see "How to apply" below.

---

## How to apply

You would like to become a partner? Write to us with:

- Description of your organisation
- Links to your open-source contributions
- Your motivation for a partnership
- Specific area where you would like to contribute
- Your SSH public key, if you want to review the code beforehand

---

<div style="text-align:center; padding: 2rem;">

**Together we forge the tools of the future.**

blacksmith@forgeiec.io

</div>
