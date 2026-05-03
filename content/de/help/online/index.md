---
title: "Online-Hilfe"
summary: "Einstiegspunkt fuer die kontext-sensitive Hilfe aus dem ForgeIEC-Editor"
---

## Online-Hilfe — Was ist das?

Die Online-Hilfe ist die kontext-sensitive Hilfe-Schicht des ForgeIEC-
Editors. Beim Druecken von **F1** im Editor oeffnet sich Ihr Browser
direkt mit der Hilfeseite zum aktuell fokussierten Element (Dialog,
Panel, Variablen-Tabelle, Codegen-Aktion, ...).

## URL-Schema

Alle Hilfeseiten sind unter einem einheitlichen Schema erreichbar:

```
https://forgeiec.io/<sprache>/help/<thema>/
```

- `<sprache>` folgt der Editor-Locale (de, en, fr, es, ja, tr, zh, ar);
  Default `de` wenn keine passende Lokalisierung vorhanden ist
- `<thema>` ist ein Slug, der pro Topic gleich ist und nicht uebersetzt wird

So koennen Sie eine Hilfeseite auch direkt im Browser oeffnen, ohne den
Editor zu starten.

## Verfuegbare Themen

Die wichtigsten Themen finden Sie auf der [Hilfe-Uebersicht](/help/).

## Im Editor

- **F1** auf einem fokussierten Element → kontext-sensitive Hilfeseite
- **Hilfe → Online-Hilfe** im Hauptmenue → Einstiegspunkt (diese Seite)
- **Hilfe → Ueber ForgeIEC** → Versions-Info + Lizenz
