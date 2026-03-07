---
title: "Plattform"
description: "Die ForgeIEC Plattform -- alle Komponenten fuer die industrielle Automatisierung"
weight: 10
---

## Die ForgeIEC Plattform

ForgeIEC ist eine vollstaendige Plattform fuer die industrielle
Automatisierung -- von der Entwicklungsumgebung bis zum Leitsystem. Jede
Komponente traegt den Namen eines Schmiedewerkzeugs, denn ForgeIEC ist
fuer die Industrie geschmiedet.

---

### Forge Studio

**IEC 61131-3 Entwicklungsumgebung**

Die professionelle IDE fuer SPS-Programmierung. Alle fuenf IEC-Sprachen,
grafische und textuelle Editierung, lokale Kompilierung, Remote-Deployment.
Gebaut mit C++17 und Qt6.

[Mehr erfahren](forge-studio/)

---

### Anvil

**Echtzeit-SPS-Laufzeitumgebung**

Der Runtime-Daemon, der IEC-Programme auf dem Zielsystem ausfuehrt.
Zero-Copy-Kommunikation zwischen Runtime und Protokoll-Bridges ueber
die Anvil Shared-Memory-Technologie.

[Mehr erfahren](anvil/)

---

### Bellows

**OPC-UA-Gateway** -- In Entwicklung

Standardisierte Maschine-zu-Maschine-Kommunikation nach OPC-UA-Standard.
Transparente Integration von Automatisierungssystemen in die bestehende
IT-Infrastruktur.

[Mehr erfahren](bellows/)

---

### Hearth

**SCADA/HMI** -- In Entwicklung

Prozessvisualisierung und Mensch-Maschine-Schnittstelle fuer die industrielle
Ueberwachung. Echtzeit-Dashboards, Datenhistorie, Alarmmanagement.

[Mehr erfahren](hearth/)

---

### Spark

**Zenoh-Tunnel**

Netzwerk-Bridge von Edge zu Cloud auf Basis des Zenoh-Protokolls. Sichere
Verbindung zwischen lokalen SPS-Systemen und Cloud-Diensten, ohne VPN,
ohne komplexe Konfiguration.

[Mehr erfahren](spark/)

---

### Tongs

**Feldbus-Bridges**

Protokoll-Bridges fuer Modbus TCP/RTU, EtherCAT und Profibus DP. Jede Bridge
laeuft als eigenstaendiger Prozess, ueberwacht und automatisch neu gestartet
durch den Runtime.

[Mehr erfahren](tongs/)

---

### Ledger

**Auftragsmanagement** -- In Entwicklung

MES-Integration fuer die Verwaltung von Produktionsauftraegen,
Produktionsverfolgung und Rueckverfolgbarkeit. Bruecke zwischen
Automatisierung und Produktionsplanung.

[Mehr erfahren](ledger/)

---

<div style="text-align:center; padding: 2rem;">

**Aufbauend auf OpenPLC** -- ForgeIEC basiert auf dem
[OpenPLC](https://autonomylogic.com/)-Projekt und ist vollstaendig kompatibel
mit dessen Dateiarchitektur. Bestehende OpenPLC-Projekte koennen direkt
geoeffnet und weiterentwickelt werden.

**Alle Komponenten sind Open Source. Keine Lizenzkosten. Keine Herstellerbindung.**

blacksmith@forgeiec.io

</div>
