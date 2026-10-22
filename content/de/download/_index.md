---
title: "Download"
summary: "Alle ForgeIEC-Komponenten — APT-Repository, Direkt-Downloads, Quellcode"
---

{{< callout type="note" title="Stand: Vorabversion 0.2" >}}
Alle Pakete sind Vorabversionen der Reihe 0.2 (aktuell 0.2.2). Im
produktiven Einsatz (Pilotbetrieb) ist der ST-Editor. Je Release
kommt eine IEC-Sprache hinzu: 0.3 LD, 0.4 FBD, 0.5 SFC; IL ist
abgekündigt. Siehe [Roadmap](/de/roadmap/).
{{< /callout >}}

## ForgeIEC-Komponenten im Überblick

ForgeIEC besteht aus mehreren Komponenten. Welche Sie brauchen,
hängt von Ihrer Rolle:

| Rolle | Komponente | Wo installieren |
|---|---|---|
| **SPS-Programmierer / Anwender** | `forgeiec-studio` | Workstation |
| **Inbetriebnehmer** | `forgeiec-anvil-server` — der Anvil-Server (anvild); Dienst `forgeiec-anvil-server.service`, Programm `anvil-server` | Ziel-SPS |
| **Modbus TCP** | im Paket `forgeiec-anvil-server` enthalten | Ziel-SPS |
| **EtherCAT / PROFIBUS / EtherNet/IP** | Gerüst, ebenfalls in `forgeiec-anvil-server` — Protokoll in Arbeit | Ziel-SPS |
| **Bedienoberfläche (HMI, Vorschau)** | `forgeiec-hearth-server` | Ziel-SPS |
| **Bedien-Panel** | `forgeiec-screen-wayland` oder `-xorg` | Panel-Hardware |
| **OPC-UA-Gateway** | `forgeiec-bellows-server` — *ruht, ohne Wartung* | — |

---

## Installation aus dem Paket-Repository

ForgeIEC wird als signiertes Debian-Repository unter
`apt.forgeiec.io` und als signiertes RPM-Repository unter
`rpm.forgeiec.io` bereitgestellt — signierte Pakete aus einer
automatisierten CI. Einrichtung ist einmalig pro Workstation bzw.
Ziel-SPS — wählen Sie Ihre Distribution aus:

{{< distro-install >}}

Danach Komponenten einzeln installieren:

```bash
# Workstation
sudo apt install forgeiec-studio          # ForgeIEC Studio
sudo apt install forgeiec-fdd-data        # Gerätebeschreibungen (empfohlen)

# Ziel-SPS
sudo apt install forgeiec-anvil-server    # SPS-Runtime (Anvil-Server + alle tongs-*)
sudo apt install forgeiec-hearth-server   # Bedienoberfläche (Vorschau)

# Bedien-Panel
sudo apt install forgeiec-screen-wayland  # Kiosk unter Wayland
sudo apt install forgeiec-screen-xorg     # Kiosk unter X11
```

Auf RPM-Systemen heißen die Befehle `sudo dnf install …` bei sonst
gleichen Paketnamen — welche Pakete es dort gibt, zeigt die Tabelle
unten (die Runtime noch nicht).

Die Bus-Bridges (`tongs-modbustcp`, `tongs-ethercat`, `tongs-profibus`,
`tongs-ethernetip`) sind **keine** eigenen Pakete — sie liegen im Paket
`forgeiec-anvil-server` und werden vom Anvil-Server gestartet.

Das Paket `forgeiec-bellows-server` (OPC-UA-Gateway) liegt weiter im
APT-Repository, **ruht aber** — es wird derzeit nicht entwickelt und
nicht gewartet.

Updates folgen dem normalen `apt update && apt upgrade`-Zyklus —
keine manuellen `.deb`-Dateien nötig.

---

## Unterstützte Plattformen

### Debian / Ubuntu (`apt.forgeiec.io`)

