---
title: "Bedienung im Alltag"
summary: "Eingabe, Eingabe-Historie, Notbremse, Geschwindigkeits-Modus, Tool-Schritte-Grenze"
---

## Der Chat-Bereich

Im rechten Editor-Dock sitzt der Reiter `AI Assistant`. Aufbau von
oben nach unten:

1. **Persona-Karteikarten** — Blacksmith Master, Reviewer, Doc, …
2. **Server-Adresse + Modell-Auswahl** — wo lauft die KI, welches
   Modell
3. **Verlauf** — Chat-Historie zwischen Ihnen und dem Helfer
4. **Eingabe-Feld** unten — hier tippen Sie Ihre Frage
5. **Sicherheits-Banner** (gelb mit rotem STOP-Knopf) — erscheint nur
   wenn der Geschwindigkeits-Modus aktiv ist

---

## Eine Anfrage stellen

Tippen Sie Ihre Frage normal ins Eingabefeld und druecken Sie
**Enter**.

> „Lege mir 16 BOOL-Variablen `LED_00` bis `LED_15` an,
> auf den Adressen `%MX0.0` bis `%MX1.7`, mit Bellows-Export."

Der Helfer fasst zunaechst Ihre Anfrage in Schritte zusammen, fuehrt
sie aus, fragt bei jeder schreibenden Aktion zurueck und gibt am Ende
einen Bericht.

---

## Eingabe-Historie — Pfeil hoch / runter

Wie in einer Linux-Shell:

- **Pfeil hoch** im Eingabe-Feld → letzte Eingabe wieder rausholen
- **Pfeil runter** → naechst-juengere Eingabe
- Spart Tippen wenn Sie eine aehnliche Frage variieren wollen

---

## Notbremse — der rote STOP-Knopf

Wenn der Geschwindigkeits-Modus aktiv ist (siehe naechster Abschnitt),
erscheint **unten ein gelber Sicherheits-Streifen** mit einem **roten
runden STOP-Knopf** rechts daneben.

**Druecken Sie ihn jederzeit** wenn die KI etwas tut das Sie nicht
wollen. Er unterbricht **sofort**:

- Den laufenden Modell-Aufruf
- Alle wartenden Tool-Schritte
- Eventuell offene Confirm-Rueckfragen werden auf „cancel" gesetzt

Der Knopf ist genauso ausgelegt wie die klassische Industrie-Pilz-
Taster: gross, rot, leicht zu treffen, immer erreichbar.

---

## Der Geschwindigkeits-Modus (Danger-Mode)

Standardmaessig stellt ForgeIEC Studio bei **jeder** schreibenden
Aktion der KI eine Rueckfrage. Das ist sicher, aber langsam — wenn die KI
50 Variablen anlegen soll, klickt man sich 50× durch.

**Im Geschwindigkeits-Modus** beantwortet ForgeIEC Studio diese Rueckfragen
**automatisch mit „yes"**. Der LLM-Loop kann dann ohne menschliche
Unterbrechung durchlaufen. Empfohlen nur fuer **Test-Setups** oder
**experimentelle Iteration** — in Produktion sollten Sie ihn
**ausschalten**.

**So schalten Sie um:**

`Preferences -> AI` → Haken bei `Danger Mode — auto-confirm AI tool calls`.

Beim Einschalten erscheint eine zusaetzliche Sicherheits-Warnung mit
dem Hinweis dass dieser Modus **nicht** auf einer produktiven SPS
laufen soll. Bestaetigen Sie nur wenn Sie das verstanden haben.

Beim Wechsel zwischen Personas bleibt der Modus pro Persona
gespeichert — Sie koennen also nur den Blacksmith Master schnell
machen und den Trainee weiterhin langsam betreiben.

---

## Tool-Schritte-Grenze (max_tool_turns)

Eine einzelne Anfrage von Ihnen kann beim Helfer **mehrere
Werkzeug-Aufrufe** ausloesen. Beispiel: „Knight-Rider-Programm
anlegen" macht intern:

1. POU `KnightRider` anlegen
2. 16 LED-Variablen anlegen
3. POU-Body schreiben
4. Kompilieren
5. Deployen
6. SPS starten

Das sind schon 21 Schritte. Damit der Helfer nicht in eine
Endlos-Schleife laeuft, gibt es eine **Schritt-Grenze pro Anfrage**.

**Standard: 10 Schritte.** Reicht fuer einfache Anfragen.

**Anpassen** ueber `Preferences -> AI -> Max tool turns per user request`.
Erlaubte Werte: 1 bis 1000.

**Im Geschwindigkeits-Modus** wird die Grenze **automatisch
deaktiviert** — wenn Sie schon der KI vertraut haben, soll sie auch
einen langen Job durchziehen koennen.

Wenn die Grenze erreicht ist, bricht der Helfer kontrolliert ab und
sagt: „Tool-loop guard hit max N turns; aborted." Sie koennen dann
„weiter" tippen, und er macht ab dort weiter.

---

## Was tun wenn die KI sich verirrt?

Manchmal probiert ein Modell denselben Fehler 3-4 mal hintereinander.
Hilfreich:

- **STOP-Knopf** → Loop sauber abbrechen
- **Anders fragen** — kuerzer, konkreter, mit Adressen statt Namen
- **Persona wechseln** — Reviewer findet manchmal den Fehler den
  Blacksmith Master uebersieht
- **Modell wechseln** — wenn Ihr lokales Modell zu klein ist, kann
  ein groesseres Modell denselben Auftrag in einem Versuch loesen

---

## Weiter

- [Was die KI kann](/help/ai/tools/) — Liste der moeglichen Aktionen
- [Sicherheits-Modell](/help/ai/security/) — Details zum Geschwindigkeits-
  Modus
- [Personas](/help/ai/agents/) — welcher Charakter fuer welche Aufgabe
- [Zurueck zur AI-Uebersicht](/help/ai/)
