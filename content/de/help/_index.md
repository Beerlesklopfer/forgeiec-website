---
title: "Hilfe"
summary: "Dokumentation und Ressourcen für ForgeIEC"
---

## Hilfe und Ressourcen

Willkommen im Hilfebereich von ForgeIEC. Hier finden Sie Informationen
zu den Grundlagen unseres Projekts und unserer Philosophie.

---

## Themen

### [Online-Hilfe](/help/online/)

Einstiegspunkt für die kontext-sensitive Hilfe aus dem Editor.
F1 öffnet aus dem Editor heraus genau die passende Seite hier
auf der Website. URL-Schema und Themen-Slugs sind dort beschrieben.

### [FAQ](/help/faq/)

Wachsende Sammlung häufiger Fragen + Lösungen aus der Praxis.
Beginnt mit einem klassischen Symptom (Variable hängt trotz frischem
Deploy) und wächst mit jedem neu beobachteten Fall.

### [KI-Integration](/help/ai/)

Wie Sie den eingebauten KI-Helfer in ForgeIEC Studio nutzen:
Personas, Provider (ChatGPT / Claude / lokal), Bedienung im Alltag,
Sicherheits-Modell, Team-Mode für mehrere Workstations. Plus eine
Architektur-Tiefe für Security-Auditoren.

### [MCP-Protokoll](/help/mcp/)

Die Protokoll-Schicht unter dem KI-Helfer — für Applikations-
ingenieure die eigene Skripte/Werkzeuge anbinden, und für
IT/Betrieb die deployen, monitoren und troubleshooten.

---

## Weitere Bereiche

- [Download](/download/) — alle Komponenten + APT-Setup
- [News](/news/) — Release-Notes + technische Updates

### [Projekt-Dateiformat (.forge)](/help/file-format/)

Aufbau einer ForgeIEC-Projektdatei: PLCopen-XML-Wurzel, POU-Typen,
Adress-Pool, ForgeIEC-Erweiterungen über `<addData>` und ST-Sprach-
zusätze (Bit-Zugriff, 3-Level-Qualifikation).

### [Bus-Konfiguration](/help/bus-config/)

PLCopen-XML-Schema für die industrielle Feldbus-Konfiguration im `.forge`-Projekt.
Segmente, Devices, Variablen-Binding und IEC-Adressvergabe.

### [Testabdeckung](/help/tests/)

62 automatisierte Testprogramme (Stand 22.10.2026) prüfen den
IEC-61131-3-Sprachvorrat, die Standard-Bausteine und das
Multi-Task-Threading-System.

### [Open Source Philosophie](/help/open-source/)

Der Gedanke hinter Open Source geht weit über Software hinaus — es ist
eine Bewegung, die Wissen befreit und Innovation demokratisiert.

---

## Erste Schritte

Für den Einstieg brauchen Sie zwei Pakete:

1. **ForgeIEC Studio** (`forgeiec-studio`, Programm `forgeiec`) — die Entwicklungsumgebung auf Ihrer Workstation
2. **Anvil-Server (anvild)** (`forgeiec-anvil-server`, Programm `anvil-server`) — das Laufzeitsystem auf der Ziel-SPS

Alle weiteren Komponenten stehen auf der [Plattform-Seite](/de/plattform/).

### Installation aus dem ForgeIEC APT-Repository

ForgeIEC wird als signiertes Debian-Repository unter
`apt.forgeiec.io` bereitgestellt. Die Einrichtung erfolgt einmalig
auf jeder Workstation bzw. Ziel-SPS:

```bash
# Signier-Schlüssel hinterlegen
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Repository-Quelle eintragen
# (Debian 12 "bookworm" bzw. Debian 13 "trixie" — passend zum System)
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

sudo apt update
```

Anschließend kann jedes ForgeIEC-Paket mit dem Standard-Paket-
Manager installiert werden:

```bash
# Editor (Workstation)
sudo apt install forgeiec-studio

# Daemon (Ziel-SPS)
sudo apt install forgeiec-anvil-server
```

Updates folgen automatisch dem normalen `apt update && apt upgrade`
Lebenszyklus — es ist keine manuelle `.deb`-Datei nötig.

### Unterstützte Plattformen

| Komponente | Architekturen | Debian-/Ubuntu-Suites |
|------------|---------------|------------------|
| Studio     | amd64, arm64  | bookworm, trixie, noble |
| Anvil-Server + Bridges | amd64, arm64, armhf | bookworm, trixie, jammy, noble |
| Hearth (Vorschau) | amd64, arm64, armhf | bookworm, trixie, jammy, noble |

Studio, Gerätebeschreibungen, Hearth und das Bedien-Panel gibt es
zusätzlich als RPM für AlmaLinux 9 und Fedora 44 unter
`rpm.forgeiec.io` (die Runtime noch nicht). Ein Windows-Build des
Studios existiert; den Installer gibt es auf Anfrage. Die vollständige
Paket-/Plattform-Matrix steht auf der [Download-Seite](/de/download/).

### Kontakt

Bei Fragen wenden Sie sich an: blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**Die Dokumentation wächst mit dem Projekt.**

blacksmith@forgeiec.io

</div>
