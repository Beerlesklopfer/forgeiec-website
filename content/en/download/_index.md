---
title: "Download"
summary: "All ForgeIEC components — APT repository, direct downloads, source code"
---

## ForgeIEC components at a glance

ForgeIEC consists of several components. Which ones you need
depends on your role:

| Role | Component | Where to install |
|---|---|---|
| **PLC programmer / user** | `forgeiec` (ForgeIEC Studio) | Workstation |
| **Commissioning engineer** | `anvild` (PLC runtime) | Target PLC |
| **HMI / OPC-UA bridge** | `bellowsd` (HMI gateway) | Target PLC or separate host |
| **Modbus TCP** | `tongs-modbustcp` (bus bridge) | Target PLC |
| **Profibus / EtherCAT / EthernetIP** | further `tongs-*` | Target PLC |

---

## Installation from the APT repository

ForgeIEC is provided as a signed Debian repository at
`apt.forgeiec.io`. Setup is a one-time step per workstation or
target PLC:

```bash
# Import signing key
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Add repository source
# (Debian 12 "bookworm" or Debian 13 "trixie" — pick what matches your system)
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

Then install components individually:

```bash
# Workstation
sudo apt install forgeiec                # ForgeIEC Studio

# Target PLC
sudo apt install anvild                  # PLC runtime
sudo apt install bellowsd                # HMI gateway
sudo apt install tongs-modbustcp         # Modbus TCP bridge
```

Updates follow the standard `apt update && apt upgrade` cycle —
no manual `.deb` files needed.

---

## Supported platforms

| Component | Architectures | Debian codenames |
|---|---|---|
| ForgeIEC Studio | amd64, arm64 | bookworm, trixie |
| anvild | amd64, arm64 | bookworm, trixie |
| bellowsd | amd64, arm64 | bookworm, trixie |
| Bus bridges (tongs-*) | amd64, arm64 | bookworm, trixie |
| Hearth | amd64, arm64 | bookworm, trixie |

**Windows build** of ForgeIEC Studio: in preparation. Until then
Studio runs natively on Linux or via WSL2 on Windows
workstations.

---

## Direct downloads (release tarballs)

If you cannot or do not want to use the APT repository — e.g. for
air-gap workstations — you can download individual releases
directly from the repository pages:

- **ForgeIEC Studio source**:
  [GitHub](https://github.com/Beerlesklopfer/ForgeIEC-Studio) /
  [Forgejo](https://git.forgeiec.io/ForgeIEC/forgeiec-studio)
- **anvild + bridges**:
  [Forgejo](https://git.forgeiec.io/ForgeIEC/anvil)
- **bellowsd**:
  [Forgejo](https://git.forgeiec.io/ForgeIEC/bellows)
- **Website source**:
  [GitHub](https://github.com/Beerlesklopfer/forgeiec-website) /
  [Forgejo](https://git.forgeiec.io/ForgeIEC/forgeiec-website)

Per release, signed `.deb` packages + source tarballs are
attached to the GitHub/Forgejo release tag.

---

## Building from source

```bash
# Clone the repository (with submodules)
git clone --recurse-submodules https://github.com/Beerlesklopfer/ForgeIEC-Studio.git
cd ForgeIEC-Studio

# Build Studio + all daemons
cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)

# Deploy on the local system
./deploy.sh all
```

Prerequisites:

- Debian 12/13 or Ubuntu 24.04+
- `build-essential cmake qt6-base-dev qt6-declarative-dev libtomlplusplus-dev`
- Rust 1.85+ (via rustup)

---

## Demo projects

Example projects shipped with ForgeIEC Studio:

| Project | Purpose |
|---|---|
| `knight_rider.forge` | Classic chaser-light test for Bellows LEDs |
| more to follow | … |

Found in Studio under `File → Open Example`.

---

## Next steps

- [First steps with ForgeIEC Studio](/help/)
- [Setting up the AI assistant](/help/ai/)
- [Bus configuration](/help/bus-config/)
- [News + release notes](/news/)
