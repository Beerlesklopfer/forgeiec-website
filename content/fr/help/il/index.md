---
title: "Éditeur Instruction List"
summary: "Éditeur IL : langage IEC 61131-3 basé sur accumulateur avec registre CR"
---

## Vue d'ensemble

**Instruction List (IL)** est le langage texte de type assembleur de
IEC 61131-3 et historiquement le premier des cinq langages IEC. Les
programmes sont des séquences d'instructions qui manipulent un seul
**registre accumulateur** interne — le *Current Result* (`CR`). Chaque
ligne est une instruction de la forme

```
[Label:] Operator [Modifier] [Operand] (* Comment *)
```

et lit ou écrit soit dans l'accumulateur, soit dans une variable
externe.

Dans ForgeIEC, IL est édité via le `FIlEditor` — la disposition et
l'outillage sont analogues à l'[éditeur ST](../st/).

## Disposition de l'éditeur

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT)             |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (tree-sitter-instruction-list grammar) |
+----------------------------------------+
```

| Zone | Contenu |
|---|---|
| **Tableau de variables** (haut) | Déclarations avec Nom, Type, Valeur initiale, Adresse, Commentaire — synchronisé avec le bloc `VAR ... END_VAR`. |
| **Zone de code** (bas) | Source IL avec coloration tree-sitter (grammaire `tree-sitter-instruction-list`). |
| **Barre de recherche** (Ctrl-F / Ctrl-H) | Barre de rechercher-remplacer. |

Le mode en ligne et la superposition de valeurs en ligne fonctionnent
de manière identique à l'éditeur ST.

## Modèle d'accumulateur

L'accumulateur (`CR`) contient le résultat intermédiaire de
l'évaluation en cours. Une séquence typique :

  1. `LD x` — charger `x` dans l'accumulateur (`CR := x`)
  2. `AND y` — combiner l'accumulateur avec `y` (`CR := CR AND y`)
  3. `ST z` — stocker l'accumulateur dans `z` (`z := CR`)

Cela fait d'IL une **machine à un seul registre, sans pile** — très
proche des plateformes microcontrôleur qui dominaient lorsque le
langage a été normalisé en 1993.

## Opérateurs clés

| Groupe | Opérateurs | Effet |
|---|---|---|
| **Load / Store** | `LD`, `LDN`, `ST`, `STN` | Définir l'accumulateur / stocker l'accumulateur (`N` = nié) |
| **Set / Reset** | `S`, `R` | Mettre à 1 / remettre à 0 un bit (variable BOOL, quand `CR` = TRUE) |
| **Logique bit** | `AND`, `OR`, `XOR`, `NOT` | Combiner l'accumulateur avec l'opérande |
| **Arithmétique** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` | Accumulateur + opérande → accumulateur |
| **Comparaison** | `GT`, `GE`, `EQ`, `NE`, `LE`, `LT` | Résultat de comparaison dans `CR` |
| **Saut** | `JMP`, `JMPC`, `JMPCN` | Saut vers étiquette (`C` = quand `CR` = TRUE) |
| **Appel** | `CAL`, `CALC`, `CALCN` | Appel d'instance de bloc fonctionnel |
| **Retour** | `RET`, `RETC`, `RETCN` | Quitter le POU |

## Modificateurs

Un opérateur peut être affiné via des modificateurs en suffixe :

| Modificateur | Signification |
|---|---|
| `N` | **Négation** de l'opérande (`LDN x` charge `NOT x`) |
| `C` | **Conditionnel** — n'exécute que quand `CR` = TRUE (`JMPC label`) |
| `(`...`)` | **Modificateur de parenthèse** — diffère l'évaluation jusqu'à la fermeture de `)` |

La forme parenthésée permet des expressions composées sans variables
intermédiaires :

```
LD   a
AND( b
OR   c
)
ST   result            (* result := a AND (b OR c) *)
```

## Quand utiliser IL au lieu de ST

ST est le choix par défaut aujourd'hui. IL a encore du sens quand :

  - **La performance microcontrôleur** est décisive — IL se mappe 1:1
    aux instructions machine dans la plupart des back-ends matiec, sans
    optimisation intermédiaire.
  - **Des systèmes hérités** doivent rester compatibles (logique
    AWL S5/S7-dérivée, base installée plus ancienne ABB / Beckhoff).
  - **Blocs de logique très compacts** — verrouillages, latches,
    conditions de front sont souvent deux lignes plus courtes en IL
    qu'en ST.

Pour tout le reste, ST est plus lisible et plus facile à maintenir.

## Exemple de code — contacteur auto-maintenu avec contacts NO/NC

**Auto-maintien classique de contacteur** en IL : appuyer sur `start`
alimente le contacteur `K1`, le bouton `stop` (NC, actif bas) le
relâche. Logique :

```
K1 := (start OR K1) AND NOT stop
```

En IL :

```
PROGRAM Selbsthaltung
VAR
    start  AT %IX0.0 : BOOL;       (* NO push-button *)
    stop   AT %IX0.1 : BOOL;       (* NC push-button, low-active *)
    K1     AT %QX0.0 : BOOL;       (* contactor *)
END_VAR

    LD    start
    OR    K1                    (* CR := start OR K1 *)
    ANDN  stop                  (* CR := CR AND NOT stop *)
    ST    K1                    (* K1 := CR *)
END_PROGRAM
```

Quatre instructions, un registre, pas de stockage temporaire.
Exactement le genre de construction pour lequel IL a été conçu à
l'origine.

## Sujets liés

- [Structured Text](../st/) — le langage sœur de type Pascal
- [Bibliothèque](../library/) — blocs fonctionnels appelables via `CAL`
- [Format de fichier de projet](../file-format/) — corps IL dans
  `<body><IL>...`
