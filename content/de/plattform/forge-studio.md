---
title: "Forge Studio"
description: "IEC 61131-3 Entwicklungsumgebung — ST heute, die übrigen vier Sprachen in Arbeit; native Qt6-Oberfläche"
weight: 1
---

## Die Werkbank

Forge Studio ist die integrierte Entwicklungsumgebung der ForgeIEC-Plattform.
Hier entsteht das SPS-Programm — vom ersten Entwurf bis zum fertigen Projekt.
Wie die Werkbank in der Schmiede bietet Forge Studio alle Werkzeuge in
Griffweite: Editor, Compiler, Debugger und Bussystem-Konfiguration in
einer Anwendung.

---

## IEC 61131-3: ST heute, die übrigen vier in Arbeit

Strukturierter Text ist im produktiven Einsatz (Pilotbetrieb). Die
Editoren für IL, FBD, LD und SFC sind in Arbeit; Programme in diesen
Sprachen werden derzeit **noch nicht übersetzt**.

- **Strukturierter Text (ST)** — {{< status "use" >}} Hochsprache mit Syntax-Hervorhebung,
  Auto-Vervollständigung und Tree-sitter-basiertem Parsing; eigener
  Compiler-Kern, der auch die objektorientierten Erweiterungen
  (METHOD, INTERFACE, EXTENDS) beherrscht
- **Anweisungsliste (AWL/IL)** — {{< status "wip" >}} Assembler-ähnliche Sprache mit intelligenter
  Editierung und Sprachumschaltung von/zu ST
- **Funktionsbausteindiagramm (FBS/FBD)** — {{< status "wip" >}} Grafischer Editor mit
  Baustein-Bibliothek und Drag-and-Drop
- **Kontaktplan (KOP/LD)** — {{< status "wip" >}} Vertraute Darstellung für Schaltlogik,
  direkt am Bildschirm verdrahten
- **Ablaufsprache (AS/SFC)** — {{< status "wip" >}} Schrittkettendiagramme für
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

Forge Studio kommuniziert über gRPC mit dem Anvil-Server (anvild):

- **Übersetzung in zwei Stufen** — das Studio übersetzt IEC-Code in
  C++-Quelltext und schickt ihn verschlüsselt an die Steuerung; dort
  baut die Runtime ihn mit g++ — die Steuerung braucht also `make`
  und `g++`, aber keinen IEC-Compiler
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
| **Plattformen** | Linux x86_64/ARM64, Windows x64 (Installer auf Anfrage) |
| **Lizenz** | AGPL-3.0-or-later (generierter Code: Apache-2.0) |

---

<div style="text-align:center; padding: 2rem;">

**Forge Studio — Die Werkbank für industrielle Automatisierung.**

blacksmith@forgeiec.io

</div>
