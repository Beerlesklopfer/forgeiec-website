---
title: "Hearth"
description: "SCADA/HMI — Prozessvisualisierung und Anlagenbedienung im Browser"
weight: 4
---

## Die Feuerstelle — *In Entwicklung*

Die Feuerstelle ist der Mittelpunkt der Schmiede — hier sieht man das Gluehen
des Metalls, hier spuert man die Hitze. **Hearth** ist die SCADA/HMI-Loesung
der ForgeIEC-Plattform: Prozessvisualisierung und Anlagenbedienung,
ueberall erreichbar im Browser.

> Hearth befindet sich in aktiver Entwicklung. Die hier beschriebenen
> Funktionen repraesentieren den geplanten Umfang.

---

## Geplante Funktionen

### Prozessvisualisierung

- Webbasierte Darstellung von Anlagenzustaenden und Prozesswerten
- Responsive Dashboards fuer Desktop, Tablet und Mobilgeraete
- Echtzeit-Aktualisierung ohne manuelles Neuladen
- Frei konfigurierbare Prozessbilder mit Symbolen und Animationen

### Alarmmanagement

- Zentrale Alarmverwaltung mit Quittierung und Eskalation
- Alarmhistorie mit Zeitstempel und Benutzerprotokoll
- Priorisierung und Filterung nach Anlagenbereichen
- Push-Benachrichtigungen bei kritischen Zustaenden

### Trendaufzeichnung

- Langzeit-Aufzeichnung von Prozesswerten
- Konfigurierbare Abtastraten und Speicherdauer
- Trend-Diagramme mit Zoom, Pan und Cursor-Abfrage
- Export in CSV und gaengige Formate

### Bedienoberfaeche

- Eingabemasken fuer Sollwerte und Rezeptparameter
- Benutzerverwaltung mit Berechtigungsstufen
- Bedienerprotokoll (Audit Trail) fuer regulierte Umgebungen

---

## Integration in die Plattform

Hearth verbindet sich ueber die OPC-UA-Schnittstelle (Bellows) oder
direkt ueber gRPC mit der Anvil-Laufzeitumgebung. Der Zugriff erfolgt
ueber den Webbrowser — keine Installation auf dem Bediengeraet erforderlich.

```
Browser  --->  Hearth (Web-Server)  --->  anvild / Bellows
                                            |
                                          SPS-Kern
```

---

<div style="text-align:center; padding: 2rem;">

**Hearth — Die Anlage im Blick, von ueberall.**

blacksmith@forgeiec.io

</div>
