---
title: "Download"
summary: "All ForgeIEC components — APT and RPM repositories, direct downloads, source code"
---

{{< callout type="note" title="State: preview version 0.2" >}}
All packages are preview versions of the 0.2 series. The ST editor is
in productive use (pilot operation); the IL, FBD, LD and SFC editors
and further buses follow.
{{< /callout >}}

## ForgeIEC components at a glance

ForgeIEC consists of several components. Which ones you need
depends on your role:

| Role | Component | Where to install |
|---|---|---|
| **PLC programmer / user** | `forgeiec-studio` | Workstation |
| **Commissioning engineer** | `forgeiec-anvil-server` — the Anvil server (anvild); service `forgeiec-anvil-server.service`, program `anvil-server` | Target PLC |
| **Modbus TCP** | contained in `forgeiec-anvil-server` | Target PLC |
| **EtherCAT / PROFIBUS / EtherNet/IP** | skeleton, likewise in `forgeiec-anvil-server` — protocol in progress | Target PLC |
| **Operator interface (HMI, preview)** | `forgeiec-hearth-server` | Target PLC |
| **Operator panel** | `forgeiec-screen-wayland` or `-xorg` | Panel hardware |
| **OPC-UA gateway** | `forgeiec-bellows-server` — *resting, unmaintained* | — |

---

## Installing from the package repository

ForgeIEC is provided as a signed Debian repository at
`apt.forgeiec.io` and as a signed RPM repository at
`rpm.forgeiec.io` — signed packages from an automated CI. Setup is
a one-time step per workstation or target PLC — pick your
distribution:

{{< distro-install >}}

Then install the components individually:

```bash
# Workstation
sudo apt install forgeiec-studio          # ForgeIEC Studio
sudo apt install forgeiec-fdd-data        # device descriptions (recommended)

# Target PLC
sudo apt install forgeiec-anvil-server    # PLC runtime (Anvil server + all tongs-*)
sudo apt install forgeiec-hearth-server   # operator interface (preview)

# Operator panel
sudo apt install forgeiec-screen-wayland  # kiosk under Wayland
sudo apt install forgeiec-screen-xorg     # kiosk under X11
```

On RPM systems the commands are `sudo dnf install …` with the same
package names — which packages exist there is shown in the table
below (the runtime not yet).

The bus bridges (`tongs-modbustcp`, `tongs-ethercat`, `tongs-profibus`,
`tongs-ethernetip`) are **not** separate packages — they ship inside
`forgeiec-anvil-server` and are started by the Anvil server.

The package `forgeiec-bellows-server` (OPC-UA gateway) remains in the
APT repository but is **resting** — it is currently neither developed
nor maintained.

Updates follow the normal `apt update && apt upgrade` cycle — no
manual `.deb` files required.

---

## Supported platforms

### Debian / Ubuntu (`apt.forgeiec.io`)

| Package | Architectures | Suites |
|---|---|---|
| `forgeiec-studio` | amd64, arm64 | bookworm, trixie, noble |
| `forgeiec-fdd-data` | architecture-independent | bookworm, trixie, noble |
| `forgeiec-anvil-server` | amd64, arm64, armhf | bookworm, trixie, jammy, noble |
| `forgeiec-hearth-server` | amd64, arm64, armhf | bookworm, trixie, jammy, noble |
| `forgeiec-screen-wayland` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-screen-xorg` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-bellows-server` (resting) | amd64, arm64, armhf | bookworm, trixie, jammy, noble |

Suite mapping: `bullseye` = Debian 11, `bookworm` = Debian 12,
`trixie` = Debian 13, `jammy` = Ubuntu 22.04, `noble` = Ubuntu 24.04.
`armhf` (ARMv7) is available for the runtime, Hearth and the device
descriptions.

### Enterprise Linux / Fedora (`rpm.forgeiec.io`)

