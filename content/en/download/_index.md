---
title: "Download"
summary: "All ForgeIEC components — APT and RPM repositories, direct downloads, source code"
---

## ForgeIEC components at a glance

ForgeIEC consists of several components. Which ones you need
depends on your role:

| Role | Component | Where to install |
|---|---|---|
| **PLC programmer / user** | `forgeiec-studio` | Workstation |
| **Commissioning engineer** | `forgeiec-anvil-server` (ships `anvild`) | Target PLC |
| **HMI / OPC-UA bridge** | `forgeiec-bellows-server` (ships `bellowsd`) | Target PLC or separate host |
| **Modbus TCP** | contained in `forgeiec-anvil-server` | Target PLC |
| **Profibus / EtherCAT / EthernetIP** | likewise in `forgeiec-anvil-server` | Target PLC |
| **Operator panel** | `forgeiec-screen-wayland` or `-xorg` | Panel hardware |

---

## Installation from the package repository

ForgeIEC is provided as a signed Debian repository at
`apt.forgeiec.io` and as a signed RPM repository at
`rpm.forgeiec.io`. Setup is a one-time step per workstation or
target PLC — pick your distribution:

{{< distro-install >}}

Then install components individually:

```bash
# Workstation
sudo apt install forgeiec-studio          # ForgeIEC Studio
sudo apt install forgeiec-fdd-data        # Device descriptions (recommended)

# Target PLC
sudo apt install forgeiec-anvil-server    # PLC runtime (anvild + all tongs-*)
sudo apt install forgeiec-bellows-server  # HMI gateway (bellowsd)

# Operator panel
sudo apt install forgeiec-screen-wayland  # Kiosk on Wayland
sudo apt install forgeiec-screen-xorg     # Kiosk on X11
```

On RPM systems the commands read `sudo dnf install …` with
otherwise identical package names.

The bus bridges (`tongs-modbustcp`, `tongs-ethercat`, `tongs-profibus`,
`tongs-ethernetip`) are **not** separate packages — they live inside
`forgeiec-anvil-server` and are started by `anvild`.

Updates follow the standard `apt update && apt upgrade` cycle —
no manual `.deb` files needed.

---

## Supported platforms

### Debian / Ubuntu (`apt.forgeiec.io`)

| Package | Architectures | Suites |
|---|---|---|
| `forgeiec-studio` | amd64, arm64 | bookworm, trixie, noble |
| `forgeiec-fdd-data` | architecture-independent | bookworm, trixie, noble |
| `forgeiec-anvil-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-bellows-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-screen-wayland` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-screen-xorg` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `hearth-server` | amd64, arm64 | bookworm, trixie, jammy, noble |

Suite mapping: `bullseye` = Debian 11, `bookworm` = Debian 12,
`trixie` = Debian 13, `jammy` = Ubuntu 22.04, `noble` = Ubuntu 24.04.

### Enterprise Linux / Fedora (`rpm.forgeiec.io`)

| Package | Architecture | Distributions |
|---|---|---|
| `forgeiec-screen-wayland` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-screen-xorg` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |

RPM delivery is new and currently covers the operator panel only.
ForgeIEC Studio and the runtime will follow once their RPM slots are
stable.

There are **two different signing keys**: `forgeiec.gpg` (ed25519)
for apt and `forgeiec-rpm.asc` (RSA-4096) for rpm. The difference is
not cosmetic — RHEL 9 ships `rpm` 4.16, whose internal PGP parser
cannot verify ed25519.

arm64 is deliberately absent on the RPM side: the CI cross-compile
path depends on Debian packages that do not exist on Enterprise Linux.

**Windows build** of ForgeIEC Studio: in preparation. Until then
Studio runs natively on Linux or via WSL2 on Windows
workstations.

---

## Direct downloads (release tarballs)

If you cannot or do not want to use the package repository — e.g. for
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
