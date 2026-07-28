---
title: "Tongs — modulare Feldbus-Bridges mit Fault-Modell"
date: 2026-05-05
summary: "Pro Protokoll ein eigener Daemon, einheitliches Status-Wire-Format, Diagnose-Bits aus dem FDD — kein Vendor-Plugin-Wildwuchs"
components: [studio, tongs, anvild]
---

{{< components "studio,tongs,anvild" >}}

## Worum es geht

Eine SPS-Plattform ist nur so gut wie ihre Feldbus-Anbindung. Aber
jeder Bus ist anders: Modbus-TCP hat keine echte Diagnose, EtherCAT
hat einen vollstaendig getakteten Slave-Zustandsautomat, Profibus
hat seine eigenen Fault-Klassen, EthernetIP hat CIP-Connections.

**Tongs** loest das mit einer **Plug-in-Familie**: pro Protokoll
ein eigener Daemon, gesteuert von anvild, mit einer **einheitlichen
Fault-Schicht** und **strukturierten Diagnose-Bits** aus den
Geraete-FDDs. Statt eines Mega-Drivers mit allen Protokollen
drin gibt es eine **modulare Komponenten-Familie**.

---

## Pro Protokoll ein Daemon

| Daemon | Protokoll | Status |
|---|---|---|
| `tongs-modbustcp` | Modbus TCP Master + Slave-Mode | produktiv |
| `tongs-ethercat` | EtherCAT-Master mit DC-Sync | in Arbeit |
| `tongs-profibus` | Profibus DP/PA | geplant |
| `tongs-ethernetip` | EtherNet/IP CIP | geplant |

Alle laufen unter dem **gleichen** anvild-Subprozess-Manager.
Lifecycle, Logging, Auto-Restart — gemeinsam, nicht pro Protokoll
neu erfunden.

---

## Einheitliches Fault-Modell

Spec `tongs-platform-v1.md` §5 definiert eine **gemeinsame
Fault-Stufung** ueber alle Bridges:

| Stufe | Bedeutung |
|---|---|
| `OK` | Geraet kommuniziert, keine Stoerungen |
| `WARN` | Funktional, aber Diagnose-Bits zeigen Vor-Stoerung |
| `FAULT` | Geraet kommuniziert, aber Schutzfunktion ausgeloest |
| `OFFLINE` | Geraet antwortet nicht |
| `UNKNOWN` | Bus-Status nicht ermittelbar (z.B. Scanner aus) |

Wird **einheitlich** in Studio + anvild gemeldet — egal ob das
darunter Modbus, EtherCAT oder Profibus ist. Operator muss nicht
fuer jeden Bus eine eigene Fehler-Tabelle lernen.

Aufruf via MCP: `bellows.protocol_status` liefert pro Segment den
aktuellen Fault-Stand inklusive Diagnose-Bits.

---

## Diagnose-Bits — strukturiert, nicht freier Text

Bei Hersteller-Geraten (z.B. Weidmueller-Busklemmen) gibt es
**konkrete Diagnose-Bits** in den Status-Bytes:

- Bit 0: Modul fehlt
- Bit 1: Kurzschluss am Ausgang
- Bit 2: Drahtbruch
- Bit 3: Versorgungsspannung ausserhalb Spec
- …

Diese Bits stehen im **FDD** (Field Device Description) des
Herstellers. ForgeIEC Studio:

1. Importiert die FDDs (auch mit eingebettetem PDF-Datenblatt)
2. Parsed die `<DiagnosticDecode>`-Sektionen
3. Stellt pro Bit Bedeutung + Schweregrad in Studio-Diagnose-Tab dar
4. Macht die aufgeloesten Bits per `catalog.diag_bits` MCP-Tool
   abrufbar

KI-Diagnose-Loop: „Warum schaltet `Motor_Bereit` nicht?" → KI ruft
`bellows.protocol_status` + `catalog.diag_bits` und kann
**klartext-antworten** „Modul `Stachelbeere` meldet Drahtbruch am
Ausgang 3".

