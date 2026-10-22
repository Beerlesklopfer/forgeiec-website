---
title: "Bellows"
description: "OPC UA Gateway — standardisierte Maschinenkommunikation für die Industrie"
weight: 3
---

## Der Blasebalg — *In Entwicklung*

Der Blasebalg hält das Feuer am Leben und bringt Luft dorthin, wo sie
gebraucht wird. **Bellows** ist das OPC-UA-Gateway der ForgeIEC-Plattform —
die standardisierte Schnittstelle zwischen Werkstatt und Leitstand,
zwischen Maschine und übergeordnetem System.

> Bellows befindet sich in aktiver Entwicklung. Die hier beschriebenen
> Funktionen repräsentieren den geplanten Umfang.

---

## OPC UA — Der Industriestandard

OPC Unified Architecture ist der herstellerunabhängige Standard für
Maschine-zu-Maschine-Kommunikation in der Industrieautomation. Bellows
implementiert diesen Standard als integralen Bestandteil der
ForgeIEC-Plattform.

---

## Geplante Funktionen

### OPC UA Server

- Bereitstellung aller SPS-Variablen als OPC-UA-Knoten
- Automatische Abbildung der IEC-Datentypen auf das OPC-UA-Informationsmodell
- Browse-, Read-, Write- und Subscribe-Dienste
- Sicherheit durch Zertifikatsauthentifizierung

### OPC UA Client

- Zugriff auf externe OPC-UA-Server aus dem SPS-Programm
- Lesen und Schreiben entfernter Variablen
- Event-Subscriptions für zustandsbasierte Steuerung

### Informationsmodell-Mapping

- Automatische Generierung des Adressraums aus der Projektkonfiguration
- Unterstützung für benutzerdefinierte Informationsmodelle
- Companion-Specification-Kompatibilität (PackML, Euromap, etc.)

---

## Integration in die Plattform

Bellows wird als eigenständiger Bridge-Prozess laufen — überwacht und
verwaltet von `anvild`. Die Kommunikation mit dem SPS-Kern erfolgt über
Anvil Technology (Zero-Copy Shared Memory), genau wie bei den
Feldbus-Bridges.

```
Forge Studio  --->  anvild  --->  Bellows (OPC UA)  --->  SCADA/MES/Cloud
                      |
                    Anvil SHM
```

**Lizenz:** AGPL-3.0

---

<div style="text-align:center; padding: 2rem;">

**Bellows — Standardisierte Kommunikation für die vernetzte Fertigung.**

blacksmith@forgeiec.io

</div>
