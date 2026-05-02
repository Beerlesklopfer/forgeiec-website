---
title: "Éditeur Structured Text"
summary: "Éditeur ST + fondamentaux du langage : instructions IEC 61131-3, accès bit, références qualifiées vers le pool"
---

## Vue d'ensemble

**Structured Text (ST)** est le langage de haut niveau de type Pascal
de IEC 61131-3 et l'éditeur par défaut pour les POU PROGRAM,
FUNCTION_BLOCK et FUNCTION dans ForgeIEC. L'éditeur est une composition
basée sur `QWidget` d'un tableau de variables et d'une zone de code,
couplés par un splitter vertical.

```
+----------------------------------------+
| Variable table                         |  <- FVariablesPanel
| (VAR/VAR_INPUT/VAR_OUTPUT/VAR_INST)    |
+========================================+  <- QSplitter (vertical)
| Code area                              |  <- FStCodeEdit
| (Tree-sitter highlighting + folding +  |
|  Ctrl-Space completion)                |
+----------------------------------------+
```

## Disposition de l'éditeur

| Zone | Contenu |
|---|---|
| **Tableau de variables** (haut) | Déclarations avec colonnes Nom, Type, Valeur initiale, Adresse, Commentaire. Les éditions se synchronisent en direct dans le bloc `VAR ... END_VAR` du code. |
| **Zone de code** (bas) | Source ST entre les sections de variables. Pliage de lignes piloté par l'AST tree-sitter, numéros de ligne, surlignage de la ligne du curseur. |
| **Barre de recherche** (Ctrl-F / Ctrl-H) | Affichée au-dessus de la zone de code, avec mode remplacer pour rechercher-remplacer. |

Le splitter mémorise sa position par POU dans l'état de mise en page.

## Coloration syntaxique tree-sitter

Au lieu d'un `QSyntaxHighlighter` à base de regex, ForgeIEC parse la
source ST avec **Tree-sitter** en un AST et colore via des requêtes de
capture :

  - **Mots-clés** (`IF`, `THEN`, `FOR`, `FUNCTION_BLOCK`, ...) : magenta
  - **Types de données** (`BOOL`, `INT`, `REAL`, `TIME`, ...) : cyan
  - **Chaînes + littéraux temps** (`'abc'`, `T#20ms`) : vert
  - **Commentaires** (`(* ... *)`, `// ...`) : gris, italique
  - **PUBLISH / SUBSCRIBE** : mots-clés d'extension Anvil, style dédié

Avantage : la coloration reste correcte sur des constructions complexes
(commentaires imbriqués, littéraux temps, références qualifiées), et le
même AST pilote les plages pliables pour le pliage de code.

## Complétion de code (Ctrl-Espace)

Appuyer sur **Ctrl-Espace** ou taper deux caractères correspondants
ouvre le popup de complétion. Le compléteur connaît :

  - **Mots-clés IEC** (`IF`, `CASE`, `FOR`, `WHILE`, `RETURN`, ...)
  - **Types de données** (`BOOL`, `INT`, `DINT`, `REAL`, `STRING`,
    `TIME`, ...)
  - **Variables locales** du POU courant
  - **Noms de POU** dans le projet (PROGRAM, FUNCTION_BLOCK, FUNCTION)
  - **Blocs de bibliothèque** (`TON`, `R_TRIG`, `JK_FF`, `DEBOUNCE`, ...)
  - **Fonctions standard** (`ABS`, `SQRT`, `LIMIT`, `LEN`, ...)

Les modifications du pool de variables (signal `poolChanged`) se
propagent dans le modèle de complétion avec un debounce de 100 ms — les
nouvelles entrées de pool deviennent disponibles presque
instantanément, sans que chaque frappe ne déclenche un rescan complet.

## Fondamentaux du langage (IEC 61131-3)

### Instructions

