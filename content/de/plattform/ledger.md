---
title: "Ledger"
description: "Auftragsmanagement — Produktionsplanung, Rezeptverwaltung und MES-Integration"
weight: 7
---

## Das Schmiedebuch — *geplant*

Jede Schmiede führt ein Auftragsbuch — welcher Auftrag, welches Material,
welche Menge. **Ledger** ist das Auftragsmanagement-Modul der
ForgeIEC-Plattform: die Brücke zwischen Fertigungssteuerung und
Betriebswirtschaft.

> Ledger ist geplant, die Entwicklung hat noch nicht begonnen. Die hier
> beschriebenen Funktionen repräsentieren den geplanten Umfang.

---

## Geplante Funktionen

### Produktionsplanung

- Auftragserfassung und Priorisierung
- Kapazitätsplanung und Maschinenbelegung
- Auftragsstatus-Verfolgung in Echtzeit
- Rückmeldung aus der SPS — automatische Fortschrittsmeldung

### Rezeptverwaltung

- Verwaltung von Produktionsrezepten und Parametersätzen
- Versionierung und Freigabeworkflow
- Automatische Parameterübertragung an die SPS bei Auftragswechsel
- Rückverfolgbarkeit: welches Rezept wurde wann geladen

### Batch-Tracking

- Chargenprotokollierung mit Zeitstempel
- Zuordnung von Produktionsdaten zu Aufträgen
- Materialverfolgung vom Eingang bis zum Endprodukt
- Exportfunktion für Qualitätsdokumentation

### MES-Integration

- Schnittstellen zu übergeordneten MES-Systemen
- ISA-95-kompatible Datenmodelle
- REST/OPC-UA-basierter Datenaustausch
- Bidirektional: Aufträge empfangen, Rückmeldungen senden

---

## Integration in die Plattform

Ledger verbindet die Produktionsebene (Anvil, Tongs) mit der
Planungsebene (MES, ERP). Die SPS meldet Stückzahlen und Zustände,
Ledger verwaltet die Aufträge und steuert den Materialfluss.

```
ERP / MES
    |
  Ledger (Auftragsmanagement)
    |
  anvild (SPS-Kern)
    |
  Tongs (Feldbus-Bridges) --> Maschinen
```

**Lizenz:** AGPL-3.0-or-later

---

<div style="text-align:center; padding: 2rem;">

**Ledger — Vom Auftrag zum fertigen Produkt.**

blacksmith@forgeiec.io

</div>
