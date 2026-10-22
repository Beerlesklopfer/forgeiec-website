---
title: "Funktionen"
summary: "Alle Funktionen von ForgeIEC im Überblick"
---

## IEC 61131-3: ST heute, die übrigen vier in Arbeit

Strukturierter Text ist im produktiven Einsatz (Pilotbetrieb); die
Editoren für die übrigen vier Sprachen sind in Arbeit und werden noch
nicht übersetzt.

- **Strukturierter Text (ST)** {{< status "use" >}} — Syntax-Hervorhebung, Auto-Vervollständigung, Suchen & Ersetzen; eigener Compiler-Kern mit objektorientierten Erweiterungen
- **Anweisungsliste (AWL)** {{< status "wip" >}}
- **Funktionsbausteindiagramm (FBS)** {{< status "wip" >}} — grafischer Editor mit Baustein-Bibliothek
- **Kontaktplan (KOP)** {{< status "wip" >}} — vertraute Darstellung für Schaltlogik
- **Ablaufsprache (AS)** {{< status "wip" >}} — Schrittkettendiagramme für Sequenzsteuerungen

## Industrielle Bussysteme

Aus IEC-61131-3-IDEs gewohnte Segment-Hierarchie mit automatischer Geräteerkennung.

- **Modbus TCP** {{< status "use" "verfügbar" >}} — Ethernet-basierte Kommunikation
- **Modbus RTU** {{< status "use" "verfügbar" >}} — serielle RS-485-Anbindung
- **LoRaWAN** {{< status "wip" "in Arbeit (Schwerpunkt)" >}} — Funk-Sensorik für Landwirtschaft und weitläufige Anlagen
- **EtherCAT** {{< status "wip" "Gerüst, in Arbeit" >}} — Echtzeit-Ethernet-Feldbus
- **PROFIBUS DP** {{< status "wip" "Gerüst, in Arbeit" >}} — bewährter Industriestandard
- **EtherNet/IP** {{< status "wip" "Gerüst, in Arbeit" >}}
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
  markiert sind, gelangen an externe Systeme. Eine Referenz auf eine nicht-exportierte Variable im ST-
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
- Unterstützung für x86_64, ARM64 und ARMv7 (armhf: Runtime und Hearth)

## Standardbibliothek

Vollständige IEC-Standardbibliothek: Zähler, Timer, Flankenbausteine,
Typkonvertierungen und mathematische Funktionen. Erweiterbar durch
benutzerdefinierte Bausteine.

## Lizenz

Keine Laufzeitlizenz pro Steuerung, kein Vendor-Lock-In. Die Werkzeuge
und Dienste stehen unter AGPL-3.0-or-later; der generierte
Steuerungscode, die Runtime-API-Header und libanvil unter Apache-2.0.
Eine kommerzielle Lizenz ist erhältlich. Läuft auf Linux; ein
Windows-Build des Studios existiert (Installer auf Anfrage).
