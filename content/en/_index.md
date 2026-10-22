---
title: "ForgeIEC"
---

<div style="text-align:center; padding: 3rem 1rem;">

# Forged for industry.

**An IEC 61131-3 development environment built to industrial standards — open source, AI-native, no vendor lock-in.**

[Download](/download/) · [Architecture](/help/ai/architecture/) · [News](/news/)

</div>

---

## What ForgeIEC delivers today

| Area | Status |
|---|---|
| **All 5 IEC 61131-3 languages** — ST, IL, FBD, LD, SFC | productive |
| **Multi-task scheduler** — real pthread parallelism | productive |
| **Live diagnostics** — monitor + oscilloscope with trigger, CSV recording | productive |
| **Bus system** — Modbus TCP productive, EtherCAT + Profibus + EtherNet/IP in progress | mixed |
| **Manufacturer data as first-class** — FDDs with embedded PDFs + diagnostic-bit resolution | productive |
| **AI assistant built-in** — ~180 typed MCP tools, 5 personas | productive |
| **Team federation** — multiple workstations with Caretaker CA | MVP productive |
| **HMI / OPC-UA bridge** via bellowsd | productive |
| **Reproducible builds** — signed APT + RPM repositories, AGPL-3.0 | productive |

---

## Three pillars

### 🛠️ ForgeIEC Studio — the IDE

Native C++/Qt6 application, all five IEC languages, bus
configuration, live monitor, oscilloscope, AI assistant built-in.
Multi-workstation federation via trust store + Caretaker model.
No browser UI, no cloud dependency.

### 🔥 anvild — the runtime

Rust/Tokio daemon on the target PLC. Multi-task, deterministic
scan cycles, gRPC connection to Studio, subprocess manager for
bus bridges, automatic watchdog restart of crashed bridges.

### 🔧 tongs-* — bus bridges

One daemon per protocol. Uniform fault model, FDD-driven
diagnostic bits, Anvil zero-copy IPC between bridge and runtime,
bridges can crash + restart independently.

---

## Why ForgeIEC?

Industrial automation is a key technology — and access to
professional tools is restricted by license costs and proprietary
systems. ForgeIEC makes the value accessible to everyone.

Three promises we keep:

- **Open source (AGPL-3.0)** — source available on request (SSH key
  enablement), build reproducible, updates via signed APT repository
- **Vendor-neutral** — manufacturer data integrated as FDDs, no
  proprietary device format, migration-capable
- **Industrial safety** — 4-layer defence for force settings,
  Confirmation State Machine for every write action, honest
  sampling-limit model instead of marketing promises

Read more in the
[founding story](/news/die-forgeiec-geschichte/) — how a 2018
OpenPLC fork became an independent platform.

---

## Get started

```bash
# Add the signing key (once)
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Add the repository source
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

# Install editor + runtime
sudo apt update
sudo apt install forgeiec-studio forgeiec-anvil-server
```

Shown for Debian 13 (trixie). For Debian 12 (bookworm) or Ubuntu 24.04 (noble), replace both occurrences of `trixie`. All distributions, RPM and the other packages: [Download](/download/).

First steps with the AI assistant: [Help](/help/ai/).

---

<div style="text-align:center; padding: 2rem;">

**Made for industry. Open by default.**

blacksmith@forgeiec.io

</div>