| Paket | Architekturen | Suites |
|---|---|---|
| `forgeiec-studio` | amd64, arm64 | bookworm, trixie, noble |
| `forgeiec-fdd-data` | architekturunabhängig | bookworm, trixie, noble |
| `forgeiec-anvil-server` | amd64, arm64, armhf | bookworm, trixie, jammy, noble |
| `forgeiec-hearth-server` | amd64, arm64, armhf | bookworm, trixie, jammy, noble |
| `forgeiec-screen-wayland` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-screen-xorg` | amd64, arm64 | bullseye, bookworm, trixie, jammy, noble |
| `forgeiec-bellows-server` (ruht) | amd64, arm64, armhf | bookworm, trixie, jammy, noble |

Suite-Zuordnung: `bullseye` = Debian 11, `bookworm` = Debian 12,
`trixie` = Debian 13, `jammy` = Ubuntu 22.04, `noble` = Ubuntu 24.04.
`armhf` (ARMv7) gibt es für die Runtime, Hearth und die
Gerätebeschreibungen.

### Enterprise Linux / Fedora (`rpm.forgeiec.io`)

| Paket | Architekturen | Distributionen |
|---|---|---|
| `forgeiec-studio` | x86_64, aarch64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-fdd-data` | x86_64, aarch64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-hearth-server` | x86_64 | AlmaLinux 9 (`el9`) |
| `forgeiec-screen-wayland` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |
| `forgeiec-screen-xorg` | x86_64 | AlmaLinux 9 (`el9`), Fedora 44 |

**Runtime als RPM: noch nicht verfügbar.** `forgeiec-anvil-server`
gibt es derzeit nur als Debian-Paket.

<!-- ENTWURF: RPM-Tabelle nach Audit W-09 (Messung el9/x86_64, el9/aarch64, fedora-44/aarch64); fedora-44/x86_64 wurde im Audit nicht einzeln aufgeführt. Vor Veröffentlichung gegen rpm.forgeiec.io prüfen. -->

Es gibt **zwei verschiedene Signierschlüssel**: `forgeiec.gpg` (ed25519)
für apt und `forgeiec-rpm.asc` (RSA-4096) für rpm. Der Unterschied ist
nicht kosmetisch — RHEL 9 liefert `rpm` 4.16, dessen interner PGP-Parser
ed25519 nicht verifizieren kann.

### Windows

Einen Windows-Build von ForgeIEC Studio gibt es, die Windows-CI läuft.
Einen öffentlichen Download gibt es noch nicht — den Installer
erhalten Sie **auf Anfrage** an blacksmith@forgeiec.io.

---

## Quellcode

Der Quellcode steht unter der AGPL-3.0-or-later (der in Ihr Projekt
gelinkte Teil unter Apache-2.0). **Die Repositories sind nicht
öffentlich einsehbar** — Einsicht auf Anfrage: Schicken Sie Ihren
SSH-Public-Key an blacksmith@forgeiec.io, wir schalten ihn frei.
Danach stehen Ihnen unter anderem diese Repositories offen:

- **ForgeIEC Studio**: `ForgeIEC/forgeiec-studio`
- **Anvil-Server (anvild)**: `ForgeIEC/anvil`
- **Tongs (Bus-Bridges)**: `ForgeIEC/tongs-core` und je Protokoll `ForgeIEC/tongs-*`
- **Hearth**: `ForgeIEC/hearth`
- **bellowsd** (ruht): `ForgeIEC/bellows`
- **Webseite**: `ForgeIEC/forgeiec-website`

Die normativen Spezifikationen liegen im Repository
`forgeiec-studio` unter `documentation/architecture/`.

---

## Bauen aus dem Quellcode

```bash
# Repository klonen (mit Submodules) — nur über SSH, nach
# Freischaltung Ihres SSH-Public-Keys
git clone --recurse-submodules ssh://git@git.forgeiec.io/ForgeIEC/forgeiec-studio.git
cd forgeiec-studio

# Studio bauen
cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc)

# Deployen auf das lokale System
./deploy.sh all
```

Voraussetzungen (Debian 12/13, Ubuntu 24.04), so wie die CI sie
installiert:

```bash
sudo apt install build-essential cmake ninja-build pkg-config git \
  qt6-base-dev qt6-base-dev-tools qt6-tools-dev qt6-tools-dev-tools \
  libqt6svg6-dev libqt6sql6-sqlite libqt6charts6-dev libqt6opengl6-dev \
  libgl-dev libssl-dev libre2-dev libargon2-dev libsqlite3-dev libxml2-dev \
  libtomlplusplus-dev libprotobuf-dev protobuf-compiler \
  libgrpc++-dev protobuf-compiler-grpc \
  forgeiec-libforge-mcp-dev   # aus dem ForgeIEC-APT-Repository
# Debian 13 zusätzlich: qt6-svg-plugins
```

Maßgeblich ist die Paketliste in `.forgejo/workflows/linux.yml` im
Repository.

---

## Beispielprojekte

Mit ForgeIEC Studio ausgelieferte Beispiele (Studio: `File -> Open Example`):

| Beispiel | Inhalt |
|---|---|
| Blinky | Blinklicht mit TON/TOF |
| Star-Delta Reversing Starter | Stern-Dreieck-Wendeschaltung |
| Knight Rider | Lauflicht, 16 Bit |
| Traffic Light | Ampelsteuerung |
| PID Controller | PID-Temperaturregelung (Funktion) |
| Weekly Timer | Wochenschaltuhr (Funktionsbaustein) |
| FOC Demo | Feldorientierte Regelung, 3-Phasen-Umrichter |
| Tankanlage | Tankanlage mit Hearth-Bedienoberfläche |
| Conveyor Pick & Place | Förderband mit Greifer |
| Compressor Station | Kompressorstation |
| Axis Control | Achssteuerung mit verschachteltem STRUCT |

---

## Nächste Schritte

- [Erste Schritte mit ForgeIEC Studio](/de/help/)
- [KI-Helfer einrichten](/de/help/ai/)
- [Bus-Konfiguration](/de/help/bus-config/)
- [News + Release-Notes](/de/news/)
