---
title: "Funktionen"
summary: "Alle Funktionen von ForgeIEC im Überblick"
---

## Alle fünf IEC 61131-3 Sprachen

Ein Editor für alle Sprachen — nahtlos umschalten, gemeinsame Variablen,
einheitliche Projektstruktur.

- **Strukturierter Text (ST)** — Syntax-Hervorhebung, Auto-Vervollständigung, Suchen & Ersetzen
- **Anweisungsliste (AWL)** — Volle Sprachunterstützung mit intelligenter Editierung
- **Funktionsbausteindiagramm (FBS)** — Grafischer Editor mit Baustein-Bibliothek
- **Kontaktplan (KOP)** — Vertraute Darstellung für Schaltlogik
- **Ablaufsprache (AS)** — Schrittkettendiagramme für Sequenzsteuerungen

## Industrielle Bussysteme

Aus IEC-61131-3-IDEs gewohnte Segment-Hierarchie mit automatischer Geräteerkennung.

- **Modbus TCP** — Ethernet-basierte Kommunikation
- **Modbus RTU** — Serielle RS-485 Anbindung
- **EtherCAT** — Echtzeit-Ethernet-Feldbus
- **Profibus DP** — Bewährter Industriestandard
- Automatische IEC-Adressvergabe ohne Kollisionen
- Netzwerk-Scanner für Geräteerkennung
- Diff-Ansicht bei Änderungen zwischen Editor und Laufzeitsystem

## Echtzeit-Datenaustausch

Hochperformanter Zero-Copy Datenaustausch zwischen SPS-Programmen und
externen Systemen. PUBLISH/SUBSCRIBE direkt im IEC-Programm.

## Live-Debugging

- Variablen in Echtzeit beobachten während die SPS läuft
- Werte forcieren ohne Produktionsstillstand
- Monitoring-Panel mit Filterfunktion

## Sicherheits-Schalter pro Variable

Drei sicherheitskritische Datenpfade verlassen die SPS — HMI-Export,
Live-Monitoring und Force. Jeder Pfad ist nicht implizit erlaubt: jede
einzelne Variable muss explizit dafür freigegeben werden, und der
ST-Compiler validiert das vor dem Generieren von Code.

- **HMI-Export** — nur Variablen, die explizit als HMI-exportiert
  markiert sind, gelangen über die OPC UA Bridge zu remote SCADA/HMI-
  Systemen. Eine Referenz auf eine nicht-exportierte Variable im ST-
  Code wird vom Compiler als harter Fehler abgewiesen.
- **Live-Monitoring** — nur explizit als monitorbar markierte
  Variablen werden über den Watch-Stream live mitgeschnitten.
  Die Monitor-Spalte im Variablen-Panel ist ausgeblendet, wenn der
  globale Monitoring-Schalter aus ist.
- **Forcing** — nur explizit als forcierbar markierte Variablen
  können vom Editor überschrieben werden. Force-Spalte ebenfalls
  vom globalen Force-Schalter abhängig sichtbar.

Globale Schalter sind eine zweite Sicherheitsstufe ("nichts in
Production" bzw. "Force-Privilegien nur in der Inbetriebnahme"); die
Per-Variable-Markierungen sind die unverzichtbare erste Stufe — Daten
verlassen die SPS nur dort, wo der Engineer es bewusst freigegeben hat.

## Remote-Betrieb

- IEC-Kompilierung auf der Workstation — SPS benötigt make, g++, libstdc++ und librt
- Verschlüsselter Upload auf das Zielsystem
- Benutzerverwaltung mit Rechtesystem
- Automatischer Neustart nach Stromausfall
- Unterstützung für x86_64, ARM64 und ARMv7

## Standardbibliothek

Vollständige IEC-Standardbibliothek: Zähler, Timer, Flankenbausteine,
Typkonvertierungen und mathematische Funktionen. Erweiterbar durch
benutzerdefinierte Bausteine.

## Open Source

Keine Lizenzkosten. Kein Vendor-Lock-In. Läuft auf Linux.
