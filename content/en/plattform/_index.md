---
title: "Platform"
description: "The ForgeIEC Platform -- all components for industrial automation"
weight: 10
---

## The ForgeIEC Platform

ForgeIEC is a complete industrial automation platform -- from the development
environment to the supervisory system. Each component bears the name of a
blacksmith's tool, because ForgeIEC is forged for industry.

---

### Forge Studio

**IEC 61131-3 Development Environment**

The professional IDE for PLC programming. All five IEC languages, graphical
and textual editing, local compilation, remote deployment. Built with C++17
and Qt6.

[Learn more](forge-studio/)

---

### Anvil

**Real-Time PLC Runtime**

The runtime daemon that executes IEC programs on the target system. Zero-Copy
communication between the runtime and protocol bridges via Anvil shared memory
technology.

[Learn more](anvil/)

---

### Bellows

**OPC UA Gateway** -- In Development

Standardized machine-to-machine communication conforming to the OPC UA
standard. Seamless integration of automation systems into existing IT
infrastructure.

[Learn more](bellows/)

---

### Hearth

**SCADA/HMI** -- In Development

Process visualization and human-machine interface for industrial supervision.
Real-time dashboards, data history, alarm management.

[Learn more](hearth/)

---

### Spark

**Zenoh Tunnel**

Edge-to-Cloud network bridge based on the Zenoh protocol. Secure connection
between on-site PLCs and cloud services, without VPN, without complex
configuration.

[Learn more](spark/)

---

### Tongs

**Fieldbus Bridges**

Protocol bridges for Modbus TCP/RTU, EtherCAT and Profibus DP. Each bridge
runs as an independent process, monitored and automatically restarted by the
runtime.

[Learn more](tongs/)

---

### Ledger

**Manufacturing Order Management** -- In Development

MES integration for manufacturing order management, production tracking and
traceability. Bridge between automation and production planning.

[Learn more](ledger/)

---

<div style="text-align:center; padding: 2rem;">

**Built on OpenPLC** -- ForgeIEC is based on the
[OpenPLC](https://autonomylogic.com/) project and is fully compatible with
its file architecture. Existing OpenPLC projects can be opened and developed
directly.

**All components are Open Source. No license fees. No vendor lock-in.**

blacksmith@forgeiec.io

</div>
