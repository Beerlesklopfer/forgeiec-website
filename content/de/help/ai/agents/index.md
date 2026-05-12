---
title: "Die Personas im Einzelnen"
summary: "Welcher KI-Charakter darf was, und wann waehlen Sie welchen"
---

## Warum mehrere Personas?

Eine SPS-Programmierumgebung braucht **verschiedene Sichtweisen**:

- Beim Coding wollen Sie schnell Variablen anlegen und compilieren.
- Beim Code-Review wollen Sie **keine** versehentlichen Aenderungen.
- Beim Inbetriebnehmen schauen Sie nur Live-Werte an — nicht den Code.
- Beim Einarbeiten eines Lehrlings soll der KI-Helfer **alles
  einzeln nachfragen**, damit der Lehrling sieht was gerade passiert.

Statt dass Sie immer wieder das Sicherheits-Profil umstellen, hat
ForgeIEC **fertige Personas** eingebaut — jede mit ihrer eigenen
Rolle und ihrer eigenen Berechtigungs-Stufe.

Sie wechseln im AI-Reiter einfach zwischen den Karteikarten.

---

## Die fuenf Personas

### Blacksmith Master — der Vorarbeiter

- **Wann waehlen?** Standard fuer aktives Programmieren.
- **Was darf er?** Alles: Variablen anlegen, POU-Code schreiben,
  kompilieren, hochladen, SPS starten/stoppen, Werte beobachten.
- **Vorsicht:** Er kann eine SPS in den Stopp-Zustand bringen.
  Confirm-Rueckfragen erscheinen aber bei jeder Aktion (ausser im
  Geschwindigkeits-Modus, siehe [Bedienung](/help/ai/chat/)).

### Reviewer — der zweite Blick

- **Wann waehlen?** Wenn Sie sich Ihren Code durchsehen lassen wollen
  bevor Sie ihn deployen.
- **Was darf er?** **Nur lesen**: Projekt-Variablen, POU-Bodies,
  Bibliotheks-Bausteine. Er kann **kein** Variable anlegen, **kein**
  Code aendern, **kein** Deploy ausloesen.
- **Sicherheits-Vorteil:** Sie koennen ihn unkonzentriert chatten
  lassen — er wird **nichts kaputt machen koennen**, selbst wenn
  Sie ihn schlecht anweisen.

### Doc — der Dokumentar

- **Wann waehlen?** Wenn Sie aus fertigem Code Kommentare oder eine
  Doku-Datei erzeugen lassen wollen.
- **Was darf er?** Lesen + Variablen-Kommentare schreiben. **Kein**
  Code-Body wird angefasst, **kein** Deploy.
- **Typischer Einsatz:** "Lies meine `MotorSteuerung`-POU und schreibe
  in jede Variable einen kurzen Kommentar was sie tut."

### Monitor — der Beobachter

- **Wann waehlen?** Wenn Sie an einer laufenden Anlage Diagnose machen
  wollen, OHNE die Gefahr dass irgendwas geaendert wird.
- **Was darf er?** **Ausschliesslich** Live-Werte lesen, Oszilloskop-
  Aufnahmen abrufen, Task-Statistiken anzeigen.
- **Was darf er NICHT?** Keine Variablen anlegen, keine Force-Setzungen,
  kein Code-Anfassen, kein Deploy.
- **Typische Frage:** "Warum bleibt `Motor_Bereit` waehrend des
  Startvorgangs auf FALSE? Schau dir die letzten 5 Sekunden auf
  dem Oszi an."

### Trainee — fuer Einarbeitung und Erstkontakt

- **Wann waehlen?** Wenn Sie einen neuen Mitarbeiter einarbeiten — oder
  selbst zum ersten Mal mit dem KI-Helfer arbeiten und alles
  Schritt-fuer-Schritt sehen wollen.
- **Was darf er?** Im Prinzip alles wie Blacksmith Master.
- **Was ist anders?** Der Geschwindigkeits-Modus ist hier **immer
  ausgeschaltet**. Jede einzelne Aktion erfordert Ihre Bestaetigung
  per Klick. Auch wenn der Bearbeiter „Mach das, mach das, mach das"
  hintereinander tippt, kommt nach jedem Schritt eine Rueckfrage.

---

## Eigenen Charakter anlegen

Sie koennen die mitgelieferten Personas anpassen oder neue erstellen:

- **Rechtsklick auf einen Reiter** → `Duplicate Profile`
- **Preferences → AI** → System-Prompt anpassen
  (z.B. „Antworte immer auf Deutsch, technisch knapp")

Der **System-Prompt** ist der Text, mit dem die KI bei jeder Anfrage
„geimpft" wird. Hier koennen Sie Stil, Sprache, Detailgrad,
Domaenen-Wissen mitgeben.

---

## Welche Persona fuer welche Aufgabe?

| Sie wollen … | Persona |
|---|---|
| Neues Programm schreiben | Blacksmith Master |
| Code-Review vor dem Deploy | Reviewer |
| Doku aus fertigem Code | Doc |
| Anlage in Betrieb diagnostizieren | Monitor |
| Lehrling einlernen | Trainee |
| Erste Schritte mit dem Helfer | Trainee, dann Blacksmith Master |

---

## Weiter

- [Bedienung im Alltag](/help/ai/chat/) — Eingabe-Tricks, Notbremse
- [Was die KI kann](/help/ai/tools/) — Aktionen-Uebersicht
- [Zurueck zur AI-Uebersicht](/help/ai/)