---

## Pro Segment ein eigener Daemon-Prozess

Architektur-Vorteil: **Crashed eine Bridge nicht den ganzen
Master**. Wenn die EtherCAT-Bridge gegen einen frischen Slave-
Bug laeuft und stirbt, laufen Modbus + Profibus + die PLC-Logik
ungestoert weiter. anvild startet den abgestuerzten Bridge-Daemon
automatisch neu.

Das ist anders als bei monolithischen Runtimes wo ein Treiber-
Fault die ganze Maschine schlachtet.

---

## Bus-Konfiguration in `.forge`

Im `.forge`-Projekt-Format liegen Bus-Segmente strukturiert
abgelegt:

```toml
[[bus_segments]]
name = "Modbus_HMI"
protocol = "modbustcp"
settings.host = "192.168.1.50"
settings.port = 502

[[bus_segments.devices]]
name = "Stachelbeere"
fdd_path = "catalog/weidmueller/UR20-FBC-PN-IRT-V2.fdd"
```

Studio rendert das als Bus-Baum, generiert Codegen + auto-rolt
beim Save den passenden tongs-Bridge-Daemon ein.

IEC-Zugriff im ST-Code mit klarem 5-Level-Namespace:
`anvil.<segment>.<device>.Status.<var>` — z.B.
`anvil.Modbus_HMI.Stachelbeere.Status.WireBreak`.

---

## Plus: Anvil ABI-Probe — kein Versions-Roulette mehr

Tongs-Bridges sprechen mit anvild ueber **Anvil-Shared-Memory**.
Bei Versionsmischung zwischen anvild + Bridge konnten frueher
**still inkonsistente Daten** auftreten — Bridge schreibt eine
ABI-Variante A, anvild liest Variante B, niemand bemerkt es.

Mit der **ABI-Probe** (commit `7653cc5` + `9b17adc`) wird der
Type-Hash der SHM-Topics beim Connect verifiziert. Mismatch wirft
sofort eine **Studio-Warnung** mit konkretem Versions-Vergleich
— statt stiller Daten-Korruption.

---

## Was die Commits getragen haben

- `83fe7d4` — `anvil.*` Tool-Familie (4 Tools)
- `3c61445` — `bellows.protocol_status` + `tasks.cycle_overview`
- `9cc6dcd` — Force-Gate-Layer-1-3 (auch Bus-IO betreffend)
- `5dc087c` — FDD-Diagnostic-Bit-Resolver
- `5fe1e69` — Module-Picker-Filter via `<ModuleProtocol>` im
  Coupler-FDD
- `66923df` — Weidmueller-FDDs self-contained mit CDATA-PDFs +
  Git-LFS
- `6774397` — FDD-Editor: Diagnostics-Tab + Documents-Tab
- `7653cc5`, `9b17adc` — Anvil-ABI-Probe Layer 3a/3b
- `21759e7` — MCP-4a Remote-Bind macht Bus-Diagnose ueber Distanz
  moeglich

Spec: `documentation/architecture/tongs-platform-v1.md`
+ `bus-system-v1.md` + `anvil-platform-v2.md` §13.

---

## Wo Sie das nutzen

| Setup | Was Sie konfigurieren |
|---|---|
| Modbus-TCP an einer SPS | `tongs-modbustcp` + Geraet im Bus-Tab anlegen |
| Mehrere Protokolle gemischt | je ein `tongs-*` pro Protokoll, anvild orchestriert |
| Diagnose im laufenden Betrieb | `bellows.protocol_status` per MCP oder im Studio-Bus-Panel |
| Geraet wechseln (Stachelbeere → Birne) | FDD austauschen, regenerieren, deployen |

---

## Wo es konkret nachzulesen ist

- [Bus-Konfiguration](/help/bus-config/)
- [MCP-Tool-Familien: anvil + bellows + bus-system](/help/ai/tools/)
- Spec: `documentation/architecture/tongs-platform-v1.md`
  (Source-Tree)
