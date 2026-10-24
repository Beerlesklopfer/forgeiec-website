---
title: "Bus-Konfiguration"
summary: "Wie ForgeIEC Studio Feldbusnetze + Geräte + Variablen-Bindung verwaltet — von der Hersteller-FDD bis zum IEC-ST-Zugriff"
---

{{< components "studio,tongs,anvild" >}}

## Worum es geht

Die Bus-Konfiguration in ForgeIEC Studio beschreibt die **physische
Topologie einer Anlage**: welche Feldbus-Netze laufen auf welcher
Schnittstelle, welche Geräte hängen daran, welche Variablen sind
mit welchen Geräte-Registern verknüpft. Sie wird Teil der
`.forge`-Projektdatei und treibt die Codegen-Pipeline + den
Bridge-Daemon-Lifecycle.

```
.forge-Projekt
  Segmente (Feldbus-Netze)
    Devices (Geraete)
      Module (bei modularen Couplern)
        Variablen (gebunden ueber den Adress-Pool)
```

Pro Segment startet `anvild` **genau einen Bridge-Daemon**
(`tongs-modbustcp`, `tongs-ethercat`, ...). Ein Crash in der
EtherCAT-Bridge schlachtet **nicht** Ihre Modbus-Bridge — jeder
Bridge-Daemon wird einzeln verwaltet + bei Bedarf auto-neu-gestartet.

---

## IEC-ST-Zugriff: 5-Level-Namespace

Variablen aus dem Bus-System erreichen Sie im ST-Code über einen
klaren 5-Level-Namespace:

```
anvil.<Segment>.<Device>.<Struct>.<Variable>
```

Beispiel:

```text
IF anvil.Halle1.Stachelbeere.Status.WireBreak THEN
    Motor_Bereit := FALSE;
END_IF;

anvil.Halle1.Maibeere.IO.DO_1 := Schalter_State;
```

Das ist **kein** flacher Variablen-Pool wie in vielen klassischen
IDEs, sondern eine **echte Hierarchie** die der Codegen aus der
Bus-Topologie ableitet. Tree-sitter-getypt — Autocomplete im
ST-Editor zeigt Ihnen welche Struct-Member ein Gerät hat.

Status-Variablen (`Status.<Var>`) sind **auto-generierte TYPE-
Member**, kein Eintrag im Pool. Sie kommen aus der `<DiagnosticDecode>`-
Sektion der FDD des Herstellers (siehe nächster Abschnitt).

---

## Hersteller-Daten als First-Class

Statt PDF-Datenblätter und FDD-Files getrennt zu pflegen, packt
ForgeIEC alles in **eine** FDD-Datei pro Gerät:

| Element | Inhalt |
|---|---|
| `<Vendor>` | Hersteller-Daten + Lizenz |
| `<Identification>` | Bestellnummer, Produktname |
| `<ModuleProtocol>` | Welche Module dieser Coupler versteht |
| `<DiagnosticDecode>` | Status-Bit-Definitionen (DE + EN) |
| `<Document>` | CDATA-eingebettetes PDF-Datenblatt |

Folgen:

- **Module-Picker** zeigt nur Module die zum Coupler passen — kein
  Raten in einer 200-Einträge-Liste
- **Diagnose-Bits** sind im Properties-Panel mit Live-Werten +
  Bedeutung sichtbar
- **Datenblatt** im Documents-Tab — kein externes PDF-Programm
- **Eine Datei = ein vollständiges Gerät** — Maschine als Tarball
  weitergeben enthält automatisch die Hersteller-Info

Eigene FDDs anlegen über `File → New FDD` (Diagnostics-Tab +
Documents-Tab im FDD-Editor).

Mehr zum FDD-System: [News-Eintrag](/news/catalog-fdd/).

---

## Bridge-Fault-Modell — einheitlich

Alle Bridges (Modbus, EtherCAT, Profibus, EthernetIP) melden ihren
Status nach **derselben** 5-stufigen Skala:

| Stufe | Bedeutung |
|---|---|
| `OK` | Gerät kommuniziert, keine Störungen |
| `WARN` | Funktional, aber Diagnose-Bits zeigen Vor-Störung |
| `FAULT` | Gerät kommuniziert, Schutzfunktion ausgelöst |
| `OFFLINE` | Gerät antwortet nicht |
| `UNKNOWN` | Bus-Status nicht ermittelbar (z.B. Scanner aus) |

Abrufbar im Studio (Bus-Panel-Statusspalte) oder per MCP:

```
bellows.protocol_status — Snapshot aller Segmente + Devices
catalog.diag_bits       — aufgeloeste Diagnose-Bits pro Device
project.bus_topology    — komplette Topologie als JSON
```

Operator + KI-Helfer sehen sofort welches Gerät wackelt — egal
welches Protokoll darunter läuft.

---

## Variablen-Anbindung

I/O-Variablen werden **nicht** im Device-Eintrag aufgelistet.
Stattdessen trägt jede Variable im Adress-Pool ein
`busBinding`-Attribut, das auf die Device-ID zeigt:

```
FVariable
  name:    "DI_1"
  address: "%IX0.0"     ← physisch, vom Pool-Allokator
  scope:   anvil.Stachelbeere
  flags:
    bellows_export: false    ← in HMI/OPC-UA exportieren? (bellowsd ruht)
    force_enabled:  false    ← darf forciert werden? (Force-Sperre)
    monitor_enabled: true
  busBinding:
    deviceId:       <UUID-of-Stachelbeere>
    modbusAddress:  0
    count:          1
```

