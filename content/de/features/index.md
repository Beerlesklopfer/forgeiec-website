---
title: "Funktionen"
summary: "Alle Funktionen von ForgeIEC im Ueberblick"
---

## Alle fuenf IEC 61131-3 Sprachen

Ein Editor fuer alle Sprachen — nahtlos umschalten, gemeinsame Variablen,
einheitliche Projektstruktur.

- **Strukturierter Text (ST)** — Syntax-Hervorhebung, Auto-Vervollstaendigung, Suchen & Ersetzen
- **Anweisungsliste (AWL)** — Volle Sprachunterstuetzung mit intelligenter Editierung
- **Funktionsbausteindiagramm (FBS)** — Grafischer Editor mit Baustein-Bibliothek
- **Kontaktplan (KOP)** — Vertraute Darstellung fuer Schaltlogik
- **Ablaufsprache (AS)** — Schrittkettendiagramme fuer Sequenzsteuerungen

## Industrielle Bussysteme

CoDeSys-kompatible Segment-Hierarchie mit automatischer Geraeteerkennung.

- **Modbus TCP** — Ethernet-basierte Kommunikation
- **Modbus RTU** — Serielle RS-485 Anbindung
- **EtherCAT** — Echtzeit-Ethernet-Feldbus
- **Profibus DP** — Bewaehrter Industriestandard
- Automatische IEC-Adressvergabe ohne Kollisionen
- Netzwerk-Scanner fuer Geraeteerkennung
- Diff-Ansicht bei Aenderungen zwischen Editor und Laufzeitsystem

## Echtzeit-Datenaustausch

Hochperformanter Zero-Copy Datenaustausch zwischen SPS-Programmen und
externen Systemen. PUBLISH/SUBSCRIBE direkt im IEC-Programm.

## Live-Debugging

- Variablen in Echtzeit beobachten waehrend die SPS laeuft
- Werte forcieren ohne Produktionsstillstand
- Monitoring-Panel mit Filterfunktion

## Sicherheits-Schalter pro Variable

Drei sicherheitskritische Datenpfade verlassen die SPS — HMI-Export,
Live-Monitoring und Force. Jeder Pfad ist nicht implizit erlaubt: jede
einzelne Variable muss explizit dafuer freigegeben werden, und der
ST-Compiler validiert das vor dem Generieren von Code.

- **HMI-Export** — nur Variablen, die explizit als HMI-exportiert
  markiert sind, gelangen ueber die OPC UA Bridge zu remote SCADA/HMI-
  Systemen. Eine Referenz auf eine nicht-exportierte Variable im ST-
  Code wird vom Compiler als harter Fehler abgewiesen.
- **Live-Monitoring** — nur explizit als monitorbar markierte
  Variablen werden ueber den Watch-Stream live mitgeschnitten.
  Die Monitor-Spalte im Variablen-Panel ist ausgeblendet, wenn der
  globale Monitoring-Schalter aus ist.
- **Forcing** — nur explizit als forcierbar markierte Variablen
  koennen vom Editor ueberschrieben werden. Force-Spalte ebenfalls
  vom globalen Force-Schalter abhaengig sichtbar.

Globale Schalter sind eine zweite Sicherheitsstufe ("nichts in
Production" bzw. "Force-Privilegien nur in der Inbetriebnahme"); die
Per-Variable-Markierungen sind die unverzichtbare erste Stufe — Daten
verlassen die SPS nur dort, wo der Engineer es bewusst freigegeben hat.

## Remote-Betrieb

- IEC-Kompilierung auf der Workstation — SPS benoetigt make, g++, libstdc++ und librt
- Verschluesselter Upload auf das Zielsystem
- Benutzerverwaltung mit Rechtesystem
- Automatischer Neustart nach Stromausfall
- Unterstuetzung fuer x86_64, ARM64 und ARMv7

## Standardbibliothek

Vollstaendige IEC-Standardbibliothek: Zaehler, Timer, Flankenbausteine,
Typkonvertierungen und mathematische Funktionen. Erweiterbar durch
benutzerdefinierte Bausteine.

## Open Source

Keine Lizenzkosten. Kein Vendor-Lock-In. Laeuft auf Linux.
