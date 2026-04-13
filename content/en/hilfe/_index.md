---
title: "Help"
summary: "Documentation and resources for ForgeIEC"
---

## Help and Resources

Welcome to the ForgeIEC help section. Here you will find information
about the fundamentals of our project and our philosophy.

---

## Topics

### [Bus Configuration](/hilfe/bus-config/)

PLCopen XML schema for industrial fieldbus configuration in `.forge` projects.
Segments, devices, variable binding and IEC address assignment.

### [Test Coverage](/hilfe/tests/)

117 automated tests verify the complete IEC 61131-3 language feature set,
all 132 standard library blocks and the multi-task threading system.

### [Open Source Philosophy](/hilfe/open-source/)

The idea behind open source goes far beyond software — it is a movement
that liberates knowledge and democratizes innovation.

---

## Getting Started

ForgeIEC consists of two components:

1. **ForgeIEC Editor** (`forgeiec`) — The development environment on your workstation
2. **ForgeIEC Daemon** (`anvild`) — The runtime system on the target PLC

### Installation from the ForgeIEC APT Repository

ForgeIEC is provided as a signed Debian repository at
`apt.forgeiec.io`. Setup is a one-time step on each workstation
or target PLC:

```bash
# Import signing key
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Add repository source
# (Debian 12 "bookworm" or Debian 13 "trixie" — match your system)
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

Then install any ForgeIEC package using the standard package manager:

```bash
# Editor (Workstation)
sudo apt install forgeiec

# Daemon (Target PLC)
sudo apt install anvild
```

Updates follow the normal `apt update && apt upgrade` lifecycle —
no manual `.deb` files needed.

### Supported Platforms

| Component | Architectures | Debian Codenames |
|-----------|---------------|------------------|
| Editor    | amd64, arm64  | bookworm, trixie |
| Daemon    | amd64, arm64  | bookworm, trixie |
| Bridges   | amd64, arm64  | bookworm, trixie |
| Hearth    | amd64, arm64  | bookworm, trixie |

### Contact

For questions, reach out to: blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**The documentation grows with the project.**

blacksmith@forgeiec.io

</div>
