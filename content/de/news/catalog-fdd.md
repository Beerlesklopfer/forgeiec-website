---
title: "Hersteller-Daten als First-Class-Citizen: FDD-System"
date: 2026-05-04
summary: "Geräte-Beschreibungen mit eingebetteten PDF-Datenblättern, Diagnose-Bit-Auflösung, Modul-Picker — kein PDF-Suchen mehr"
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
Quelle** und packt alles zusammen: die maschinenlesbare Geräte-
Beschreibung **plus** das PDF-Datenblatt **plus** die Diagnose-Bit-
Tabellen — alles in **einer Datei**, alles aus dem Studio
zugänglich.

---

## Eine Datei, alles drin

Die FDD wird im PLCopen-FDD-XML-Format gehalten. Datenblätter
landen als **CDATA-eingebettete PDFs** im
`<Document>`-Element der FDD. Bei Import erkennt Studio das,
extrahiert das PDF, zeigt es im Documents-Tab des Geräte-
Properties-Panel — direkt im Editor, ohne externes PDF-Programm.

Vorteil: **eine Datei = ein vollständiges Gerät**. Wenn Sie eine
Maschine als Tarball übergeben, ist die komplette Hersteller-Info
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

Studio parst diese Blöcke und stellt sie im Properties-Panel
unter **Diagnostics-Tab** dar — mit Live-Wert pro Bit aus der
laufenden SPS. Sie sehen sofort welche Bits aktiv sind und was
sie bedeuten, auf Deutsch oder Englisch.

Per MCP `catalog.diag_bits` ist das auch für den KI-Helfer
abrufbar — KI-Diagnose-Loop kann dann konkret antworten:

> „Modul `Stachelbeere` meldet Drahtbruch an Kanal 3 (severity
> warning, seit 14:32:05). Prüfen Sie die Verkabelung zu
> Klemme X3."

---

## Modul-Picker mit Protokoll-Filter

Bei modularen Buskopplern (z.B. Weidmueller UR20 mit
ProfiNet-IRT-Coupler + bunter Modulauswahl) hat jeder Coupler
einen `<ModuleProtocol>`-Eintrag im FDD, der sagt welche Modul-
Familien er versteht. Studio nutzt das für einen **gefilterten
Modul-Picker**:

- Sie wählen den Coupler aus
- Studio zeigt **nur** die Module die mit diesem Coupler
  kompatibel sind
- Keine 200-Einträge-Liste in der Sie händisch raten müssen
- Keine versehentliche Auswahl eines inkompatiblen Moduls

Hintergrund: commit `5fe1e69`. Spec-Verweis: `bus-system-v1.md`
§7.

---

## FDD-Editor im Studio

Neben dem Read-Pfad gibt es auch einen **FDD-Editor** für den
Fall dass eine Hersteller-FDD unvollständig ist oder Sie eine
eigene Komponente einpflegen müssen:

- **Diagnostics-Tab** — `<DiagnosticDecode>` strukturiert
  editieren, Bit-Offset + Description + Severity
- **Documents-Tab** — PDF einfügen, geht als CDATA-Embedded in
  die `<Document>`-Sektion
- **Geometrie-persist** — Fenster-Positionen + Zoom-Stufen werden
  pro Datei gemerkt

Source-Commit: `6774397` (Diagnostics + Documents Tabs).

---

## Catalog-Performance — von 30s auf Sub-Sekunde

Anfangs hat der **Catalog-Auto-Import** beim Studio-Start jede
einzelne FDD mit ihrem eingebetteten PDF re-parst — Cold-Start
dauerte **30+ Sekunden** bei mittlerer Catalog-Größe.

Fix in commit `3ee7cd6`: kein BLOB-Read im Auto-Import, das PDF
wird erst beim **Klick auf das Gerät** lazy-geladen. Cold-Start:
**Sub-Sekunde**.

---

## Lizenz + Verteilung

ForgeIEC kommt mit einem **eingebauten Weidmueller-Catalog**
(commit `66923df`):

- 100+ Module komplett mit Datenblatt + Diagnostics
- Git-LFS-managed — `catalog/`-Verzeichnis im Source-Tree
- Alle Lizenz-Hinweise eingebettet in den `<Vendor>`-Tags der FDDs

Weitere Hersteller folgen. Eigene FDDs können Sie per `File ->
Import FDD` einlesen — wenn der Hersteller PLCopen-FDD nicht
selbst publiziert, können Sie GSDML/EDS/ESI über den FDD-Editor
in das ForgeIEC-Format überführen.

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
| Diagnose-Bits eines aktiven Geräts verstehen | Diagnostics-Tab mit Live-Werten |
| Eine fehlende FDD selbst pflegen | File → New FDD, Editor-Tabs |
| KI-Diagnose mit Klartext-Antworten | `catalog.diag_bits` MCP-Tool |
| Maschine als Tarball weitergeben | FDDs + Datenblätter sind im Projekt mit drin |

---

## Wo es konkret nachzulesen ist

- [Bus-Konfiguration](/help/bus-config/)
- Spec: `documentation/architecture/bus-system-v1.md` (Source-Tree)
