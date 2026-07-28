---
title: "Hilfe"
summary: "Dokumentation und Ressourcen fuer ForgeIEC"
---

## Hilfe und Ressourcen

Willkommen im Hilfebereich von ForgeIEC. Hier finden Sie Informationen
zu den Grundlagen unseres Projekts und unserer Philosophie.

---

## Themen

### [Online-Hilfe](/help/online/)

Einstiegspunkt fuer die kontext-sensitive Hilfe aus dem Editor.
F1 oeffnet aus dem Editor heraus genau die passende Seite hier
auf der Website. URL-Schema und Themen-Slugs sind dort beschrieben.

### [FAQ](/help/faq/)

Wachsende Sammlung haeufiger Fragen + Loesungen aus der Praxis.
Beginnt mit einem klassischen Symptom (Variable haengt trotz frischem
Deploy) und waechst mit jedem neu beobachteten Fall.

### [KI-Integration](/help/ai/)

Wie Sie den eingebauten KI-Helfer in ForgeIEC Studio nutzen:
Personas, Provider (ChatGPT / Claude / lokal), Bedienung im Alltag,
Sicherheits-Modell, Team-Mode fuer mehrere Workstations. Plus eine
Architektur-Tiefe fuer Security-Auditoren.

### [MCP-Protokoll](/help/mcp/)

Die Protokoll-Schicht unter dem KI-Helfer — fuer Applikations-
ingenieure die eigene Skripte/Werkzeuge anbinden, und fuer
IT/Betrieb die deployen, monitoren und troubleshooten.

---

## Weitere Bereiche

- [Download](/download/) — alle Komponenten + APT-Setup
- [News](/news/) — Release-Notes + technische Updates

### [Projekt-Dateiformat (.forge)](/help/file-format/)

Aufbau einer ForgeIEC-Projektdatei: PLCopen-XML-Wurzel, POU-Typen,
Adress-Pool, ForgeIEC-Erweiterungen ueber `<addData>` und ST-Sprach-
zusaetze (Bit-Zugriff, 3-Level-Qualifikation).

### [Bus-Konfiguration](/help/bus-config/)

PLCopen-XML-Schema fuer die industrielle Feldbus-Konfiguration im `.forge`-Projekt.
Segmente, Devices, Variablen-Binding und IEC-Adressvergabe.

### [Testabdeckung](/help/tests/)

117 automatisierte Tests pruefen den vollstaendigen IEC 61131-3 Sprachvorrat,
alle 132 Standard-Bausteine und das Multi-Task-Threading-System.

### [Open Source Philosophie](/help/open-source/)

Der Gedanke hinter Open Source geht weit ueber Software hinaus — es ist
eine Bewegung, die Wissen befreit und Innovation demokratisiert.

---

## Erste Schritte

ForgeIEC besteht aus zwei Komponenten:

1. **ForgeIEC Editor** (`forgeiec`) — Die Entwicklungsumgebung auf Ihrer Workstation
2. **ForgeIEC Daemon** (`anvild`) — Das Laufzeitsystem auf der Ziel-SPS

### Installation aus dem ForgeIEC APT-Repository

ForgeIEC wird als signiertes Debian-Repository unter
`apt.forgeiec.io` bereitgestellt. Die Einrichtung erfolgt einmalig
auf jeder Workstation bzw. Ziel-SPS:

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

Anschliessend kann jedes ForgeIEC-Paket mit dem Standard-Paket-
Manager installiert werden:

```bash
# Editor (Workstation)
sudo apt install forgeiec-studio

# Daemon (Ziel-SPS)
sudo apt install forgeiec-anvil-server
```

Updates folgen automatisch dem normalen `apt update && apt upgrade`
Lebenszyklus — es ist keine manuelle `.deb`-Datei noetig.

### Unterstuetzte Plattformen

| Komponente | Architekturen | Debian-/Ubuntu-Suites |
|------------|---------------|------------------|
| Editor     | amd64, arm64  | bookworm, trixie, noble |
| Daemon     | amd64, arm64  | bookworm, trixie, jammy, noble |
| Bridges    | amd64, arm64  | bookworm, trixie, jammy, noble |
| Hearth     | amd64, arm64  | bookworm, trixie, jammy, noble |

Das Bedien-Panel (`forgeiec-screen-*`) gibt es zusaetzlich als RPM
fuer AlmaLinux 9 und Fedora 44 unter `rpm.forgeiec.io`. Die
vollstaendige Paket-/Plattform-Matrix steht auf der
[Download-Seite](/download/).

### Kontakt

Bei Fragen wenden Sie sich an: blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**Die Dokumentation waechst mit dem Projekt.**

blacksmith@forgeiec.io

</div>
