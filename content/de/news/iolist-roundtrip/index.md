---
title: "IO-Liste Roundtrip: CSV-Brücke zwischen Elektriker und Programmierer"
date: 2026-05-14
summary: "bus.import_iolist + bus.export_iolist — 14-Spalten-CSV mit EPLAN-Property-Headern, idempotenter Import, kein Variablen-Erfinden"
components: [studio]
---

{{< components "studio" >}}

## Worum es geht

Im Maschinenbau arbeiten zwei Welten parallel an derselben
Anlage: der **Elektriker** zeichnet im EPLAN den Schaltplan und
weist jedem Klemmenpunkt eine SPS-Adresse zu — der **Programmierer**
schreibt die IEC-Logik gegen genau diese Adressen. Bisher wurde
diese Brücke per E-Mail gepflegt: PDF-Auszug, Tabellen-Copy-
Paste, manuelles Nachtragen. Jeder Drehgeber-Tausch, jede
Klemmen-Umverdrahtung kostete eine Synchronisationsrunde.

Mit dem **MCP-Bus-3-Sprint** können ForgeIEC Studio und EPLAN
P8 ihre IO-Listen direkt austauschen — über eine 14-Spalten-CSV
mit EPLAN-Property-Headern, **bidirektional und idempotent**.

## Die Konvention

Eine ForgeIEC-IO-Liste ist ein **UTF-8/BOM/`;`-getrennter** CSV
mit Headern, die direkt aus den EPLAN-SPS-Eigenschaften (TechTipp
"Übersicht der SPS-Eigenschaften", AML AR APC) abgeleitet sind:

| Spalte | EPLAN-Prop | ForgeIEC-Mapping |
|---|---|---|
| `Konfigurationsprojekt` | 20161 | Projektname |
| `SPS-Station: Name` | 20408 | CPU-Name |
| `Bus-System` | 20308 | Segment-Protokoll (modbustcp/...) |
| `Physikalisches Netz: Name` | 20413 | **Segment-Identität** |
| `Bus-Adresse` | 20311 | Geräte-IP |
| `Hostname` | 20309 | **Geräte-Identität** (= Anvil-Namespace) |
| `BMK` | 20006 | Betriebsmittelkennzeichen |
| `Funktionstext` | 20031 | Variable-Doku |
| `Symbolische Adresse` | 20404 | **Variable-Identität** |
| `Adresse` | 20400 | IEC-Adresse (`%IX0.0`, ...) |
| `Datentyp` | 20405 | BOOL/INT/REAL/... |
| `Symbolische Adresse: Gruppe` | 20610 | AnvilVarList-Name |
| `Bus-Richtung` | (ForgeIEC) | in/out |
| `Modbus-Adresse` | (ForgeIEC) | numerische Modbus-Address |

## Warum nicht "EPLAN-CSV"?

Die Web-Recherche (EPLAN Help-Portal, TechTipp Plattform 2027)
zeigt es klar: **EPLAN P8 hat KEIN universelles IO-Listen-CSV-
Format**. Der primäre Datenaustausch läuft über **AutomationML
AR APC** (XML); CSV-Schemata variieren je SPS-Hersteller (verschiedene Hersteller-Toolchains
haben jeweils eigene Export-Plug-ins) und je
Export-Plug-in. Was es gibt, sind die **EPLAN-SPS-Eigenschaften**
mit eindeutigen Property-IDs — wir nutzen die als Spaltennamen,
schaffen aber explizit **keine "EPLAN-CSV"-Marke**, sondern ein
**ForgeIEC-IO-list-Format**, das gegen EPLAN-Exporte mit denselben
Spalten kompatibel ist.

## Idempotenz und Sicherheits-Disziplin

Der Importer macht **drei Dinge bewusst NICHT**:

1. **Keine Variablen-Erfindung.** Variablen werden im FDD-Pfad
   (`bus.add_module` / `bus.replace_device`) materialisiert.
   Wenn das CSV eine Variable nennt, die nicht im Pool existiert,
   wird die Zeile als `variables_skipped` gezählt — nie als
   neue Pool-Variable angelegt. Wer eine neue Variable braucht,
   geht über das FDD.
2. **Keine FDD-Materialisation bei neuen Geräten.** Existiert
   in der CSV ein Hostname, den das Projekt noch nicht kennt,
   wird das Gerät als **leeres Gerät** angelegt — der Operator
   muss anschließend `bus.replace_device` mit der passenden
   Coupler-FDD aufrufen, um die Modul-Struktur reinzuziehen.
3. **Keine Atomic-Transactions.** Zeilen mit Parse-Fehlern landen
   in `errors[]`, der Rest committet. Partielle Imports sind
   gewollt — EPLAN-Exporte tragen oft Zeilen mit leeren Adressen
   (Dokumentations-Einträge), die der Operator trotzdem
   importieren will.

Die **Roundtrip-Garantie** ist hart: ein `bus.export_iolist`
unmittelbar gefolgt von `bus.import_iolist` auf einem
unveränderten Projekt MUSS
`{ segments_created: 0, devices_created: 0, variables_updated: 0,
errors: [] }` ergeben. Verifiziert end-to-end gegen die
Ackersteuerung-Test-Anlage (2 Segmente, 6 Geräte, 100+
Pool-Variablen).

## Workflow im Alltag

```
Elektriker (EPLAN P8)              Programmierer (ForgeIEC)
=====================              =========================
1. Schaltplan zeichnet
2. SPS-Adressen vergibt
3. Zuordnungsliste exportiert
   → ackersteuerung.csv
                          ─ Mail ─►
                                   4. File → Import → IO-Liste...
                                   5. (Confirm-Dialog: cascade-impact)
                                   6. Pool-Variable bekommen die
                                      neuen Adressen + Funktionstexte
                                   7. ST-Code arbeitet weiter
                                      gegen die alten symbolischen
                                      Namen — keine Re-Compile noetig
```

Beide Tools (`bus.import_iolist` / `bus.export_iolist`) sind
sowohl als **MCP-Werkzeug** (LLM-getrieben) als auch über das
**File → Import / Export**-Menü (operator-getrieben) verfügbar
— bit-identisches Verhalten. Die IO-Liste-Aktionen liegen
zusätzlich unter **Tools → Import / Export**, weil sie konzeptuell
zur Bus-Familie gehören und nicht zum POU-Code.

## Nächste Schritte

- **Phase 4 (Backlog):** BMK-Round-Trip-Persistenz — derzeit
  wird die BMK-Spalte nur informativ durchgereicht. Ein
  zukünftiges Schema hängt sie als Variable-Annotation an.
- **AutomationML AR APC:** der "echte" EPLAN-Standard. Sobald
  ein Anwender das fordert, ergänzen wir `bus.import_aml` /
  `bus.export_aml` parallel zur CSV-Variante.
