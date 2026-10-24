---
title: "Help"
summary: "Documentation and resources for ForgeIEC"
---

## Help and Resources

Welcome to the ForgeIEC help section. Here you will find information
about the fundamentals of our project and our philosophy.

---

## Topics

### [Online Help](/help/online/)

Entry point for the editor's context-sensitive help. F1 in the editor
opens exactly the matching page on this site. URL scheme and topic
slugs are described there.

### [FAQ](/help/faq/)

Growing collection of common questions + practical solutions. Starts
with one classic symptom (variable sticks despite a fresh deploy) and
grows with every new observed case.

### [AI integration](/help/ai/)

How to use the built-in AI assistant in ForgeIEC Studio: personas,
providers (ChatGPT / Claude / local), daily operation, security
model, team mode for multiple workstations. Plus an architecture
deep-dive for security auditors.

### [MCP protocol](/help/mcp/)

The protocol layer under the AI assistant — for application
engineers connecting their own scripts/tools, and for IT/operations
deploying, monitoring, and troubleshooting.

---

## Other sections

- [Download](/download/) — all components + APT setup
- [News](/news/) — release notes + technical updates

### [Bus Configuration](/help/bus-config/)

PLCopen XML schema for industrial fieldbus configuration in `.forge` projects.
Segments, devices, variable binding and IEC address assignment.

### [Test Coverage](/help/tests/)

62 automated test programs (as of 22 Oct 2026) verify the IEC 61131-3
language feature set, the standard library blocks and the multi-task
threading system.

### [Open Source Philosophy](/help/open-source/)

The idea behind open source goes far beyond software — it is a movement
that liberates knowledge and democratizes innovation.

---

## Getting Started

To get started you need two packages:

1. **ForgeIEC Studio** (`forgeiec-studio`, program `forgeiec`) — the development environment on your workstation
2. **Anvil server (anvild)** (`forgeiec-anvil-server`, program `anvil-server`) — the runtime system on the target PLC

All other components are listed on the [platform page](/en/plattform/).

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
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

Then install any ForgeIEC package using the standard package manager:

```bash
# Editor (Workstation)
sudo apt install forgeiec-studio

# Daemon (Target PLC)
sudo apt install forgeiec-anvil-server
```

Updates follow the normal `apt update && apt upgrade` lifecycle —
no manual `.deb` files needed.

### Supported Platforms

| Component | Architectures | Debian/Ubuntu suites |
|-----------|---------------|------------------|
| Studio    | amd64, arm64  | bookworm, trixie, noble |
| Anvil server + bridges | amd64, arm64, armhf | bookworm, trixie, jammy, noble |
| Hearth (preview) | amd64, arm64, armhf | bookworm, trixie, jammy, noble |

Studio, device descriptions, Hearth and the HMI panel are also
available as RPMs for AlmaLinux 9 and Fedora 44 at `rpm.forgeiec.io`
(the runtime not yet). A Windows build of the Studio exists; the
installer is available on request. The full package/platform matrix
is on the [download page](/en/download/).

### Contact

For questions, reach out to: blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**The documentation grows with the project.**

blacksmith@forgeiec.io

</div>
