---
title: "Help"
summary: "Documentation and resources for ForgeIEC"
---

## Help and Resources

Welcome to the ForgeIEC help section. Here you will find information
about the fundamentals of our project and our philosophy.

---

## Topics

### [Open Source Philosophy](/hilfe/open-source/)

The idea behind open source goes far beyond software — it is a movement
that liberates knowledge and democratizes innovation.

---

## Getting Started

ForgeIEC consists of two components:

1. **ForgeIEC Editor** (`forgeiec`) — The development environment on your workstation
2. **ForgeIEC Daemon** (`anvild`) — The runtime system on the target PLC

### Installation

ForgeIEC is distributed as Debian packages:

```bash
# Editor (Workstation)
sudo dpkg -i forgeiec_0.1.0_amd64.deb

# Daemon (Target PLC)
sudo dpkg -i anvild_0.1.0_armhf.deb
```

### Supported Platforms

| Component | Architectures |
|-----------|---------------|
| Editor | x86_64, ARM64 |
| Daemon | x86_64, ARM64, ARMv7 |

### Contact

For questions, reach out to: blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**The documentation grows with the project.**

blacksmith@forgeiec.io

</div>
