---
title: "Spark"
description: "Zenoh-Tunnel — Netzwerk-Bridge zwischen Edge und Cloud"
weight: 5
---

## Der Funke

Ein Funke springt ueber — von der Schmiede nach draussen. **Spark** ist der
Zenoh-Tunnel der ForgeIEC-Plattform: eine Netzwerk-Bridge, die
SPS-Installationen ueber Standortgrenzen hinweg verbindet. Edge-to-Cloud,
Maschine-zu-Maschine, Werkstatt-zu-Leitstand.

---

## Zenoh-Protokoll

Spark basiert auf dem Zenoh-Protokoll — einem modernen Pub/Sub-Protokoll
fuer verteilte Systeme mit minimaler Latenz und automatischer
Netzwerkerkennung:

- **Zero-Config Discovery** — Teilnehmer finden sich automatisch im Netzwerk
- **Adaptive Uebertragung** — vom lokalen Shared Memory bis zum
  WAN-Tunnel, transparent
- **Effizient** — minimaler Overhead, geeignet fuer eingebettete Systeme
  und Cloud-Infrastruktur gleichermassen

---

## Anwendungsfaelle

### Live-Monitoring

Prozesswerte von entfernten SPS-Installationen in Echtzeit ueberwachen —
ohne VPN-Konfiguration, ohne Portweiterleitung. Spark stellt den
Datentunnel bereit.

### Variable Forcing

Variablen auf entfernten Steuerungen forcieren, als saesse man direkt
am Geraet. Fuer Inbetriebnahme, Fernwartung und Diagnose.

### Multi-Standort-Vernetzung

Mehrere ForgeIEC-Installationen zu einem logischen Netzwerk verbinden.
Jeder Standort publiziert und abonniert Variablen — Spark leitet die
Daten transparent weiter.

### Edge-to-Cloud

SPS-Daten in Cloud-Plattformen streamen fuer Langzeitanalyse,
Machine Learning oder zentrale Dashboards. Spark ist die Bruecke
zwischen Shopfloor und IT.

---

## Integration in die Plattform

Spark laeuft als eigenstaendiger Prozess neben `anvild` und nutzt
Anvil Technology (Zero-Copy Shared Memory) fuer den lokalen Datenaustausch.
Ueber das Netzwerk kommuniziert Spark via Zenoh.

```
Standort A                          Standort B
+---------+    Zenoh-Tunnel    +---------+
|  anvild |<--- Spark ----- Spark --->|  anvild |
+---------+    (Internet)      +---------+
```

---

## Technische Eckdaten

| Eigenschaft | Wert |
|-------------|------|
| **Protokoll** | Zenoh |
| **Transport** | TCP, UDP, TLS, QUIC |
| **Discovery** | Multicast + Scouting |
| **Lokaler IPC** | Anvil Technology (Shared Memory) |
| **Plattformen** | x86_64, ARM64, ARMv7 (Linux) |

---

<div style="text-align:center; padding: 2rem;">

**Spark — Der Funke, der Standorte verbindet.**

blacksmith@forgeiec.io

</div>
