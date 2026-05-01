---
title: "Ladder Diagram Editor (LD)"
summary: "Stromlaufplan-Metapher: Power-Rails, Kontakte, Spulen"
---

## Ueberblick

Ladder Diagram (LD) ist die aelteste der drei grafischen IEC-61131-3-Sprachen
und folgt der **Stromlaufplan-Metapher**: Zwischen einer linken und einer
rechten **Power-Rail** verlaufen horizontale **Strompfade** (Rungs). Auf
jedem Rung sitzen Kontakte (links, in Reihe) und Spulen (rechts), die das
Signal je nach Variablenzustand „leiten" oder „sperren". LD eignet sich
besonders fuer einfache Steuerungen — Endlagenschaltungen, Selbsthaltungen,
Verriegelungen — und ist fuer Elektroplaner intuitiv lesbar.

## Editor-Layout

Der LD-Editor hat den gleichen Aufbau wie der FBD-Editor (Toolbar oben,
QGraphicsView mit Grid + Zoom + Pan, Variablentabelle rechts), mit
zwei Besonderheiten:

* **Linke Power-Rail** und **rechte Power-Rail** stehen als spezielle
  Items dauerhaft im Diagramm. Sie sind nicht verschiebbar und wachsen
  vertikal mit der Anzahl der Rungs.
* Die Toolbar enthaelt zusaetzliche Aktionen fuer LD-Symbole (Kontakte,
  Spulen, Edge-Trigger) und einen `Add Rung`-Button, der eine neue
  Rung-Verbindung zwischen den Power-Rails einfuegt.

## Symbole

### Kontakte (links auf dem Rung)

| Symbol | Bedeutung |
|---|---|
| `--\| \|--` | **Schliesser (NO)** — leitet, wenn die Variable TRUE ist |
| `--\|/\|--` | **Oeffner (NC)** — leitet, wenn die Variable FALSE ist |
| `--\|P\|--` | **Rising-Edge-Kontakt** — leitet einen Zyklus lang bei steigender Flanke |
| `--\|N\|--` | **Falling-Edge-Kontakt** — leitet einen Zyklus lang bei fallender Flanke |

Mehrere Kontakte in Reihe wirken als logisches **AND**, parallele Pfade
als logisches **OR**.

### Spulen (rechts auf dem Rung)

| Symbol | Bedeutung |
|---|---|
| `--( )` | **Standard-Spule** — schreibt den aktuellen Pfad-Zustand in die Variable |
| `--(/)` | **Negierte Spule** — schreibt den invertierten Zustand |
| `--(S)` | **Set-Spule** — setzt die Variable auf TRUE und haelt sie (auch wenn der Pfad spaeter wieder oeffnet) |
| `--(R)` | **Reset-Spule** — setzt die Variable auf FALSE und haelt sie |

Set/Reset-Paare ergeben eine Selbsthaltung, ohne explizite IF-THEN-Logik.

### Funktionsbloecke im Pfad

Funktionen und Funktionsbloecke aus der Library koennen **inline zwischen
Kontakten und Spulen** eingebaut werden. Der LD-Editor zeichnet sie als
horizontale Box mit Pin-Liste rechts/links — semantisch identisch zum
FBD-Block. Typischer Einsatz: Timer (`TON`), Zaehler (`CTU`), Vergleicher
(`GT`, `EQ`).

## Beispiel — Selbsthaltung mit Stop-Vorrang

Eine klassische Schuetz-Schaltung: Ein Start-Taster `xStart` schaltet einen
Motor `qMotor` ein, ein Stop-Taster `xStop` schaltet ihn aus. Solange
`xStart` gedrueckt war und `xStop` nicht, bleibt der Motor an
(Selbsthaltung).

```text
        |                                              |
        |   xStart      xStop                          |
   +----| |---+--|/|---+-----------------------( )----+
        |    |         |                       qMotor  |
        |    |         |                                |
        |   qMotor     |                                |
        +----| |-------+                                |
        |                                              |
```

Sprachlich gesprochen:

  * `xStart` (NO) **oder** `qMotor` (Selbsthalte-Kontakt, NO) — parallel,
  * **und** `xStop` (NC) — in Reihe,
  * setzt die Spule `qMotor`.

Beim Compile uebersetzt der LD-Compiler diesen Pfad zu:

```text
qMotor := (xStart OR qMotor) AND NOT xStop;
```

Das ist die einfachste Form einer Selbsthaltung mit Stop-Vorrang. Wenn
beide Taster gleichzeitig gedrueckt werden, gewinnt `xStop`, weil der
NC-Kontakt den Strompfad oeffnet.

## Verwandte Themen

* [Function Block Diagram](../fbd/) — datenfluss-orientierte Schwester-Sprache.
* [Library](../library/) — Funktionsbloecke fuer Inline-Einsatz im Pfad
  (`TON`, `CTU`, `JK_FF`, `DEBOUNCE`).
* [Variables Panel](../variables/) — Adress-Pool und Variablenbindung.
