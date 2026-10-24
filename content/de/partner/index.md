---
title: "Partner"
summary: "Gemeinsam die Zukunft der Automatisierung schmieden"
---

## Partnerschaft bei ForgeIEC

ForgeIEC ist ein Open-Source-Projekt, das von der Überzeugung lebt,
dass industrielle Automatisierung für alle zugänglich sein muss.
Wir suchen Partner, die diese Vision teilen und bereit sind, die
Zukunft der Automatisierung aktiv mitzugestalten.

---

## Unsere Source-Repositories

Die Code-Basis liegt im **Forgejo** unter `git.forgeiec.io`.
Die Repositories sind nicht öffentlich einsehbar; der Quellcode steht
unter der AGPL, Einsicht auf Anfrage. Der Zugriff läuft über SSH:
Sie schicken uns Ihren SSH-Public-Key, wir schalten ihn frei. Danach
können Sie den Code vor einer Bewerbung durchsehen. Beiträge Dritter
werden erst angenommen, wenn die Contributor License Agreement in
Kraft ist.

| Repository (`ssh://git@git.forgeiec.io/ForgeIEC/<name>.git`) | Was drin ist |
|---|---|
| **forgeiec-studio** | C++/Qt6-IDE + Bus-Konfig + MCP-Server |
| **anvil** | Rust/Tokio-SPS-Runtime, der Anvil-Server (anvild) |
| **tongs-core** und **tongs-*** | gemeinsamer Kern der Bus-Bridges und je Protokoll ein Repository |
| **hearth** | Bedienoberfläche (HMI), Vorschau |
| **screen** | Kiosk-Browser für Bedienpanels |
| **lib-forgeiecdom**, **forge-mcp** | Projektmodell-Bibliothek, MCP-Bibliothek |
| **fdd-files** | Gerätebeschreibungen (FDD) |
| **bellows** | OPC-UA-/HMI-Gateway — ruht |
| **forgeiec-website** | die Hugo-Seite, die Sie gerade lesen |

Die normativen Spezifikationen liegen im Repository
`forgeiec-studio` unter `documentation/architecture/`.

---

## Voraussetzungen

### Nachgewiesenes Open-Source-Engagement

Bewerber müssen bereits bewiesen haben, dass sie den Gedanken von
Open Source unterstützen. Das bedeutet:

- **Nachweisbare Beiträge** zu bestehenden Open-Source-Projekten
  (Commits, Pull Requests, Bug Reports, Dokumentation)
- **Öffentliches Profil** auf Plattformen wie GitHub, GitLab oder
  Codeberg
- **Aktive Teilnahme** an Open-Source-Communities — nicht nur
  Nutzung, sondern Mitgestaltung

Wir glauben, dass Taten mehr sagen als Worte. Wer Open Source nur
als Marketinginstrument betrachtet, ohne selbst beizutragen, passt
nicht zu unserer Philosophie.

### Gemeinsame Werte

- **Transparenz** — Offene Kommunikation, nachvollziehbare
  Entscheidungen
- **Zusammenarbeit** — Code Reviews, gemeinsame Architektur-
  Diskussionen, geteiltes Wissen
- **Qualität** — Dokumentierte Tests, sauberer Code,
  industrietaugliche Zuverlässigkeit
- **Langfristigkeit** — Partnerschaft ist kein Sprint, sondern ein
  Marathon

---

## Bereiche in denen wir konkret Unterstützung suchen

Wenn die Voraussetzungen oben für Sie passen — hier sind die
Subsysteme an denen wir besonders nach Mitstreitern suchen:

### 🔧 Bus-Bridges (tongs-*)

{{< components "tongs,anvild" >}}

- **tongs-lorawan** — Schwerpunkt: Funk-Sensorik für Landwirtschaft
  und weitläufige Anlagen (in Arbeit)
- **tongs-ethercat** — DC-Sync, Slave-State-Machine, ENI-XML-Import
- **tongs-profibus** — DP-Master, GSD-Import-Toolchain
- **tongs-ethernetip** — CIP-Connections, EDS-Import
- **tongs-can** — CANopen + J1939

Für EtherCAT, PROFIBUS und EtherNet/IP stehen Gerüst, Fault-Model und
IPC-Wire-Format — der protokollspezifische Teil fehlt.

### 🛠️ Studio-Editor-Features

{{< components "studio" >}}

