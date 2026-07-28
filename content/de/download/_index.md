---
title: "Download"
summary: "Alle ForgeIEC-Komponenten — APT-Repository, Direkt-Downloads, Quellcode"
---

## ForgeIEC-Komponenten im Ueberblick

ForgeIEC besteht aus mehreren Komponenten. Welche Sie brauchen,
haengt von Ihrer Rolle:

| Rolle | Komponente | Wo installieren |
|---|---|---|
| **SPS-Programmierer / Anwender** | `forgeiec-studio` | Workstation |
| **Inbetriebnehmer** | `forgeiec-anvil-server` (liefert `anvild`) | Ziel-SPS |
| **HMI / OPC-UA-Anbindung** | `forgeiec-bellows-server` (liefert `bellowsd`) | Ziel-SPS oder eigener Host |
| **Modbus-TCP** | im Paket `forgeiec-anvil-server` enthalten | Ziel-SPS |
| **Profibus / EtherCAT / EthernetIP** | ebenfalls in `forgeiec-anvil-server` | Ziel-SPS |
| **Bedien-Panel** | `forgeiec-screen-wayland` oder `-xorg` | Panel-Hardware |

---

## Installation aus dem Paket-Repository

ForgeIEC wird als signiertes Debian-Repository unter
`apt.forgeiec.io` und als signiertes RPM-Repository unter
`rpm.forgeiec.io` bereitgestellt. Einrichtung ist einmalig pro
Workstation bzw. Ziel-SPS — waehlen Sie Ihre Distribution aus:

{{< distro-install >}}

Danach Komponenten einzeln installieren:

```bash
# Workstation
sudo apt install forgeiec-studio          # ForgeIEC Studio
sudo apt install forgeiec-fdd-data        # Geraetebeschreibungen (empfohlen)

# Ziel-SPS
sudo apt install forgeiec-anvil-server    # PLC-Runtime (anvild + alle tongs-*)
sudo apt install forgeiec-bellows-server  # HMI-Gateway (bellowsd)

# Bedien-Panel
sudo apt install forgeiec-screen-wayland  # Kiosk unter Wayland
sudo apt install forgeiec-screen-xorg     # Kiosk unter X11
```

Auf RPM-Systemen heissen die Befehle `sudo dnf install …` bei sonst
gleichen Paketnamen.

Die Bus-Bridges (`tongs-modbustcp`, `tongs-ethercat`, `tongs-profibus`,
`tongs-ethernetip`) sind **keine** eigenen Pakete — sie liegen im Paket
`forgeiec-anvil-server` und werden von `anvild` gestartet.

Updates folgen dem normalen `apt update && apt upgrade`-Zyklus —
keine manuellen `.deb`-Dateien noetig.

---

## Unterstuetzte Plattformen

### Debian / Ubuntu (`apt.forgeiec.io`)

| Paket | Architekturen | Suites |
|---|---|---|
| `forgeiec-studio` | amd64, arm64 | bookworm, trixie, noble |
| `forgeiec-fdd-data` | architekturunabhaengig | bookworm, trixie, noble |
| `forgeiec-anvil-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-bellows-server` | amd64, arm64 | bookworm, trixie, jammy, noble |
| `forgeiec-screen-wayland` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-screen-xorg` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `hearth-server` | amd64, arm64 | bookworm, trixie, jammy, noble |

Suite-Zuordnung: `bullseye` = Debian 11, `bookworm` = Debian 12,
`trixie` = Debian 13, `jammy` = Ubuntu 22.04, `noble` = Ubuntu 24.04.

### Enterprise Linux / Fedora (`rpm.forgeiec.io`)

| Paket | Architektur | Distributionen |
|---|---|---|
| `forgeiec-screen-wayland` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-screen-xorg` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |

Die RPM-Auslieferung ist neu und umfasst derzeit nur das Bedien-Panel.
ForgeIEC Studio und die Runtime folgen, sobald ihre RPM-Slots stabil sind.

Es gibt **zwei verschiedene Signierschluessel**: `forgeiec.gpg` (ed25519)
fuer apt und `forgeiec-rpm.asc` (RSA-4096) fuer rpm. Der Unterschied ist
nicht kosmetisch — RHEL 9 liefert `rpm` 4.16, dessen interner PGP-Parser
ed25519 nicht verifizieren kann.

arm64 auf der RPM-Seite fehlt bewusst: der Cross-Compile-Pfad der CI ist
an Debian-Pakete gebunden, die es auf Enterprise Linux nicht gibt.

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
