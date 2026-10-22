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
The repositories are not publicly browsable; the source code is
under the AGPL, access on request. Access goes through SSH: send us
your SSH public key and we enable it. You can then review the code
before applying. Third-party contributions are accepted only once
the Contributor License Agreement is in force.

| Repository (`ssh://git@git.forgeiec.io/ForgeIEC/<name>.git`) | What's inside |
|---|---|
| **forgeiec-studio** | C++/Qt6 IDE + bus config + MCP server |
| **anvil** | Rust/Tokio PLC runtime, the Anvil server (anvild) |
| **tongs-core** and **tongs-*** | shared core of the bus bridges and one repository per protocol |
| **hearth** | operator interface (HMI), preview |
| **screen** | kiosk browser for operator panels |
| **lib-forgeiecdom**, **forge-mcp** | project model library, MCP library |
| **fdd-files** | device descriptions (FDD) |
| **bellows** | OPC-UA / HMI gateway — resting |
| **forgeiec-website** | the Hugo site you are reading right now |

The normative specifications live in the `forgeiec-studio`
repository under `documentation/architecture/`.

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

- **tongs-lorawan** — focus: wireless sensors for agriculture and
  wide-area plants (in progress)
- **tongs-ethercat** — DC sync, slave state machine, ENI XML
  import
- **tongs-profibus** — DP master, GSD import toolchain
- **tongs-ethernetip** — CIP connections, EDS import
- **tongs-can** — CANopen + J1939

For EtherCAT, PROFIBUS and EtherNet/IP the skeleton, fault model
and IPC wire format are in place — the protocol-specific part is
missing.

### 🛠️ Studio editor features

{{< components "studio" >}}

- **FBD/LD/SFC editors** — today the focus is on ST. Graphical
  languages need their own tree-sitter grammars + canvas renderers.
- **Vendor catalog** — over 1,100 device descriptions from Phoenix
  Contact, Beckhoff, Weidmüller, SALZ and others ship with it (as of
  22 Oct 2026). GSDML/EDS/ESI converters welcome.
- **Internationalisation** — translations of the Studio; the website
  is currently maintained in German and English.

### 🏠 Operator interface (Hearth)

{{< components "hearth" >}}

- **Hearth** — the operator interface reads the process data
  directly from the Anvil bus and is available as a preview. If you
  have experience with HMI design, alarming or trend recording, you
  can help shape it.

### 🔥 Runtime + determinism (Anvil server, anvild)

{{< components "anvild" >}}

- **Real-time Linux tuning** — PREEMPT_RT kernel, CPU pinning,
  cache locality for sub-millisecond cycle times
<!-- ENTWURF: Item "Rust+LLVM codegen (rusty)" removed — matiec has been replaced; whether rusty is still planned is the owner's decision (audit W-16). -->
- **Hardware targets** — Raspberry Pi, BeagleBone, industrial
  x86, ARM SBCs.

### 📚 Education + documentation

{{< components "studio" >}}

- **Tutorials** — from "first Knight Rider in 5 minutes" to
  "complete machine control with Modbus and LoRaWAN"
- **Example projects** — the Studio ships 11 examples today; more
  from real-world practice are welcome
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