Wenn Sie eine Variable an ein Device **binden**, wechselt die Adresse
automatisch von `%MX` (Merker) nach `%IX`/`%QX` (physisch). Beim
Entbinden geht sie zurück in den Merker-Bereich.

### Per-Variable Sicherheits-Flags

Drei separate Flags steuern was eine Variable darf — alle Default OFF:

- **`bellows_export`** — Variable wird über bellowsd als
  OPC-UA-Knoten + Modbus-TCP-Server-Coil sichtbar (HMI-Anbindung)
- **`force_enabled`** — `F`-Checkbox darf in der GUI gesetzt
  werden; ohne dieses Flag ist Forcing schon im Code-Generator
  abgeschaltet (erste Stufe der [Force-Sperre](/de/help/ai/security/): dreifach
  gesperrt — Codegen, Runtime, Editor; für die KI eine vierte Sperre)
- **`monitor_enabled`** — Variable erscheint im Live-Monitor-Stream
  (sonst nur lokal in der PLC)

Das ist die Granularität: **kein** „Alles oder Nichts" — jede
Variable ist einzeln gegated.

---

## Setup-Workflow im ForgeIEC Studio

| Schritt | Aktion |
|---|---|
| **1. Segment anlegen** | Bus-Panel → `+ Segment` → Protokoll + Interface eintragen |
| **2. Device dazu** | Rechtsklick aufs Segment → `+ Device` → FDD aus Catalog wählen |
| **3. Module (bei Coupler)** | Rechtsklick aufs Device → `+ Module` (gefiltert nach `<ModuleProtocol>`) |
| **4. Variablen binden** | Im Variables-Tab `F`-Spalte / Bus-Binding-Editor — oder per MCP `project.write.set_variable_scope` |
| **5. Flags setzen** | `B`-Checkbox für Bellows-Export, `F` für Force, `M` für Monitor |
| **6. Save + Deploy** | `Build → Compile and Upload` — anvild startet die Bridges + spawnt die PLC |

Editieren wahlweise im **Properties-Panel** (Einfach-Klick, sofort
gespeichert) oder im **modalen Dialog** (Doppel-Klick, OK/Cancel).

---

## Bus-Konfiguration im `.forge`-XML

Persistiert wird die Bus-Konfiguration als
`<addData>`-Erweiterung auf Projekt-Ebene (PLCopen-TC6-konform):

```xml
<project>
  <types>...</types>
  <instances>...</instances>

  <addData>
    <data name="https://forgeiec.io/v2/bus-config"
          handleUnknown="discard">
      <fi:busConfig xmlns:fi="https://forgeiec.io/v2">

        <fi:segment id="a3f7c2e1-..."
                    protocol="modbustcp"
                    name="Halle1"
                    interface="eth0"
                    bindAddress="192.168.24.100/24"
                    pollIntervalMs="100">

          <fi:device deviceId="b7f8d3a2-..."
                     hostname="Stachelbeere"
                     ipAddress="192.168.24.25"
                     slaveId="1"
                     catalogRef="weidmueller/UR20-FBC-PN-IRT-V2"/>

        </fi:segment>

      </fi:busConfig>
    </data>
  </addData>
</project>
```

`handleUnknown="discard"` sorgt dafür dass PLCopen-konforme
Werkzeuge die nichts mit ForgeIEC anfangen können, die Sektion
ignorieren **ohne Fehler**. Umgekehrt liest ForgeIEC unbekannte
`<addData>`-Blöcke und bewahrt sie beim Speichern.

Detail-Schema:
- [Bus-Segmente](segments/) — Felder pro Segment + protokoll-
  spezifische Settings
- [Bus-Devices](devices/) — Geräte + Module + per-Device-Overrides
- [`.forge`-Dateiformat](../file-format/) — XML-Wurzel + Vendor-
  Extensions

---

## Unterstützte Protokolle

| Protokoll | `protocol`-Wert | Medium | Bridge | Status |
|---|---|---|---|---|
| Modbus TCP | `modbustcp` | Ethernet | `tongs-modbustcp` | {{< status "use" "verfügbar" >}} |
| Modbus RTU | `modbusrtu` | RS-485 | `tongs-modbusrtu` | {{< status "use" "verfügbar" >}} |
| LoRaWAN | — | Funk | `tongs-lorawan` | {{< status "wip" "in Arbeit (Schwerpunkt)" >}} |
| EtherCAT | `ethercat` | Ethernet (DC) | `tongs-ethercat` | {{< status "wip" "Gerüst, in Arbeit" >}} |
| PROFIBUS DP | `profibus` | Feldbus | `tongs-profibus` | {{< status "wip" "Gerüst, in Arbeit" >}} |
| EtherNet/IP | `ethernetip` | Ethernet (CIP) | `tongs-ethernetip` | {{< status "wip" "Gerüst, in Arbeit" >}} |

---

## Weiterführende Themen

- [Bus-Segmente](segments/) — Felder + Protokoll-Settings
- [Bus-Devices](devices/) — Geräte-Konfiguration + FDD-Integration
- [Catalog + FDD-System](/news/catalog-fdd/) — Hersteller-Daten
  als First-Class
- [Tongs-Bridge-Familie](/news/tongs-bridges/) — Fault-Modell +
  Bridge-Lifecycle
- [Sicherheits-Modell](/help/ai/security/) — die Force-Sperre
- [`.forge`-Dateiformat](../file-format/)
