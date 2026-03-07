---
title: "Ledger"
description: "Auftragsmanagement — Produktionsplanung, Rezeptverwaltung und MES-Integration"
weight: 7
---

## Das Schmiedebuch — *In Entwicklung*

Jede Schmiede fuehrt ein Auftragsbuch — welcher Auftrag, welches Material,
welche Menge. **Ledger** ist das Auftragsmanagement-Modul der
ForgeIEC-Plattform: die Bruecke zwischen Fertigungssteuerung und
Betriebswirtschaft.

> Ledger befindet sich in aktiver Entwicklung. Die hier beschriebenen
> Funktionen repraesentieren den geplanten Umfang.

---

## Geplante Funktionen

### Produktionsplanung

- Auftragserfassung und Priorisierung
- Kapazitaetsplanung und Maschinenbelegung
- Auftragsstatus-Verfolgung in Echtzeit
- Rueckmeldung aus der SPS — automatische Fortschrittsmeldung

### Rezeptverwaltung

- Verwaltung von Produktionsrezepten und Parametersaetzen
- Versionierung und Freigabeworkflow
- Automatische Parameteruebertragung an die SPS bei Auftragswechsel
- Rueckverfolgbarkeit: welches Rezept wurde wann geladen

### Batch-Tracking

- Chargenprotokollierung mit Zeitstempel
- Zuordnung von Produktionsdaten zu Auftraegen
- Materialverfolgung vom Eingang bis zum Endprodukt
- Exportfunktion fuer Qualitaetsdokumentation

### MES-Integration

- Schnittstellen zu uebergeordneten MES-Systemen
- ISA-95-kompatible Datenmodelle
- REST/OPC-UA-basierter Datenaustausch
- Bidirektional: Auftraege empfangen, Rueckmeldungen senden

---

## Integration in die Plattform

Ledger verbindet die Produktionsebene (Anvil, Tongs) mit der
Planungsebene (MES, ERP). Die SPS meldet Stueckzahlen und Zustaende,
Ledger verwaltet die Auftraege und steuert den Materialfluss.

```
ERP / MES
    |
  Ledger (Auftragsmanagement)
    |
  anvild (SPS-Kern)
    |
  Tongs (Feldbus-Bridges) --> Maschinen
```

---

<div style="text-align:center; padding: 2rem;">

**Ledger — Vom Auftrag zum fertigen Produkt.**

blacksmith@forgeiec.io

</div>
