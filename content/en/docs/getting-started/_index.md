---
title: "Getting Started"
linkTitle: "Getting Started"
weight: 1
description: Install ForgeIEC and create your first PLC program.
---

## Installation

### From Debian Packages

Download the latest release from [GitHub Releases](https://github.com/Beerlesklopfer/ForgeIEC/releases).

```bash
# Install editor (workstation)
sudo dpkg -i forgeiec_0.1.0_amd64.deb
sudo apt-get -f install

# Install runtime server (PLC target)
sudo dpkg -i forgeiecd_0.1.0_amd64.deb
sudo apt-get -f install
sudo systemctl enable --now forgeiecd
```

### Build from Source

```bash
sudo apt install qt6-base-dev libgrpc++-dev cargo rustc flex bison
git clone https://github.com/Beerlesklopfer/ForgeIEC.git
cd ForgeIEC
dpkg-buildpackage -us -uc -b -d
```

## First Steps

1. Launch ForgeIEC: `forgeiec`
2. Connect to your runtime server via the Connection dialog
3. Create a new project (File > New Project)
4. Add a PROGRAM POU and write your first Structured Text
5. Compile and upload to the PLC
6. Start the PLC via the Control panel

## Architecture

```
Workstation                          PLC Target
+-----------+     gRPC (50051)     +------------+
| ForgeIEC  | ------------------> | forgeiecd   |
| (Qt6 GUI) |  compile & upload   | (Rust)      |
|           |  live debugging     |             |
| iec2c     |  bus config         | Modbus TCP  |
| (ST -> C) |                     | EtherCAT    |
+-----------+                     | Profibus    |
                                  +------------+
```

The editor runs `iec2c` locally to compile IEC ST/IL to C code, then uploads
the C files to the runtime server which compiles them with `g++` on the target.
