---
title: "Offene Sprach-Erweiterung: matiec → matiec++ → rustly als Evolutionspfad"
date: 2026-05-14
summary: "Drei IEC-61131-3-Backends parallel — mit klarer Reihenfolge: matiec heute, matiec++ als nächstes, rustly als Ziel."
components: [studio]
---

{{< components "studio" >}}

{{< callout type="note" title="Nachtrag Oktober 2026" >}}
matiec ist abgelöst. ForgeIEC übersetzt ST mit einem eigenen Kern nach
C++, der auch die objektorientierten Erweiterungen (METHOD, INTERFACE,
EXTENDS) beherrscht. Der folgende Beitrag gibt den Stand vom Mai 2026
wieder.
{{< /callout >}}
<!-- ENTWURF: Ob eine Rust+LLVM-Migration ("rustly"/"rusty") noch Plan ist, ist offen (Audit W-16). Der Beitrag bleibt als historischer Stand stehen. -->

## Worum es geht

ForgeIEC's Codegen-Schicht ist nicht an einen Compiler
gebunden. Wir trennen seit Beginn die **Sprach-Spezifikation**
(IEC 61131-3) von der **Implementierung** (welcher Compiler
das ST in Maschinen-Code übersetzt). Daraus folgt: wir
können den Compiler-Backend austauschen, ohne dass sich an
der Sprache aus Anwender-Sicht etwas ändert.

Wir nutzen das pragmatisch — nicht als akademische Übung. Die
Reihenfolge ist:

1. **matiec** — die etablierte ST→C-Pipeline aus dem
   Beremiz-Universum. Heute der Default für jedes neue
   ForgeIEC-Projekt. Pro Konstrukt dokumentiert in der
   neuen [IEC-Reference](/en/reference/iec61131-3/), inklusive
   der bekannten Quirks.
2. **matiec++** — die in Vorbereitung befindliche C++-Variante.
   Generiert C++ statt C, was mehrere Probleme der heutigen
   Variante adressiert (sauberere Type-Checks, bessere
   Diagnose-Messages, bessere Generic-Handling). Plan-Doku
   in der internen Codegen-v1-Spec; Sprint-Sequenz a → a.5 →
   b → c → d → e → f.
3. **rustly** — pre-1.0 IEC-Compiler in Rust + LLVM. Das
   strategische Ziel. Bietet Online-Change als
   Differentiator-Feature (matiec/matiec++ können das nicht
   strukturell), liefert moderne Diagnose-Messages und ist
   die Grundlage für alles, was wir an Compile-Time-Analyse
   in Zukunft tun wollen (Property-Checks, Liveness-Analyse,
   formale Verifikation).

**Genau diese Reihenfolge wird die Evolution.** Wir migrieren
nicht hoch-und-runter zwischen Backends; wir wandern entlang
einer monoton wachsenden Reife-Kette.

## Warum drei Backends?

Weil keiner alleine alle drei Anforderungen erfüllt:

| Anforderung | matiec | matiec++ | rustly |
|---|---|---|---|
| Bewährt in der Praxis | ✓ | (in Entwicklung) | (Pre-1.0) |
| Standard-Konformität IEC 61131-3 | ✓ | ✓ | ✓ |
| Saubere Diagnose-Messages | ✗ | (verbessert) | ✓ |
| Online-Change | ✗ | ✗ | ✓ |
| Property-Checks bei Compile | ✗ | (geplant) | ✓ |
| Sprache: Implementierung | C | C++ | Rust + LLVM |

Wir können heute schon ForgeIEC mit matiec produktiv
betreiben, nächstes Jahr Projekte mit matiec++ deployen und
in 2-3 Jahren auf rustly umsteigen — alles ohne dass das
ST-Source des Anwenders sich ändern muss. Das **ST ist die
Schnittstelle**; der Compiler ist austauschbar.

## Was bedeutet das praktisch?

- **Bibliotheken werden Backend-aware**. Das in Vorbereitung
  befindliche [Library-System](/de/help/library/) (`.forge_lib`-Dateiformat,
  in Planung) trägt pro POU eine Backend-Markierung. Eine
  Library kann gleichzeitig matiec-, matiec++- und rustly-
  Implementierungen liefern; das konsumierende Projekt
  picked sich raus, was es braucht.
- **Die IEC-Reference ist Compiler-agnostisch geschrieben**
  und dokumentiert die matiec-spezifischen Quirks separat in
  einem `matiec conformance`-Abschnitt pro Konstrukt-Seite.
  Sobald matiec++ und rustly da sind, kommen weitere
  Conformance-Abschnitte hinzu — die Spec-Abschnitte ändern
  sich nicht.
- **Die LLM-Auto-Fix-Blöcke (`llm_signals[]`)** sind
  ebenfalls per-Backend annotiert. Ein `where: matiec`-Signal
  feuert nicht, wenn das Projekt auf rustly compiliert wird.

## Was als nächstes kommt

- Die existing matiec-Quirks systematisch in die
  IEC-Reference einbauen (läuft bereits — neun Patterns
  dokumentiert, mehr kommen).
- matiec++-Backend als eigene Codegen-Layer in den Editor
  integrieren. Sprint-Sequenz steht intern.
- rustly-Evaluation als Drittprojekt anstoßen — Memory-
  Eintrag `project_rusty_evaluation` fängt das auf.

Drei Backends sind kein Abenteuer, sondern eine ruhige
Migrations-Strategie. Was heute mit matiec geht, geht morgen
mit matiec++ und übermorgen mit rustly — nur leiser, sauberer
und mit besseren Werkzeugen.
