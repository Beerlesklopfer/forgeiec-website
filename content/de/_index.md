---
title: "ForgeIEC"
---

<div style="text-align:center; padding: 3rem 1rem;">

# Geschmiedet fuer die Industrie.

**Eine IEC 61131-3 Entwicklungsumgebung in Industriequalitaet — Open Source, KI-nativ, ohne Vendor-Lock-In.**

[Download](/download/) · [Architektur](/help/ai/architecture/) · [News](/news/)

</div>

---

## Was ForgeIEC heute leistet

| Bereich | Status |
|---|---|
| **Alle 5 IEC-61131-3-Sprachen** — ST, IL, FBD, LD, SFC | produktiv |
| **Multi-Task-Scheduler** — echte pthread-Parallelitaet | produktiv |
| **Live-Diagnose** — Monitor + Oszilloskop mit Trigger, CSV-Aufnahme | produktiv |
| **Bus-System** — Modbus-TCP produktiv, EtherCAT in Arbeit, Profibus + EthernetIP geplant | gemischt |
| **Hersteller-Daten als First-Class** — FDDs mit eingebetteten PDFs + Diagnose-Bit-Aufloesung | produktiv |
| **KI-Helfer eingebaut** — ~80 typisierte MCP-Werkzeuge, 5 Personas | produktiv |
| **Team-Federation** — mehrere Workstations mit Caretaker-CA | MVP produktiv |
| **HMI / OPC-UA-Anbindung** ueber bellowsd | produktiv |
| **Reproduzierbare Builds** — signiertes APT-Repository, AGPL-3.0 | produktiv |

---

## Drei Saeulen

### 🛠️ ForgeIEC Studio — die IDE

Native C++/Qt6-Anwendung, alle fuenf IEC-Sprachen, Bus-Konfiguration,
Live-Monitor, Oszilloskop, KI-Helfer eingebaut. Multi-Workstation-
Federation ueber Trust-Store + Caretaker-Modell. Keine Browser-UI,
keine Cloud-Pflicht.

### 🔥 anvild — die Runtime

Rust/Tokio-Daemon auf der Ziel-SPS. Multi-Task, deterministische
Scan-Cycles, gRPC-Anbindung zum Studio, Subprocess-Manager fuer
die Bus-Bridges, Auto-Cleanup beim Startup.

### 🔧 tongs-* — Bus-Bridges

Pro Protokoll ein Daemon. Einheitliches Fault-Modell, FDD-getriebene
Diagnose-Bits, Anvil-Zero-Copy-IPC zwischen Bridge und Runtime,
Bridges koennen unabhaengig crashen + neu starten.

---

## Warum ForgeIEC?

Industrielle Automatisierung ist Schluesseltechnologie — und der
Zugang zu professionellen Werkzeugen wird durch Lizenzkosten und
proprietaere Systeme eingeschraenkt. ForgeIEC macht die Wertschoepfung
fuer jeden zugaenglich.

Drei Versprechen die wir halten:

- **Open Source (AGPL-3.0)** — Source einsehbar, Build reproduzierbar,
  Updates ueber signiertes APT-Repository
- **Vendor-neutral** — Hersteller-Daten als FDDs eingebunden, kein
  proprietaeres Geraete-Format, Migration-faehig
- **Industrie-Sicherheit** — 4-Layer-Defense fuer Force-Setzungen,
  Confirmation State Machine fuer jede schreibende Aktion, ehrliches
  Sampling-Limit-Modell statt Marketing-Versprechen

Mehr dazu in der [Founding-Story](/news/die-forgeiec-geschichte/) —
wie aus einem 2018er OpenPLC-Fork eine eigenstaendige Plattform wurde.

---

## Loslegen

```bash
# Editor + Runtime aus signiertem APT-Repository
sudo apt install forgeiec-studio forgeiec-anvil-server
```

Komplette Installations-Anleitung: [Download](/download/).

Erste Schritte mit dem KI-Helfer: [Hilfe](/help/ai/).

---

<div style="text-align:center; padding: 2rem;">

**Made for industry. Open by default.**

blacksmith@forgeiec.io

</div>