- **LD-, FBD- und SFC-Editoren** — heute ist ST im Einsatz; LD, FBD
  und SFC sind für die Releases 0.3, 0.4 und 0.5 geplant. Grafische
  Sprachen brauchen eigene Tree-sitter-Grammatik + Canvas-Renderer.
- **Vendor-Catalog-Pflege** — mitgeliefert sind über 1 100
  Gerätebeschreibungen von Phoenix Contact, Beckhoff, Weidmüller,
  SALZ u. a. (Stand 22.10.2026). GSDML/EDS/ESI-Konverter sind
  willkommen.
- **Internationalisierung** — Übersetzungen des Studios; die Webseite
  wird derzeit auf Deutsch und Englisch gepflegt.

### 🏠 Bedienoberfläche (Hearth)

{{< components "hearth" >}}

- **Hearth** — die Bedienoberfläche liest die Prozessdaten direkt vom
  Anvil-Bus und ist als Vorschau verfügbar. Wer Erfahrung mit
  HMI-Gestaltung, Alarmierung oder Trendaufzeichnung hat, kann hier
  mitgestalten.

### 🔥 Runtime + Determinismus (Anvil-Server, anvild)

{{< components "anvild" >}}

- **Real-Time-Linux-Tuning** — PREEMPT_RT-Kernel, CPU-Pinning,
  Cache-Locality für Sub-Millisekunden-Cycle-Times
<!-- ENTWURF: Punkt "Rust+LLVM-Codegen (rusty)" entfernt — matiec ist abgelöst, ob rusty noch Plan ist, entscheidet der Eigentümer (Audit W-16). -->
- **Hardware-Targets** — Raspberry Pi, BeagleBone, industrielle
  x86, ARM-SBCs.

### 📚 Bildung + Dokumentation

{{< components "studio" >}}

- **Tutorials** — von „erstes Knight-Rider in 5 Minuten" bis
  „komplette Maschinensteuerung mit Modbus und LoRaWAN"
- **Beispiel-Projekte** — heute liefert das Studio 11 Beispiele mit;
  weitere aus der Praxis sind willkommen
- **Lehr-Curriculum** — Hochschulen die ForgeIEC als Lehr-IDE
  einsetzen wollen. Wir liefern Studio kostenlos, Dozenten bringen
  IEC-Curriculum.

---

## Was wir bieten

### Zugang zur ForgeIEC-Plattform

- Frühzeitiger Zugriff auf neue Features und Entwicklungszweige
- Direkter Draht zum Kernteam
- Möglichkeit, die Roadmap aktiv mitzugestalten

### Gemeinsame Entwicklung

- Gemeinsame Arbeit an industriellen Bussystem-Treibern
- Integration herstellerspezifischer Hardware
- Entwicklung branchenspezifischer Erweiterungen

### Technischer Support

- Priorisierte Fehlerbehebung
- Architektur-Beratung für eigene Erweiterungen
- Unterstützung bei der Integration in bestehende Systeme

---

## Formen der Partnerschaft

### Technologie-Partner

Hersteller von Automatisierungskomponenten, die ihre Hardware in
ForgeIEC integrieren möchten. Gemeinsame Treiberentwicklung,
Gerätekonfigurationen und Testverfahren.

### Integrations-Partner

Systemintegratoren und Ingenieursbüros, die ForgeIEC in
Kundenprojekten einsetzen. Praxiswissen fließt zurück in die
Entwicklung.

### Bildungs-Partner

Hochschulen und Ausbildungsstätten, die ForgeIEC in der Lehre
verwenden. Freier Zugang für den Bildungsbereich — die nächste
Generation von Automatisierungstechnikern sollte mit offenen
Werkzeugen lernen.

---

## Aktuell registrierte Partner

Stand 2026-05: noch keine externen Partner — die Plattform ist im
Aufbau-Sprint, Partner-Onboarding kommt sobald die ersten Subsystem-
APIs (Bridge-SDK, FDD-Format) stabilisiert sind.

Wenn Sie zu den ersten gehören wollen: siehe „Bewerbung" unten.

---

## Bewerbung

Sie möchten Partner werden? Schreiben Sie uns mit:

- Beschreibung Ihrer Organisation
- Links zu Ihren Open-Source-Beiträgen
- Ihre Motivation für eine Partnerschaft
- Konkreter Bereich, in dem Sie beitragen möchten
- Ihren SSH-Public-Key, wenn Sie den Code vorab durchsehen wollen

---

<div style="text-align:center; padding: 2rem;">

**Gemeinsam schmieden wir die Werkzeuge der Zukunft.**

blacksmith@forgeiec.io

</div>
