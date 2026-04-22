---
title: "Hilfe"
summary: "Dokumentation und Ressourcen fuer ForgeIEC"
---

## Hilfe und Ressourcen

Willkommen im Hilfebereich von ForgeIEC. Hier finden Sie Informationen
zu den Grundlagen unseres Projekts und unserer Philosophie.

---

## Themen

### [Bus-Konfiguration](/hilfe/bus-config/)

PLCopen-XML-Schema fuer die industrielle Feldbus-Konfiguration im `.forge`-Projekt.
Segmente, Devices, Variablen-Binding und IEC-Adressvergabe.

### [Testabdeckung](/hilfe/tests/)

117 automatisierte Tests pruefen den vollstaendigen IEC 61131-3 Sprachvorrat,
alle 132 Standard-Bausteine und das Multi-Task-Threading-System.

### [Open Source Philosophie](/hilfe/open-source/)

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

{{< distro-install >}}

Anschliessend kann jedes ForgeIEC-Paket mit dem Standard-Paket-
Manager installiert werden:

```bash
# Editor (Workstation)
sudo apt install forgeiec

# Daemon (Ziel-SPS)
sudo apt install anvild
```

Updates folgen automatisch dem normalen `apt update && apt upgrade`
Lebenszyklus — es ist keine manuelle `.deb`-Datei noetig.

### Unterstuetzte Plattformen

| Komponente | Architekturen | Debian-Codenamen |
|------------|---------------|------------------|
| Editor     | amd64, arm64  | bookworm, trixie |
| Daemon     | amd64, arm64  | bookworm, trixie |
| Bridges    | amd64, arm64  | bookworm, trixie |
| Hearth     | amd64, arm64  | bookworm, trixie |

### Kontakt

Bei Fragen wenden Sie sich an: blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**Die Dokumentation waechst mit dem Projekt.**

blacksmith@forgeiec.io

</div>
