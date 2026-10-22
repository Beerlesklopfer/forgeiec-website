---
title: "Sicherheits-Modell"
summary: "Wie ForgeIEC verhindert dass die KI versehentlich Schaden anrichtet — drei Schutz-Schichten"
---

## Das Grundprinzip

Eine KI im Industrie-Editor ist gefährlich wenn sie ohne Aufsicht
schalten kann. Ein **geforcter Output** könnte einen Motor anwerfen.
Ein **falsches Deploy** könnte die laufende Anlage stoppen. Eine
**versehentlich gelöschte Variable** könnte eine Schutzfunktion
außer Kraft setzen.

ForgeIEC's Antwort: **drei aufeinanderfolgende Schutz-Schichten**. Eine
KI muss alle drei passieren bevor sie etwas in Ihrer Anlage verändern
kann.

---

## Schicht 1 — Standard-Auslieferung ist sicher

Wenn Sie ForgeIEC frisch aus dem APT-Repository installieren, ist
der KI-Helfer im **Read-only-Modus**. Er kann:

- Lesen (Projekt, POUs, Live-Werte)
- Vorschläge machen ("hier wäre ein Bug")
- Diagnose-Berichte erstellen

Er kann **nicht**:

- Variablen anlegen oder löschen
- POU-Code ändern
- Kompilieren oder deployen
- SPS starten / stoppen / pausieren

Das ist nicht ein Hakchen das man umstellt — das ist eine **andere
Editor-Version**. Die Standard-Version aus dem Internet hat die
Schreib-Funktionen **gar nicht erst eingebaut**.

Um schreibende Aktionen zu erlauben, muss ForgeIEC Studio neu **mit
der Option `-DMCP_OVERRIDE_SECURITIES=ON`** gebaut werden — oder Sie
installieren das mitgelieferte Dev-Paket. **Auf einer produktiven
SPS-Workstation sollte das nicht laufen.**

Erkennen Sie es daran: wenn ForgeIEC Studio mit Schreib-Freigabe
gestartet ist, zeigt der KI-Helfer beim Start einen **Sicherheits-
Banner**:

```
!!! SECURITY OVERRIDE ACTIVE !!!
Editor was built with MCP_OVERRIDE_SECURITIES=ON
ALL MCP security gates are OPEN
This build MUST NOT run on a productive PLC.
```

### Wenn die KI ein Schreib-Werkzeug aufruft das gesperrt ist

In der Standard-Version bekommt die KI einen klaren Fehler — und
einen **konkreten Menü-Pfad**, den sie Ihnen zeigen kann. Die KI
versucht **nicht**, das System aufzuweichen; sie zeigt Ihnen
stattdessen wo Sie den entsprechenden Knopf im Editor selbst
finden. Beispiel: die KI möchte eine Variable anlegen:

```
{ "ok": false,
  "error": "FORGE_ERR_PERMISSION_DENIED",
  "remediation": {
    "rule": "editor_override_required",
    "requires_human_action": true,
    "gui_path": "Variables panel → Add Variable button (top of the table)",
    "user_prompt": "Ich kann den Schritt in dieser Installation nicht
      selber ausfuehren. Um es manuell zu tun, gehe zu:
      → Variables panel → Add Variable button
      Sag mir Bescheid wenn Du fertig bist."
  }
}
```

Die KI weiß dadurch sofort:

1. **Was schief lief** — Production-Build, Tool ist gesperrt.
2. **Welchen Knopf Sie als Operator drücken müssen** — den
   konkreten Menü-/Dialog-/Tree-Context-Pfad zur passenden GUI-
   Aktion. Jede MCP-Schreibaktion hat ein hand-klickbares
   Äquivalent.
3. **Was die KI _nicht_ tun darf** — Sie zu Shell-Befehlen, einem
   Rebuild oder einem Anruf beim Administrator anzustiften. Der
   GUI-Pfad ist die einzige Operator-Aktion.

Das gleiche Pattern gilt für den **PLC-Runtime** (anvild) wenn
der ohne Live-Monitoring läuft — `monitor.*` / `oscilloscope.*`
verweisen dann auf den Menü-Toggle:

```
{ "ok": false,
  "error": "FORGE_ERR_RUNTIME_FEATURE_UNAVAILABLE",
  "feature": "monitor",
  "remediation": {
    "gui_path": "Runtime → Live-Monitoring",
    "user_prompt": "Bitte oeffne das **Runtime**-Menue in ForgeIEC
      Studio und klick **Live-Monitoring**. Das Menue-Item ist
      eine Checkbox — anklicken schaltet ein."
  }
}
```