| Package | Architectures | Distributions |
|---|---|---|
| `forgeiec-studio` | x86_64, aarch64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-fdd-data` | x86_64, aarch64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-hearth-server` | x86_64 | AlmaLinux 9 (`el9`) |
| `forgeiec-screen-wayland` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-screen-xorg` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |

**Runtime as RPM: not available yet.** `forgeiec-anvil-server` is
currently shipped as a Debian package only.

<!-- ENTWURF: RPM table per audit W-09 (measured el9/x86_64, el9/aarch64, fedora-44/aarch64); fedora-44/x86_64 was not listed separately in the audit. Verify against rpm.forgeiec.io before publishing. -->

There are **two different signing keys**: `forgeiec.gpg` (ed25519)
for apt and `forgeiec-rpm.asc` (RSA-4096) for rpm. The difference is
not cosmetic — RHEL 9 ships `rpm` 4.16, whose internal PGP parser
cannot verify ed25519.

### Windows

A Windows build of ForgeIEC Studio exists and its CI runs. There is
no public download yet — you get the installer **on request** at
blacksmith@forgeiec.io.

---

## Source code

The source code is licensed under AGPL-3.0-or-later (the part linked
into your project under Apache-2.0). **The repositories are not
publicly browsable** — access on request: send your SSH public key
to blacksmith@forgeiec.io and we will enable it. Afterwards these
repositories, among others, are open to you:

- **ForgeIEC Studio**: `ForgeIEC/forgeiec-studio`
- **Anvil server (anvild)**: `ForgeIEC/anvil`
- **Tongs (bus bridges)**: `ForgeIEC/tongs-core` and one `ForgeIEC/tongs-*` per protocol
- **Hearth**: `ForgeIEC/hearth`
- **bellowsd** (resting): `ForgeIEC/bellows`
- **Website**: `ForgeIEC/forgeiec-website`

The normative specifications live in the `forgeiec-studio`
repository under `documentation/architecture/`.

---

## Building from source

```bash
# Clone the repository (with submodules) — SSH only, after
# your SSH public key has been enabled
git clone --recurse-submodules ssh://git@git.forgeiec.io/ForgeIEC/forgeiec-studio.git
cd forgeiec-studio

# Build the Studio
cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc)

# Deploy to the local system
./deploy.sh all
```

Prerequisites (Debian 12/13, Ubuntu 24.04), as the CI installs them:

```bash
sudo apt install build-essential cmake ninja-build pkg-config git \
  qt6-base-dev qt6-base-dev-tools qt6-tools-dev qt6-tools-dev-tools \
  libqt6svg6-dev libqt6sql6-sqlite libqt6charts6-dev libqt6opengl6-dev \
  libgl-dev libssl-dev libre2-dev libargon2-dev libsqlite3-dev libxml2-dev \
  libtomlplusplus-dev libprotobuf-dev protobuf-compiler \
  libgrpc++-dev protobuf-compiler-grpc \
  forgeiec-libforge-mcp-dev   # from the ForgeIEC APT repository
# Debian 13 additionally: qt6-svg-plugins
```

The authoritative list is the package set in
`.forgejo/workflows/linux.yml` in the repository.

---

## Example projects

Examples shipped with ForgeIEC Studio (Studio: `File → Open Example`):

| Example | Content |
|---|---|
| Blinky | Blinking light with TON/TOF |
| Star-Delta Reversing Starter | Star-delta reversing starter |
| Knight Rider | Running light, 16 bit |
| Traffic Light | Traffic light control |
| PID Controller | PID temperature control (function) |
| Weekly Timer | Weekly timer (function block) |
| FOC Demo | Field-oriented control, 3-phase drive |
| Tankanlage | Tank plant with Hearth operator interface |
| Conveyor Pick & Place | Conveyor with gripper |
| Compressor Station | Compressor station |
| Axis Control | Axis control with nested STRUCT |

---

## Next steps

- [First steps with ForgeIEC Studio](/en/help/)
- [Setting up the AI assistant](/en/help/ai/)
- [Bus configuration](/en/help/bus-config/)
- [News + release notes](/en/news/)
