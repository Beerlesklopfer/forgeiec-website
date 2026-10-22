---
title: "Hearth"
description: "SCADA/HMI — Prozessvisualisierung und Anlagenbedienung im Browser"
weight: 4
---

## Die Feuerstelle — *In Entwicklung*

Die Feuerstelle ist der Mittelpunkt der Schmiede — hier sieht man das Glühen
des Metalls, hier spürt man die Hitze. **Hearth** ist die SCADA/HMI-Lösung
der ForgeIEC-Plattform: Prozessvisualisierung und Anlagenbedienung,
überall erreichbar im Browser.

> Hearth befindet sich in aktiver Entwicklung. Die hier beschriebenen
> Funktionen repräsentieren den geplanten Umfang.

---

## Geplante Funktionen

### Prozessvisualisierung

- Webbasierte Darstellung von Anlagenzuständen und Prozesswerten
- Responsive Dashboards für Desktop, Tablet und Mobilgeräte
- Echtzeit-Aktualisierung ohne manuelles Neuladen
- Frei konfigurierbare Prozessbilder mit Symbolen und Animationen

### Alarmmanagement

- Zentrale Alarmverwaltung mit Quittierung und Eskalation
- Alarmhistorie mit Zeitstempel und Benutzerprotokoll
- Priorisierung und Filterung nach Anlagenbereichen
- Push-Benachrichtigungen bei kritischen Zuständen

### Trendaufzeichnung

- Langzeit-Aufzeichnung von Prozesswerten
- Konfigurierbare Abtastraten und Speicherdauer
- Trend-Diagramme mit Zoom, Pan und Cursor-Abfrage
- Export in CSV und gängige Formate

### Bedienoberfläche

- Eingabemasken für Sollwerte und Rezeptparameter
- Benutzerverwaltung mit Berechtigungsstufen
- Bedienerprotokoll (Audit Trail) für regulierte Umgebungen

---

## Integration in die Plattform

Hearth verbindet sich über die OPC-UA-Schnittstelle (Bellows) oder
direkt über gRPC mit der Anvil-Laufzeitumgebung. Der Zugriff erfolgt
über den Webbrowser — keine Installation auf dem Bediengerät erforderlich.

```
Browser  --->  Hearth (Web-Server)  --->  anvild / Bellows
                                            |
                                          SPS-Kern
```

**Lizenz:** AGPL-3.0

---

<div style="text-align:center; padding: 2rem;">

**Hearth — Die Anlage im Blick, von überall.**

blacksmith@forgeiec.io

</div>
