---
title: "Bussystem"
summary: "Industrielle Kommunikation mit ForgeIEC"
---

## Hierarchische Bussystem-Verwaltung

ForgeIEC organisiert die industrielle Kommunikation in einer CoDeSys-kompatiblen
Segment-Hierarchie:

```
Bussysteme
+-- Modbus TCP: Halle 1 (eth0) [aktiv]
|   +-- 192.168.1.100 -- Temperaturmodul (Slave 1)
|   |   +-- Temperatur : INT (%IW0)
|   |   +-- Sollwert : INT (%QW10)
|   +-- 192.168.1.101 -- Pumpe (Slave 2)
+-- Modbus RTU: Labor (/dev/ttyUSB0)
+-- Unzugeordnet (Scanner-Pool)
    +-- 192.168.2.55 -- Unbekannt
```

## Unterstuetzte Protokolle

| Protokoll | Medium | Einsatzgebiet |
|-----------|--------|---------------|
| **Modbus TCP** | Ethernet | Gebaeudeautomation, Prozesstechnik |
| **Modbus RTU** | RS-485 (seriell) | Sensorik, einfache Feldgeraete |
| **EtherCAT** | Ethernet (Echtzeit) | Motion Control, schnelle E/A |
| **Profibus DP** | Seriell (Feldbus) | Fertigungsautomation |

## Automatische Adressvergabe

IEC-Adressen (`%IX`, `%QW`, `%MD` etc.) werden global und kollisionsfrei vergeben.
Bestehende Adressen in globalen Variablenlisten werden beruecksichtigt.

## Geraeteerkennung

Der integrierte Netzwerk-Scanner erkennt Modbus-faehige Geraete automatisch.
Gefundene Geraete koennen direkt einem Segment zugeordnet werden.

## Aenderungsverfolgung

Aenderungen an Bus-Variablen werden in einem uebersichtlichen Diff-Dialog
dargestellt, bevor sie auf das Laufzeitsystem uebertragen werden. Der Anwender
behaelt die volle Kontrolle.
