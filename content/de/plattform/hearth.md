---
title: "Hearth"
description: "SCADA/HMI — Prozessvisualisierung und Anlagenbedienung im Browser"
weight: 4
---

## Die Feuerstelle — *Vorschau*

Die Feuerstelle ist der Mittelpunkt der Schmiede — hier sieht man das Glühen
des Metalls, hier spürt man die Hitze. **Hearth** ist die SCADA/HMI-Lösung
der ForgeIEC-Plattform: Prozessvisualisierung und Anlagenbedienung,
überall erreichbar im Browser.

{{< callout type="note" title="Vorschau" >}}
Hearth gibt es als Vorschau: der Hearth-Server (Paket
`forgeiec-hearth-server`) liest die Prozessdaten direkt vom Anvil-Bus
und stellt die Bedienoberfläche im Browser bereit. Die folgende Liste
beschreibt den angestrebten Umfang — nicht alles davon ist umgesetzt.
{{< /callout >}}

---

## Angestrebter Umfang

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

Hearth liest die Prozessdaten direkt vom Anvil-Bus (iceoryx2, ohne
Kopie) — denselben Weg, den die Runtime intern nutzt. Anweisungen an
die Anlage gibt Hearth an den Anvil-Server (anvild). Der Zugriff
erfolgt über den Webbrowser — keine Installation auf dem Bediengerät
erforderlich.

```
Browser  --->  Hearth (Web-Server)  <---  Anvil-Bus (iceoryx2)  <---  forgeiec_plc (SPS-Zyklus)
                       |
                       +--- Anweisungen --->  Anvil-Server (anvild)
```

**Lizenz:** AGPL-3.0-or-later

---

## Ansichten

{{< screenshot program="hearth" name="editor" alt="Hearth Studio mit einem Bildschirm aus Symbolen und Verbindungen" caption="Hearth Studio: Bildschirme aus Symbolen, Verbindungen und Variablen." status="wip" >}}

{{< screenshot program="hearth-server" name="hmi" alt="Veröffentlichter Hearth-Bildschirm im Browser mit Live-Werten" caption="Ein veröffentlichter Bildschirm im Browser, mit Live-Werten." status="wip" >}}


<div style="text-align:center; padding: 2rem;">

**Hearth — Die Anlage im Blick, von überall.**

blacksmith@forgeiec.io

</div>
