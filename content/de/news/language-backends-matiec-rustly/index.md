---
title: "Offene Sprach-Erweiterung: matiec → matiec++ → rustly als Evolutionspfad"
date: 2026-05-14
summary: "Drei IEC-61131-3-Backends parallel — mit klarer Reihenfolge: matiec heute, matiec++ als naechstes, rustly als Ziel."
components: [studio]
---

{{< components "studio" >}}

## Worum es geht

ForgeIEC's Codegen-Schicht ist nicht an einen Compiler
gebunden. Wir trennen seit Beginn die **Sprach-Spezifikation**
(IEC 61131-3) von der **Implementierung** (welcher Compiler
das ST in Maschinen-Code uebersetzt). Daraus folgt: wir
koennen den Compiler-Backend austauschen, ohne dass sich an
der Sprache aus Anwender-Sicht etwas aendert.

Wir nutzen das pragmatisch — nicht als akademische Uebung. Die
Reihenfolge ist:

1. **matiec** — die etablierte ST→C-Pipeline aus dem
   Beremiz-Universum. Heute der Default fuer jedes neue
   ForgeIEC-Projekt. Pro Konstrukt dokumentiert in der
   neuen [IEC-Reference](/reference/iec61131-3/), inklusive
   der bekannten Quirks.
2. **matiec++** — die in Vorbereitung befindliche C++-Variante.
   Generiert C++ statt C, was mehrere Probleme der heutigen
   Variante adressiert (sauberere Type-Checks, bessere
   Diagnose-Messages, bessere Generic-Handling). Plan-Doku
   in der internen Codegen-v1-Spec; Sprint-Sequenz a → a.5 →
   b → c → d → e → f.
3. **rustly** — pre-1.0 IEC-Compiler in Rust + LLVM. Das
   strategische Ziel. Bietet Online-Change als
   Differentiator-Feature (matiec/matiec++ koennen das nicht
   strukturell), liefert moderne Diagnose-Messages und ist
   die Grundlage fuer alles, was wir an Compile-Time-Analyse
   in Zukunft tun wollen (Property-Checks, Liveness-Analyse,
   formale Verifikation).

**Genau diese Reihenfolge wird die Evolution.** Wir migrieren
nicht hoch-und-runter zwischen Backends; wir wandern entlang
einer monoton wachsenden Reife-Kette.

## Warum drei Backends?

Weil keiner alleine alle drei Anforderungen erfuellt:

| Anforderung | matiec | matiec++ | rustly |
|---|---|---|---|
| Bewaehrt in der Praxis | ✓ | (in Entwicklung) | (Pre-1.0) |
| Standard-Konformitaet IEC 61131-3 | ✓ | ✓ | ✓ |
| Saubere Diagnose-Messages | ✗ | (verbessert) | ✓ |
| Online-Change | ✗ | ✗ | ✓ |
| Property-Checks bei Compile | ✗ | (geplant) | ✓ |
| Sprache: Implementierung | C | C++ | Rust + LLVM |

Wir koennen heute schon ForgeIEC mit matiec produktiv
betreiben, naechstes Jahr Projekte mit matiec++ deployen und
in 2-3 Jahren auf rustly umsteigen — alles ohne dass das
ST-Source des Anwenders sich aendern muss. Das **ST ist die
Schnittstelle**; der Compiler ist austauschbar.

## Was bedeutet das praktisch?

- **Bibliotheken werden Backend-aware**. Das in Vorbereitung
  befindliche [Library-System](#) (`.forge_lib`-Dateiformat,
  in Planung) traegt pro POU eine Backend-Markierung. Eine
  Library kann gleichzeitig matiec-, matiec++- und rustly-
  Implementierungen liefern; das konsumierende Projekt
  picked sich raus, was es braucht.
- **Die IEC-Reference ist Compiler-agnostisch geschrieben**
  und dokumentiert die matiec-spezifischen Quirks separat in
  einem `matiec conformance`-Abschnitt pro Konstrukt-Seite.
  Sobald matiec++ und rustly da sind, kommen weitere
  Conformance-Abschnitte hinzu — die Spec-Abschnitte aendern
  sich nicht.
- **Die LLM-Auto-Fix-Bloecke (`llm_signals[]`)** sind
  ebenfalls per-Backend annotiert. Ein `where: matiec`-Signal
  feuert nicht, wenn das Projekt auf rustly compiliert wird.

## Was als naechstes kommt

- Die existing matiec-Quirks systematisch in die
  IEC-Reference einbauen (laeuft bereits — neun Patterns
  dokumentiert, mehr kommen).
- matiec++-Backend als eigene Codegen-Layer in den Editor
  integrieren. Sprint-Sequenz steht intern.
- rustly-Evaluation als Drittprojekt anstossen — Memory-
  Eintrag `project_rusty_evaluation` faengt das auf.

Drei Backends sind kein Abenteuer, sondern eine ruhige
Migrations-Strategie. Was heute mit matiec geht, geht morgen
mit matiec++ und uebermorgen mit rustly — nur leiser, sauberer
und mit besseren Werkzeugen.
