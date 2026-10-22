---
title: "Die Personas im Einzelnen"
summary: "Welcher KI-Charakter darf was, und wann wählen Sie welchen"
---

## Warum mehrere Personas?

Eine SPS-Programmierumgebung braucht **verschiedene Sichtweisen**:

- Beim Coding wollen Sie schnell Variablen anlegen und compilieren.
- Beim Code-Review wollen Sie **keine** versehentlichen Änderungen.
- Beim Inbetriebnehmen schauen Sie nur Live-Werte an — nicht den Code.
- Beim Einarbeiten eines Lehrlings soll der KI-Helfer **alles
  einzeln nachfragen**, damit der Lehrling sieht was gerade passiert.

Statt dass Sie immer wieder das Sicherheits-Profil umstellen, hat
ForgeIEC **fertige Personas** eingebaut — jede mit ihrer eigenen
Rolle und ihrer eigenen Berechtigungs-Stufe.

Sie wechseln im AI-Reiter einfach zwischen den Karteikarten.

---

## Die sechs Personas

### Blacksmith Master — der Vorarbeiter

- **Wann wählen?** Standard für aktives Programmieren.
- **Was darf er?** Alles: Variablen anlegen, POU-Code schreiben,
  kompilieren, hochladen, SPS starten/stoppen, Werte beobachten.
- **Vorsicht:** Er kann eine SPS in den Stopp-Zustand bringen.
  Confirm-Rückfragen erscheinen aber bei jeder Aktion (außer im
  Geschwindigkeits-Modus, siehe [Bedienung](/help/ai/chat/)).

### Reviewer — der zweite Blick

- **Wann wählen?** Wenn Sie sich Ihren Code durchsehen lassen wollen
  bevor Sie ihn deployen.
- **Was darf er?** **Nur lesen**: Projekt-Variablen, POU-Bodies,
  Bibliotheks-Bausteine. Er kann **kein** Variable anlegen, **kein**
  Code ändern, **kein** Deploy auslösen.
- **Sicherheits-Vorteil:** Sie können ihn unkonzentriert chatten
  lassen — er wird **nichts kaputt machen können**, selbst wenn
  Sie ihn schlecht anweisen.

### Doc — der Dokumentar

- **Wann wählen?** Wenn Sie aus fertigem Code Kommentare oder eine
  Doku-Datei erzeugen lassen wollen.
- **Was darf er?** Lesen + Variablen-Kommentare schreiben. **Kein**
  Code-Body wird angefasst, **kein** Deploy.
- **Typischer Einsatz:** "Lies meine `MotorSteuerung`-POU und schreibe
  in jede Variable einen kurzen Kommentar was sie tut."

### Monitor — der Beobachter

- **Wann wählen?** Wenn Sie an einer laufenden Anlage Diagnose machen
  wollen, OHNE die Gefahr dass irgendwas geändert wird.
- **Was darf er?** **Ausschließlich** Live-Werte lesen, Oszilloskop-
  Aufnahmen abrufen, Task-Statistiken anzeigen.
- **Was darf er NICHT?** Keine Variablen anlegen, keine Force-Setzungen,
  kein Code-Anfassen, kein Deploy.
- **Typische Frage:** "Warum bleibt `Motor_Bereit` während des
  Startvorgangs auf FALSE? Schau dir die letzten 5 Sekunden auf
  dem Oszi an."

### Team Lead — der Koordinator

- **Wann wählen?** Wenn eine größere Aufgabe auf mehrere Personas
  verteilt werden soll.
- **Was darf er?** Projekt, Bibliothek, Katalog und Live-Werte
  **lesen**, die Aufgabe in Teilaufgaben zerlegen, sie an Blacksmith
  Master, Reviewer, Doc und Monitor weitergeben und deren Ergebnisse
  zusammenfassen.
- **Was darf er NICHT?** Selbst Code ändern, deployen oder die
  Runtime steuern.

### Trainee — für Einarbeitung und Erstkontakt

- **Wann wählen?** Wenn Sie einen neuen Mitarbeiter einarbeiten — oder
  selbst zum ersten Mal mit dem KI-Helfer arbeiten und alles
  Schritt-für-Schritt sehen wollen.
- **Was darf er?** Im Prinzip alles wie Blacksmith Master.
- **Was ist anders?** Der Geschwindigkeits-Modus ist hier **immer
  ausgeschaltet**. Jede einzelne Aktion erfordert Ihre Bestätigung
  per Klick. Auch wenn der Bearbeiter „Mach das, mach das, mach das"
  hintereinander tippt, kommt nach jedem Schritt eine Rückfrage.

---

## Personas anpassen oder eigene anlegen

Personas verwalten Sie unter **Preferences → AI** → Tab **„AI Agent
Profiles"**:

- **`+`** unter der Profile-Liste — neues Profil anlegen.
- **`-`** — markiertes Profil löschen.
- **Liste anklicken** → rechts erscheinen Name / Role / Endpoint /
  Model / API-Key / Enabled / System-Prompt zum Editieren.
- **„Reset to defaults"** — alle Personas auf die Werks-Defaults
  zurücksetzen (löscht User-Anpassungen).

Der **System-Prompt** ist der Text, mit dem die KI bei jeder Anfrage
„geimpft" wird. Hier geben Sie Stil, Sprache, Detailgrad und
Domänen-Wissen mit (z.B. „Antworte immer auf Deutsch, technisch
knapp"). Jede Persona hat zusätzlich eine **Role**, die den
verfügbaren MCP-Tool-Satz festlegt — siehe
[Sicherheit](/help/ai/security/) und [Werkzeuge](/help/ai/tools/).

---

## Welche Persona für welche Aufgabe?

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
- [Was die KI kann](/help/ai/tools/) — Aktionen-Übersicht
- [Zurück zur AI-Übersicht](/help/ai/)
