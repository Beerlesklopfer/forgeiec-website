---
title: "Sicherheits-Modell"
summary: "Wie ForgeIEC verhindert dass die KI versehentlich Schaden anrichtet — drei Schutz-Schichten"
---

## Das Grundprinzip

Eine KI im Industrie-Editor ist gefaehrlich wenn sie ohne Aufsicht
schalten kann. Ein **geforcter Output** koennte einen Motor anwerfen.
Ein **falsches Deploy** koennte die laufende Anlage stoppen. Eine
**versehentlich geloeschte Variable** koennte eine Schutzfunktion
ausser Kraft setzen.

ForgeIEC's Antwort: **drei aufeinanderfolgende Schutz-Schichten**. Eine
KI muss alle drei passieren bevor sie etwas in Ihrer Anlage veraendern
kann.

---

## Schicht 1 — Standard-Auslieferung ist sicher

Wenn Sie ForgeIEC frisch aus dem APT-Repository installieren, ist
der KI-Helfer im **Read-only-Modus**. Er kann:

- Lesen (Projekt, POUs, Live-Werte)
- Vorschlaege machen ("hier waere ein Bug")
- Diagnose-Berichte erstellen

Er kann **nicht**:

- Variablen anlegen oder loeschen
- POU-Code aendern
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
einen **konkreten Menue-Pfad**, den sie Ihnen zeigen kann. Die KI
versucht **nicht**, das System aufzuweichen; sie zeigt Ihnen
stattdessen wo Sie den entsprechenden Knopf im Editor selbst
finden. Beispiel: die KI moechte eine Variable anlegen:

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

Die KI weiss dadurch sofort:

1. **Was schief lief** — Production-Build, Tool ist gesperrt.
2. **Welchen Knopf Sie als Operator druecken muessen** — den
   konkreten Menue-/Dialog-/Tree-Context-Pfad zur passenden GUI-
   Aktion. Jede MCP-Schreibaktion hat ein hand-klickbares
   Aequivalent.
3. **Was die KI _nicht_ tun darf** — Sie zu Shell-Befehlen, einem
   Rebuild oder einem Anruf beim Administrator anzustiften. Der
   GUI-Pfad ist die einzige Operator-Aktion.

Das gleiche Pattern gilt fuer den **PLC-Runtime** (anvild) wenn
der ohne Live-Monitoring laeuft — `monitor.*` / `oscilloscope.*`
verweisen dann auf den Menue-Toggle:

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
laeuft, sagt sie Ihnen explizit „bitte klick **hier**" + zeigt
den konkreten Pfad. Die Entscheidung — und der Klick — liegen
bei Ihnen.

---

## Schicht 2 — Rueckfrage bei jeder Aenderung

Selbst in der freigeschalteten Version stellt ForgeIEC Studio bei
**jeder** schreibenden Aktion eine Rueckfrage.

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

Diese Rueckfragen erscheinen **sichtbar im Chat-Verlauf** — der KI-
Helfer kann Sie nicht „heimlich" umgehen.

**Im Geschwindigkeits-Modus** (siehe
[Bedienung](/help/ai/chat/)) beantwortet ForgeIEC Studio diese Rueckfragen
**selbst mit „yes"**. Das ist bequem fuer Test-Setups aber **nicht
empfohlen fuer Produktion** — gilt nur fuer die aktuelle Anfrage und
muss bewusst eingeschaltet werden.

---

## Schicht 3 — Operator-Sichtbarkeit

Die KI kann **nichts heimlich** tun. Alles ist mitlesbar:

- **Im Chat-Verlauf** sehen Sie jeden Werkzeug-Aufruf der KI:
  `[tool] codegen.deploy (0 args)`
- **Im Output-Panel** sehen Sie die Compile-Ausgabe wie wenn Sie
  selbst auf den Build-Knopf gedrueckt haetten.
- **Im Audit-Log** wird jede schreibende Aktion mit Zeitstempel
  protokolliert. Die Datei liegt unter
  `~/.config/ForgeIEC/mcp_audit.log` und kann nachtraeglich
  durchgesehen werden.

---

## Force-Pfad — die rote Linie

Eine Aktion ist **prinzipiell** der KI nicht zugaenglich: das
**Forcing**. „Forcing" bedeutet einen Wert einer Variablen
manuell festlegen, unabhaengig davon was das Programm sagt — also
z.B. einen Output-Pin auf TRUE setzen, was am Hardware-Ausgang einen
Motor anwerfen kann.

Force-Setzungen muss der **Mensch ueber die GUI** vornehmen. Die KI
kann sie sehen (im Live-Snapshot zeigt sie `forced=true`) aber
**nicht selber setzen**. Das ist eine **harte Trennung** —
unabhaengig vom Geschwindigkeits-Modus, unabhaengig vom Build-Flag.

Begruendung: ein geforcter Output bewegt **reale Hardware**. Schutz-
und Sicherheits-Funktionen koennten dadurch ausser Kraft gesetzt
werden. Ein KI-Agent darf solche Side-Effects nicht selbsttaetig
ausloesen — selbst wenn er glaubt es waere richtig.

---

## Was tun wenn etwas falsch laeuft?

1. **Notbremse** (roter STOP-Knopf im Chat-Reiter, nur sichtbar im
   Geschwindigkeits-Modus) → KI-Loop sofort abbrechen
2. **SPS stoppen** ueber das `Runtime`-Menue → Outputs in
   Safe-State
3. **Geforcte Variablen aufheben** ueber den Force-Tab im Variables-
   Panel
4. **Audit-Log lesen** unter `~/.config/ForgeIEC/mcp_audit.log` →
   was hat die KI nacheinander gemacht

---

## Empfehlungen

- **Entwicklung:** freigeschaltete Version, Trainee-Persona,
  langsamer Modus — Sie sehen jeden Schritt
- **Code-Review:** Reviewer-Persona — kann nichts kaputt machen
- **Diagnose auf Produktions-SPS:** Monitor-Persona — keine
  Aenderungen moeglich
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
- [Zurueck zur AI-Uebersicht](/help/ai/)
