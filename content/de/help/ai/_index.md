---
title: "Der KI-Helfer in ForgeIEC Studio"
summary: "Wie Sie den eingebauten KI-Assistenten zum Programmieren, Diagnostizieren und Inbetriebnehmen nutzen"
---

## Was ist das?

ForgeIEC Studio hat einen **KI-Helfer eingebaut** — direkt im
Hauptfenster, im rechten Reiter `AI Assistant`. Sie können mit ihm
in normalem Deutsch oder Englisch reden, und er kann **selbst im
ForgeIEC Studio arbeiten**:

- Variablen anlegen und Adressen vergeben
- POU-Code (ST) schreiben oder ändern
- Programme kompilieren und auf die SPS spielen
- Live-Werte beobachten während die SPS läuft
- Zeitliche Verläufe auf das Oszilloskop legen

Der Helfer ist **nicht zwingend** ein Cloud-Dienst — er kann auch
komplett **auf Ihrem eigenen Rechner laufen**, ganz ohne Internet,
mit einem lokalen KI-Programm (z.B. LM-Studio oder llama.cpp).

---

## Mehrere Charaktere für verschiedene Aufgaben

Der Helfer hat **mehrere Personas** — jede mit ihrer eigenen Aufgabe.
Sie wechseln im AI-Reiter zwischen den Karteikarten:

| Persona | Was sie tut |
|---|---|
| **Blacksmith Master** | Der Vorarbeiter — schreibt Code, kompiliert, deployt. Standard für aktive Entwicklung. |
| **Reviewer** | Liest Ihren Code durch und gibt Verbesserungsvorschläge. Verändert nichts selbst. |
| **Doc** | Schreibt Kommentare und Beschreibungen zu Ihrem Programm. |
| **Monitor** | Beobachtet nur die laufende SPS — perfekt für Diagnose-Arbeiten. Keine Änderungen möglich. |
| **Trainee** | Wie der Vorarbeiter, aber **jede** Aktion muss von Ihnen einzeln freigegeben werden. Für Einarbeitung neuer Mitarbeiter oder erste Tests. |

Mehr Details: [Die Personas im Einzelnen](/help/ai/agents/).

---

## Sicherheit — kurz gesagt

Der KI-Helfer kann **nicht aus Versehen** Ihre laufende Anlage
beschädigen. Drei Stufen schützen Sie:

1. **Standard-Auslieferung ist sicher.** Wenn Sie ForgeIEC frisch aus
   dem APT-Repository installieren, kann die KI **nur lesen**.
   Variablen anlegen, kompilieren und deployen sind alles
   **abgeschaltet**.
2. **Eingeschaltet werden muss bewusst.** Um schreibende Aktionen zu
   erlauben, müssen Sie eine spezielle Version des Editors
   installieren — das ist eine echte Hardware-ähnliche Trennung, kein
   Hakchen das man aus Versehen setzt.
3. **Der Operator entscheidet bei jeder Aktion.** Selbst in der
   freigeschalteten Version stellt der Editor bei **jeder**
   Veränderung eine Rückfrage:
   > „Position-Variable anlegen mit Adresse `%MD100`? (yes / cancel)"
   Erst mit Ihrer Bestätigung passiert wirklich was.

Mehr dazu: [Sicherheits-Modell](/help/ai/security/).

---

## Erste Schritte

1. **Editor starten** und im rechten Dock den Reiter `AI Assistant`
   anwählen.
2. **Server-Adresse eintragen** — wo lauft Ihr KI-Programm?
   - Lokal auf demselben Rechner: meist
     `http://localhost:1234/v1` (LM-Studio default).
   - Im Firmen-Netz: die Adresse die Ihre IT genannt hat.
3. **Modell auswählen** im rechten Drop-Down — z.B. `qwen3-coder-30b`,
   `gpt-4o-mini`, `claude-opus-4-7`.
4. **Persona auswählen** — für den Anfang ist **Blacksmith Master**
   richtig.
5. **Eine erste Anfrage stellen**, ganz normal in Deutsch:
   > „Lege mir eine Variable `Druck_1` als REAL auf Adresse `%MD200`
   > an. Mit Bellows-Export."

Der Helfer wird die Variable anlegen, eine Rückfrage bringen
(„yes / cancel"), und nach Ihrer Bestätigung im Variables-Tab
erscheinen.

---

## Weiterführende Themen

- [Die Personas im Einzelnen](/help/ai/agents/) — was jeder Charakter
  konkret darf
- [Bedienung im Alltag](/help/ai/chat/) — Eingabe-Tricks, Notbremse,
  Geschwindigkeits-Modus
- [Was die KI kann](/help/ai/tools/) — Aktionen-Übersicht in Klartext
- [Mehrere Workstations verbinden](/help/ai/team/) — Team-Mode,
  Kollegen aufnehmen, Vertrauenskette
- [Sicherheits-Modell](/help/ai/security/) — wie der Schutz im Detail
  funktioniert

---

<div style="text-align:center; padding: 2rem;">

**Die KI ist Werkzeug. Sie entscheiden.**

blacksmith@forgeiec.io

</div>
