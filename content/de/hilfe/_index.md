---
title: "Hilfe"
summary: "Dokumentation und Ressourcen fuer ForgeIEC"
---

## Hilfe und Ressourcen

Willkommen im Hilfebereich von ForgeIEC. Hier finden Sie Informationen
zu den Grundlagen unseres Projekts und unserer Philosophie.

---

## Themen

### [Open Source Philosophie](/hilfe/open-source/)

Der Gedanke hinter Open Source geht weit ueber Software hinaus — es ist
eine Bewegung, die Wissen befreit und Innovation demokratisiert.

---

## Erste Schritte

ForgeIEC besteht aus zwei Komponenten:

1. **ForgeIEC Editor** (`forgeiec`) — Die Entwicklungsumgebung auf Ihrer Workstation
2. **ForgeIEC Daemon** (`forgeiecd`) — Das Laufzeitsystem auf der Ziel-SPS

### Installation

ForgeIEC wird als Debian-Paket ausgeliefert:

```bash
# Editor (Workstation)
sudo dpkg -i forgeiec_0.1.0_amd64.deb

# Daemon (Ziel-SPS)
sudo dpkg -i forgeiecd_0.1.0_armhf.deb
```

### Unterstuetzte Plattformen

| Komponente | Architekturen |
|-----------|---------------|
| Editor | x86_64, ARM64 |
| Daemon | x86_64, ARM64, ARMv7 |

### Kontakt

Bei Fragen wenden Sie sich an: blacksmith@forgeiec.io

---

<div style="text-align:center; padding: 2rem;">

**Die Dokumentation waechst mit dem Projekt.**

blacksmith@forgeiec.io

</div>
