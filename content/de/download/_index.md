---
title: "Download"
summary: "Alle ForgeIEC-Komponenten — APT-Repository, Direkt-Downloads, Quellcode"
---

## ForgeIEC-Komponenten im Ueberblick

ForgeIEC besteht aus mehreren Komponenten. Welche Sie brauchen,
haengt von Ihrer Rolle:

| Rolle | Komponente | Wo installieren |
|---|---|---|
| **SPS-Programmierer / Anwender** | `forgeiec` (ForgeIEC Studio) | Workstation |
| **Inbetriebnehmer** | `anvild` (PLC-Runtime) | Ziel-SPS |
| **HMI / OPC-UA-Anbindung** | `bellowsd` (HMI-Gateway) | Ziel-SPS oder eigener Host |
| **Modbus-TCP** | `tongs-modbustcp` (Bus-Bridge) | Ziel-SPS |
| **Profibus / EtherCAT / EthernetIP** | weitere `tongs-*` | Ziel-SPS |

---

## Installation aus dem APT-Repository

ForgeIEC wird als signiertes Debian-Repository unter
`apt.forgeiec.io` bereitgestellt. Einrichtung ist einmalig pro
Workstation bzw. Ziel-SPS:

```bash
# Signier-Schluessel hinterlegen
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Repository-Quelle eintragen
# (Debian 12 "bookworm" bzw. Debian 13 "trixie" — passend zum System)
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

Danach Komponenten einzeln installieren:

```bash
# Workstation
sudo apt install forgeiec                # ForgeIEC Studio

# Ziel-SPS
sudo apt install anvild                  # PLC-Runtime
sudo apt install bellowsd                # HMI-Gateway
sudo apt install tongs-modbustcp         # Modbus-TCP-Bridge
```

Updates folgen dem normalen `apt update && apt upgrade`-Zyklus —
keine manuellen `.deb`-Dateien noetig.

---

## Unterstuetzte Plattformen

| Komponente | Architekturen | Debian-Codenamen |
|---|---|---|
| ForgeIEC Studio | amd64, arm64 | bookworm, trixie |
| anvild | amd64, arm64 | bookworm, trixie |
| bellowsd | amd64, arm64 | bookworm, trixie |
| Bus-Bridges (tongs-*) | amd64, arm64 | bookworm, trixie |
| Hearth | amd64, arm64 | bookworm, trixie |

**Windows-Build** von ForgeIEC Studio: in Vorbereitung. Bis dahin
laeuft das Studio unter Linux nativ oder per WSL2 auf Windows-
Workstations.

---

## Direkt-Downloads (Release-Tarballs)

Wer kein APT-Repository nutzen kann oder mag — z.B. fuer Air-Gap-
Workstations — kann die einzelnen Releases direkt von der
Repository-Seite herunterladen:

- **ForgeIEC-Studio-Quellcode**:
  [GitHub](https://github.com/Beerlesklopfer/ForgeIEC-Studio) /
  [Forgejo](https://git.forgeiec.io/ForgeIEC/forgeiec-studio)
- **anvild + Bridges**:
  [Forgejo](https://git.forgeiec.io/ForgeIEC/anvil)
- **bellowsd**:
  [Forgejo](https://git.forgeiec.io/ForgeIEC/bellows)
- **Webseiten-Quellcode**:
  [GitHub](https://github.com/Beerlesklopfer/forgeiec-website) /
  [Forgejo](https://git.forgeiec.io/ForgeIEC/forgeiec-website)

Pro Release sind signierte `.deb`-Pakete + Source-Tarballs am
GitHub/Forgejo-Release-Tag angehaengt.

---

## Bauen aus dem Quellcode

```bash
# Repository klonen (mit Submodules)
git clone --recurse-submodules https://github.com/Beerlesklopfer/ForgeIEC-Studio.git
cd ForgeIEC-Studio

# Studio + alle Daemons bauen
cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)

# Deployen auf das lokale System
./deploy.sh all
```

Voraussetzungen:

- Debian 12/13 oder Ubuntu 24.04+
- `build-essential cmake qt6-base-dev qt6-declarative-dev libtomlplusplus-dev`
- Rust 1.85+ (via rustup)

---

## Demo-Projekte

Mit ForgeIEC Studio ausgelieferte Beispiel-Projekte:

| Projekt | Zweck |
|---|---|
| `knight_rider.forge` | Klassischer Lauflicht-Test fuer Bellows-LEDs |
| weitere folgen | … |

Zu finden im Studio unter `File -> Open Example`.

---

## Naechste Schritte

- [Erste Schritte mit ForgeIEC Studio](/help/)
- [KI-Helfer einrichten](/help/ai/)
- [Bus-Konfiguration](/help/bus-config/)
- [News + Release-Notes](/news/)