Sie merken: bevor die KI etwas „heimlich" macht oder ins Leere
läuft, sagt sie Ihnen explizit „bitte klick **hier**" + zeigt
den konkreten Pfad. Die Entscheidung — und der Klick — liegen
bei Ihnen.

---

## Schicht 2 — Rückfrage bei jeder Änderung

Selbst in der freigeschalteten Version stellt ForgeIEC Studio bei
**jeder** schreibenden Aktion eine Rückfrage.

Beispiel: Die KI will eine Variable anlegen.

```
[tool] project.write.add_variable
        name=Druck_1, iec_type=REAL, address=%MD200, scope=bellows.Sensoren

Confirmation required:
  Question: Add bellows.Sensoren.Druck_1 (iec_type=REAL)?
  Options:  yes / cancel
```

Erst wenn Sie **„yes"** klicken passiert die Aktion. Wenn Sie
**„cancel"** klicken, wird der KI-Loop sauber abgebrochen und die
KI wird informiert dass Sie abgelehnt haben — sie kann dann anders
weitermachen oder fragen.

Diese Rückfragen erscheinen **sichtbar im Chat-Verlauf** — der KI-
Helfer kann Sie nicht „heimlich" umgehen.

**Im Geschwindigkeits-Modus** (siehe
[Bedienung](/help/ai/chat/)) beantwortet ForgeIEC Studio diese Rückfragen
**selbst mit „yes"**. Das ist bequem für Test-Setups aber **nicht
empfohlen für Produktion** — gilt nur für die aktuelle Anfrage und
muss bewusst eingeschaltet werden.

---

## Schicht 3 — Operator-Sichtbarkeit

Die KI kann **nichts heimlich** tun. Alles ist mitlesbar:

- **Im Chat-Verlauf** sehen Sie jeden Werkzeug-Aufruf der KI:
  `[tool] codegen.deploy (0 args)`
- **Im Output-Panel** sehen Sie die Compile-Ausgabe wie wenn Sie
  selbst auf den Build-Knopf gedrückt hätten.
- **Im Audit-Log** wird jede schreibende Aktion mit Zeitstempel
  protokolliert. Die Datei liegt unter
  `~/.config/ForgeIEC/mcp_audit.log` und kann nachträglich
  durchgesehen werden.

---

## Force-Pfad — die rote Linie

Eine Aktion ist **prinzipiell** der KI nicht zugänglich: das
**Forcing**. „Forcing" bedeutet einen Wert einer Variablen
manuell festlegen, unabhängig davon was das Programm sagt — also
z.B. einen Output-Pin auf TRUE setzen, was am Hardware-Ausgang einen
Motor anwerfen kann.

Force-Setzungen muss der **Mensch über die GUI** vornehmen. Die KI
kann sie sehen (im Live-Snapshot zeigt sie `forced=true`) aber
**nicht selber setzen**. Das ist eine **harte Trennung** —
unabhängig vom Geschwindigkeits-Modus, unabhängig vom Build-Flag.

Begründung: ein geforcter Output bewegt **reale Hardware**. Schutz-
und Sicherheits-Funktionen könnten dadurch außer Kraft gesetzt
werden. Ein KI-Agent darf solche Side-Effects nicht selbsttätig
auslösen — selbst wenn er glaubt es wäre richtig.

---

## Was tun wenn etwas falsch läuft?

1. **Notbremse** (roter STOP-Knopf im Chat-Reiter, nur sichtbar im
   Geschwindigkeits-Modus) → KI-Loop sofort abbrechen
2. **SPS stoppen** über das `Runtime`-Menü → Outputs in
   Safe-State
3. **Geforcte Variablen aufheben** über den Force-Tab im Variables-
   Panel
4. **Audit-Log lesen** unter `~/.config/ForgeIEC/mcp_audit.log` →
   was hat die KI nacheinander gemacht

---

## Empfehlungen

- **Entwicklung:** freigeschaltete Version, Trainee-Persona,
  langsamer Modus — Sie sehen jeden Schritt
- **Code-Review:** Reviewer-Persona — kann nichts kaputt machen
- **Diagnose auf Produktions-SPS:** Monitor-Persona — keine
  Änderungen möglich
- **Aktive Programmierung mit erfahrener KI:** Blacksmith Master,
  ggf. Geschwindigkeits-Modus an
- **Produktiver Betrieb auf laufender Anlage:** lassen Sie die
  Standard-Version drauf — KI ist read-only, keine Gefahr

---

## Weiter

- [Bedienung im Alltag](/help/ai/chat/) — Notbremse + Geschwindigkeits-
  Modus
- [Personas](/help/ai/agents/) — welche Charaktere haben welche Rechte
- [Mehrere Workstations verbinden](/help/ai/team/) — Team-Trust
- [Zurück zur AI-Übersicht](/help/ai/)
