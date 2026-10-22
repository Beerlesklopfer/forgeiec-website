---
title: "Bussystem"
summary: "Industrielle Kommunikation mit ForgeIEC"
---

## Hierarchische Bussystem-Verwaltung

ForgeIEC organisiert die industrielle Kommunikation in einer
gewohnten Segment-Hierarchie nach Industriestandard:

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

## Unterstützte Protokolle

| Protokoll | Medium | Einsatzgebiet |
|-----------|--------|---------------|
| **Modbus TCP** {{< status "use" "verfügbar" >}} | Ethernet | Gebäudeautomation, Prozesstechnik |
| **Modbus RTU** {{< status "use" "verfügbar" >}} | RS-485 (seriell) | Sensorik, einfache Feldgeräte |
| **LoRaWAN** {{< status "wip" "in Arbeit (Schwerpunkt)" >}} | Funk | Sensorik in der Landwirtschaft und auf weitläufigen Anlagen |
| **EtherCAT** {{< status "wip" "Gerüst, in Arbeit" >}} | Ethernet (Echtzeit) | Motion Control, schnelle E/A |
| **PROFIBUS DP** {{< status "wip" "Gerüst, in Arbeit" >}} | Seriell (Feldbus) | Fertigungsautomation |
| **EtherNet/IP** {{< status "wip" "Gerüst, in Arbeit" >}} | Ethernet | Fertigungsautomation |

## Automatische Adressvergabe

IEC-Adressen (`%IX`, `%QW`, `%MD` etc.) werden global und kollisionsfrei vergeben.
Bestehende Adressen in globalen Variablenlisten werden berücksichtigt.

## Geräteerkennung

Der integrierte Netzwerk-Scanner erkennt Modbus-fähige Geräte automatisch.
Gefundene Geräte können direkt einem Segment zugeordnet werden.

## Änderungsverfolgung

Änderungen an Bus-Variablen werden in einem übersichtlichen Diff-Dialog
dargestellt, bevor sie auf das Laufzeitsystem übertragen werden. Der Anwender
behält die volle Kontrolle.
