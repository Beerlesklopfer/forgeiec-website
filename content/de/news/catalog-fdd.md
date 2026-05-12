---
title: "Hersteller-Daten als First-Class-Citizen: FDD-System"
date: 2026-05-04
summary: "Geraete-Beschreibungen mit eingebetteten PDF-Datenblaettern, Diagnose-Bit-Aufloesung, Modul-Picker — kein PDF-Suchen mehr"
components: [studio]
---

{{< components "studio" >}}

## Worum es geht

Hersteller-Daten in der Automatisierung sind klassisch ein
**Verteilungsproblem**: das Datenblatt steht als PDF auf einem
Netzlaufwerk, die GSD/EDS/FDD-Datei in einem anderen Verzeichnis,
und die Diagnose-Bit-Tabelle im Anhang der Bedienungsanleitung —
falls nicht inzwischen verlegt.

ForgeIEC Studio betrachtet **die Hersteller-FDD als verbindliche
Quelle** und packt alles zusammen: die maschinenlesbare Geraete-
Beschreibung **plus** das PDF-Datenblatt **plus** die Diagnose-Bit-
Tabellen — alles in **einer Datei**, alles aus dem Studio
zugaenglich.

---

## Eine Datei, alles drin

Die FDD wird im PLCopen-FDD-XML-Format gehalten. Datenblaetter
landen als **CDATA-eingebettete PDFs** im
`<Document>`-Element der FDD. Bei Import erkennt Studio das,
extrahiert das PDF, zeigt es im Documents-Tab des Geraete-
Properties-Panel — direkt im Editor, ohne externes PDF-Programm.

Vorteil: **eine Datei = ein vollstaendiges Geraet**. Wenn Sie eine
Maschine als Tarball uebergeben, ist die komplette Hersteller-Info
mit dabei.

---

## Diagnose-Bits — strukturiert auswertbar

Im `<DiagnosticDecode>`-Block der FDD listet der Hersteller pro
Bit:

```xml
<DiagnosticDecode bitOffset="3" length="1">
  <Description lang="DE">Drahtbruch Kanal 3</Description>
  <Description lang="EN">Wire break channel 3</Description>
  <Severity>warning</Severity>
</DiagnosticDecode>
```

Studio parst diese Bloecke und stellt sie im Properties-Panel
unter **Diagnostics-Tab** dar — mit Live-Wert pro Bit aus der
laufenden SPS. Sie sehen sofort welche Bits aktiv sind und was
sie bedeuten, auf Deutsch oder Englisch.

Per MCP `catalog.diag_bits` ist das auch fuer den KI-Helfer
abrufbar — KI-Diagnose-Loop kann dann konkret antworten:

> „Modul `Stachelbeere` meldet Drahtbruch an Kanal 3 (severity
> warning, seit 14:32:05). Pruefen Sie die Verkabelung zu
> Klemme X3."

---

## Modul-Picker mit Protokoll-Filter

Bei modularen Buskopplern (z.B. Weidmueller UR20 mit
ProfiNet-IRT-Coupler + bunter Modulauswahl) hat jeder Coupler
einen `<ModuleProtocol>`-Eintrag im FDD, der sagt welche Modul-
Familien er versteht. Studio nutzt das fuer einen **gefilterten
Modul-Picker**:

- Sie waehlen den Coupler aus
- Studio zeigt **nur** die Module die mit diesem Coupler
  kompatibel sind
- Keine 200-Eintraege-Liste in der Sie haendisch raten muessen
- Keine versehentliche Auswahl eines inkompatiblen Moduls

Hintergrund: commit `5fe1e69`. Spec-Verweis: `bus-system-v1.md`
§7.

---

## FDD-Editor im Studio

Neben dem Read-Pfad gibt es auch einen **FDD-Editor** fuer den
Fall dass eine Hersteller-FDD unvollstaendig ist oder Sie eine
eigene Komponente einpflegen muessen:

- **Diagnostics-Tab** — `<DiagnosticDecode>` strukturiert
  editieren, Bit-Offset + Description + Severity
- **Documents-Tab** — PDF einfuegen, geht als CDATA-Embedded in
  die `<Document>`-Sektion
- **Geometrie-persist** — Fenster-Positionen + Zoom-Stufen werden
  pro Datei gemerkt

Source-Commit: `6774397` (Diagnostics + Documents Tabs).

---

## Catalog-Performance — von 30s auf Sub-Sekunde

Anfangs hat der **Catalog-Auto-Import** beim Studio-Start jede
einzelne FDD mit ihrem eingebetteten PDF re-parst — Cold-Start
dauerte **30+ Sekunden** bei mittlerer Catalog-Groesse.

Fix in commit `3ee7cd6`: kein BLOB-Read im Auto-Import, das PDF
wird erst beim **Klick auf das Geraet** lazy-geladen. Cold-Start:
**Sub-Sekunde**.

---

## Lizenz + Verteilung

ForgeIEC kommt mit einem **eingebauten Weidmueller-Catalog**
(commit `66923df`):

- 100+ Module komplett mit Datenblatt + Diagnostics
- Git-LFS-managed — `catalog/`-Verzeichnis im Source-Tree
- Alle Lizenz-Hinweise eingebettet in den `<Vendor>`-Tags der FDDs

Weitere Hersteller folgen. Eigene FDDs koennen Sie per `File ->
Import FDD` einlesen — wenn der Hersteller PLCopen-FDD nicht
selbst publiziert, koennen Sie GSDML/EDS/ESI ueber den FDD-Editor
in das ForgeIEC-Format ueberfuehren.

---

## Was die Commits getragen haben

- `66923df` — Weidmueller-FDDs mit CDATA-Embedded-PDFs + Git-LFS
- `5dc087c` — FDD-getriebener Diagnostic-Bit-Resolver + Diagnostics-Tab
- `5fe1e69` — `<ModuleProtocol>`-basierter Modul-Picker-Filter
- `6774397` — FDD-Editor mit Diagnostics + Documents Tabs
- `3ee7cd6` — Cold-Start-Performance: kein BLOB-Read im
  Auto-Import
- `aea0d4f` — Spec-Doku der `<DiagnosticDecode>`-Sektion

Spec: `documentation/architecture/bus-system-v1.md` §7
(Hersteller-Daten-Lifecycle).

---

## Wo Sie das nutzen

| Sie wollen … | Wie |
|---|---|
| Datenblatt zu einem Modul ansehen | Klick im Bus-Tab, Documents-Tab |
| Diagnose-Bits eines aktiven Geraets verstehen | Diagnostics-Tab mit Live-Werten |
| Eine fehlende FDD selbst pflegen | File → New FDD, Editor-Tabs |
| KI-Diagnose mit Klartext-Antworten | `catalog.diag_bits` MCP-Tool |
| Maschine als Tarball weitergeben | FDDs + Datenblaetter sind im Projekt mit drin |

---

## Wo es konkret nachzulesen ist

- [Bus-Konfiguration](/help/bus-config/)
- Spec: `documentation/architecture/bus-system-v1.md` (Source-Tree)
