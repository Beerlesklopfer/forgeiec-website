---
title: "Forge Studio"
description: "IEC 61131-3 Entwicklungsumgebung — alle fuenf Sprachen, native Qt6-Oberflaeche"
weight: 1
---

## Die Werkbank

Forge Studio ist die integrierte Entwicklungsumgebung der ForgeIEC-Plattform.
Hier entsteht das SPS-Programm — vom ersten Entwurf bis zum fertigen Projekt.
Wie die Werkbank in der Schmiede bietet Forge Studio alle Werkzeuge in
Griffweite: Editor, Compiler, Debugger und Bussystem-Konfiguration in
einer Anwendung.

---

## Alle fuenf IEC 61131-3 Sprachen

Ein Editor fuer alle Sprachen — nahtlos umschalten, gemeinsame Variablen,
einheitliche Projektstruktur:

- **Strukturierter Text (ST)** — Hochsprache mit Syntax-Hervorhebung,
  Auto-Vervollstaendigung und Tree-sitter-basiertem Parsing
- **Anweisungsliste (AWL/IL)** — Assembler-aehnliche Sprache mit intelligenter
  Editierung und Sprachumschaltung von/zu ST
- **Funktionsbausteindiagramm (FBS/FBD)** — Grafischer Editor mit
  Baustein-Bibliothek und Drag-and-Drop
- **Kontaktplan (KOP/LD)** — Vertraute Darstellung fuer Schaltlogik,
  direkt am Bildschirm verdrahten
- **Ablaufsprache (AS/SFC)** — Schrittkettendiagramme fuer
  Sequenzsteuerungen mit Transitionen und Aktionen

---

## Syntax-Hervorhebung mit Tree-sitter

Forge Studio verwendet Tree-sitter fuer inkrementelles Parsing des
Quellcodes. Das bedeutet:

- Praezise Syntax-Hervorhebung auch bei unvollstaendigem Code
- Strukturelles Verstaendnis des Programms waehrend der Eingabe
- Schnelle Navigation zwischen Deklarationen und Referenzen
- Keine regulaeren Ausdruecke — echte Grammatik

---

## Bussystem-Integration

Die CoDeSys-kompatible Bussystem-Verwaltung ist direkt in die
Entwicklungsumgebung integriert:

- Segment-Hierarchie mit Geraeten und Variablen im Projektbaum
- Automatische IEC-Adressvergabe ohne Kollisionen
- Netzwerk-Scanner fuer Geraeteerkennung
- Diff-Ansicht bei Aenderungen zwischen Editor und Laufzeitsystem
- Automatische Generierung der VAR_ANVIL-Transportschicht

---

## Verbindung zur Laufzeitumgebung

Forge Studio kommuniziert ueber gRPC mit der Anvil-Laufzeitumgebung:

- **Kompilierung auf der Workstation** — Forge Studio erzeugt C-Code
  direkt aus dem Projektmodell und uebertraegt nur das Ergebnis an
  die SPS (kein externer Compiler in der Toolchain)
- **Verschluesselter Upload** — AES-256-GCM-verschluesselte Uebertragung
  auf das Zielsystem
- **Live-Debugging** — Variablen in Echtzeit beobachten und forcieren
  waehrend die SPS laeuft
- **Benutzerverwaltung** — Mehrbenutzerbetrieb mit Rechtesystem und
  CoDeSys-kompatiblem First-Login

---

## Standardbibliothek

Vollstaendige IEC-Standardbibliothek in einer SQLite-Datenbank:

- Zaehler (CTU, CTD, CTUD)
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
| **Lizenz** | Open Source |

---

<div style="text-align:center; padding: 2rem;">

**Forge Studio — Die Werkbank fuer industrielle Automatisierung.**

blacksmith@forgeiec.io

</div>
