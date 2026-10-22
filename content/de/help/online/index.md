---
title: "Online-Hilfe"
summary: "Einstiegspunkt für die kontext-sensitive Hilfe aus dem ForgeIEC-Editor"
---

## Online-Hilfe — Was ist das?

Die Online-Hilfe ist die kontext-sensitive Hilfe-Schicht des ForgeIEC-
Editors. Beim Drücken von **F1** im Editor öffnet sich Ihr Browser
direkt mit der Hilfeseite zum aktuell fokussierten Element (Dialog,
Panel, Variablen-Tabelle, Codegen-Aktion, ...).

## URL-Schema

Alle Hilfeseiten sind unter einem einheitlichen Schema erreichbar:

```
https://forgeiec.io/<sprache>/help/<thema>/
```

- `<sprache>` folgt der Editor-Locale (de, en, fr, es, ja, tr, zh, ar);
  Default `de` wenn keine passende Lokalisierung vorhanden ist
- `<thema>` ist ein Slug, der pro Topic gleich ist und nicht übersetzt wird

So können Sie eine Hilfeseite auch direkt im Browser öffnen, ohne den
Editor zu starten.

## Verfügbare Themen

### Editor & Sprachen

- [Structured Text (ST)](/de/help/st/) — ST-Editor + Sprachfundamente, Bit-Zugriff, qualifizierte Pool-Referenzen
- [Instruction List (IL)](/de/help/il/) — Akkumulator-basierte IEC-Sprache mit CR-Register
- [Function Block Diagram (FBD)](/de/help/fbd/) — Grafische Verschaltung von Funktionen, Funktionsblöcken und Variablen
- [Ladder Diagram (LD)](/de/help/ld/) — Stromlaufplan-Metapher: Power-Rails, Kontakte, Spulen
- [Sequential Function Chart (SFC)](/de/help/sfc/) — Schritt-Übergangs-Modell für Ablaufsteuerungen und Modi-Maschinen

### Modell & Variablen

- [Variablen-Verwaltung](/de/help/variables/) — Variables-Panel als zentrale Sicht auf den FAddressPool: Spalten, Filter, Bulk-Operationen, Sicherheits-Schalter
- [Bibliothek](/de/help/library/) — IEC 61131-3 Standard-Bibliothek + ForgeIEC-Erweiterungen + benutzerdefinierte Blöcke
- [Properties-Panel](/de/help/properties-panel/) — Inline-Editor für das im Project-Tree selektierte Bus-Element
- [Einstellungen (Preferences)](/de/help/preferences/) — Zentraler Konfigurationsdialog: Editor, Runtime, PLC, AI Assistant

### Bus & Hardware

- [Bus-Konfiguration](/de/help/bus-config/) — PLCopen-XML-Schema für die industrielle Feldbus-Konfiguration

### Projekt

- [Projekt-Dateiformat (.forge)](/de/help/file-format/) — Aufbau einer ForgeIEC-Projektdatei: PLCopen-XML mit ForgeIEC-Erweiterungen

### Allgemein

- [Testabdeckung](/de/help/tests/) — 117 automatisierte Tests für den IEC-Sprachvorrat, Standard-Bausteine und Multi-Task-Threading
- [Open Source Philosophie](/de/help/open-source/) — Hintergrund: mehr als Software, ein gesellschaftlicher Gedanke

## Im Editor

- **F1** auf einem fokussierten Element → kontext-sensitive Hilfeseite
- **Hilfe → Online-Hilfe** im Hauptmenü → Einstiegspunkt (diese Seite)
- **Hilfe → Über ForgeIEC** → Versions-Info + Lizenz
