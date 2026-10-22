---
title: "Forge Studio"
description: "IEC 61131-3 Entwicklungsumgebung — alle fünf Sprachen, native Qt6-Oberfläche"
weight: 1
---

## Die Werkbank

Forge Studio ist die integrierte Entwicklungsumgebung der ForgeIEC-Plattform.
Hier entsteht das SPS-Programm — vom ersten Entwurf bis zum fertigen Projekt.
Wie die Werkbank in der Schmiede bietet Forge Studio alle Werkzeuge in
Griffweite: Editor, Compiler, Debugger und Bussystem-Konfiguration in
einer Anwendung.

---

## Alle fünf IEC 61131-3 Sprachen

Ein Editor für alle Sprachen — nahtlos umschalten, gemeinsame Variablen,
einheitliche Projektstruktur:

- **Strukturierter Text (ST)** — Hochsprache mit Syntax-Hervorhebung,
  Auto-Vervollständigung und Tree-sitter-basiertem Parsing
- **Anweisungsliste (AWL/IL)** — Assembler-ähnliche Sprache mit intelligenter
  Editierung und Sprachumschaltung von/zu ST
- **Funktionsbausteindiagramm (FBS/FBD)** — Grafischer Editor mit
  Baustein-Bibliothek und Drag-and-Drop
- **Kontaktplan (KOP/LD)** — Vertraute Darstellung für Schaltlogik,
  direkt am Bildschirm verdrahten
- **Ablaufsprache (AS/SFC)** — Schrittkettendiagramme für
  Sequenzsteuerungen mit Transitionen und Aktionen

---

## Syntax-Hervorhebung mit Tree-sitter

Forge Studio verwendet Tree-sitter für inkrementelles Parsing des
Quellcodes. Das bedeutet:

- Präzise Syntax-Hervorhebung auch bei unvollständigem Code
- Strukturelles Verständnis des Programms während der Eingabe
- Schnelle Navigation zwischen Deklarationen und Referenzen
- Keine regulären Ausdrücke — echte Grammatik

---

## Bussystem-Integration

Die an etablierten IEC-61131-3-IDEs orientierte Bussystem-Verwaltung
ist direkt in die Entwicklungsumgebung integriert:

- Segment-Hierarchie mit Geräten und Variablen im Projektbaum
- Automatische IEC-Adressvergabe ohne Kollisionen
- Netzwerk-Scanner für Geräteerkennung
- Diff-Ansicht bei Änderungen zwischen Editor und Laufzeitsystem
- Automatische Generierung der VAR_ANVIL-Transportschicht

---

## Verbindung zur Laufzeitumgebung

Forge Studio kommuniziert über gRPC mit der Anvil-Laufzeitumgebung:

- **Kompilierung auf der Workstation** — Forge Studio erzeugt C-Code
  direkt aus dem Projektmodell und überträgt nur das Ergebnis an
  die SPS (kein externer Compiler in der Toolchain)
- **Verschlüsselter Upload** — AES-256-GCM-verschlüsselte Übertragung
  auf das Zielsystem
- **Live-Debugging** — Variablen in Echtzeit beobachten und forcieren
  während die SPS läuft
- **Benutzerverwaltung** — Mehrbenutzerbetrieb mit Rechtesystem und
  First-Login-Workflow nach Industrie-Standard

---

## Standardbibliothek

Vollständige IEC-Standardbibliothek in einer SQLite-Datenbank:

- Zähler (CTU, CTD, CTUD)
- Timer (TON, TOF, TP)
- Flankenbausteine (R_TRIG, F_TRIG)
- Bistabile Elemente (SR, RS)
- Typkonvertierungen und mathematische Funktionen
- Erweiterbar durch benutzerdefinierte Bausteine

---

## Technische Eckdaten

| Eigenschaft | Wert |
|-------------|------|
| **Sprache** | C++17 |
| **GUI-Framework** | Qt 6 Widgets |
| **Syntax-Engine** | Tree-sitter |
| **Kommunikation** | gRPC (protobuf) |
| **Plattformen** | Linux x86_64, ARM64 |
| **Lizenz** | AGPL-3.0 |

---

<div style="text-align:center; padding: 2rem;">

**Forge Studio — Die Werkbank für industrielle Automatisierung.**

blacksmith@forgeiec.io

</div>