| Instruction | Forme |
|---|---|
| **Affectation** | `var := expression;` |
| **IF / ELSIF / ELSE** | `IF cond THEN ... ELSIF cond THEN ... ELSE ... END_IF;` |
| **CASE** | `CASE x OF 1: ... ; 2,3: ... ; ELSE ... END_CASE;` |
| **FOR** | `FOR i := 1 TO 10 BY 1 DO ... END_FOR;` |
| **WHILE** | `WHILE cond DO ... END_WHILE;` |
| **REPEAT** | `REPEAT ... UNTIL cond END_REPEAT;` |
| **EXIT / RETURN** | Quitter la boucle / quitter le POU |

### Expressions

Opérateurs standard avec précédence IEC : `**`, unaire `+/-/NOT`,
`* / MOD`, `+ -`, comparaisons, `AND / &`, `XOR`, `OR`. Parenthèses
comme en Pascal. Les conversions numériques implicites ne sont pas
autorisées — `INT_TO_DINT`, `REAL_TO_INT` etc. doivent être appelées
explicitement.

### Accès bit sur types ANY_BIT

`var.<bit>` extrait ou définit un seul bit, directement sur des
variables `BYTE`/`WORD`/`DWORD`/`LWORD` :

```text
status.0 := TRUE;             (* set bit 0 *)
alarm := flags.7 OR flags.3;  (* read bits *)
```

Le compilateur traduit cela en masquage de bits propre avec
`AND`/`OR`/décalage, sans variables auxiliaires.

### Références qualifiées à 3 niveaux

`<Catégorie>.<Groupe>.<Variable>` accède directement aux entrées du
pool, sans avoir à déclarer explicitement des GVL :

| Préfixe | Source |
|---|---|
| `Anvil.X.Y`   | Entrée de pool avec `anvilGroup="X"` |
| `Bellows.X.Y` | Entrée de pool avec `hmiGroup="X"` |
| `GVL.X.Y`     | Entrée de pool avec `gvlNamespace="X"` |
| `HMI.X.Y`     | Synonyme de `Bellows.X.Y` |

`Anvil.X.Y` et `Bellows.X.Y` peuvent indépendamment pointer vers des
entrées de pool différentes — le compilateur émet des symboles C
distincts dès que les adresses IEC diffèrent.

### Variables localisées (`AT %...`)

Les variables localisées lient une déclaration à une adresse IEC :

```text
button_raw    AT %IX0.0  : BOOL;
motor_speed   AT %QW1    : INT;
flag_persist  AT %MX10.3 : BOOL;
```

L'adresse est la clé primaire dans le pool — voir
[Format de fichier de projet](../file-format/).

## Exemples de code

### Exemple 1 — Appel de TON avec un bloc de bibliothèque

```text
PROGRAM PLC_PRG
VAR
    start_button   AT %IX0.0  : BOOL;
    motor_run      AT %QX0.0  : BOOL;
    fbDelay        : TON;
END_VAR

fbDelay(IN := start_button, PT := T#3s);
motor_run := fbDelay.Q;
END_PROGRAM
```

`fbDelay` est une instance du FB de bibliothèque `TON`. Après 3
secondes de `start_button` maintenu, `motor_run` passe à TRUE.

### Exemple 2 — Lecture Bellows pilotant une sortie

```text
PROGRAM Lampen
VAR
    relay_lamp  AT %QX0.1 : BOOL;
END_VAR

(* HMI panel can write Bellows.Pfirsich.T_1 *)
relay_lamp := Bellows.Pfirsich.T_1 OR Anvil.Sensors.contact_door;
END_PROGRAM
```

`Bellows.Pfirsich.T_1` et `Anvil.Sensors.contact_door` sont des
références à 3 niveaux que le compilateur résout sans déclaration de
GVL — à condition que les deux tags soient gardés dans le pool
d'adresses et que l'export HMI pour le groupe `Pfirsich` soit actif.

## Sujets liés

- [Bibliothèque](../library/) — blocs fonctionnels + fonctions disponibles
- [Instruction List](../il/) — éditeur texte alternatif (basé sur accumulateur)
- [Format de fichier de projet](../file-format/) — comment le code ST
  est stocké dans `.forge`
