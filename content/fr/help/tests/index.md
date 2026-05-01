---
title: "Couverture des tests"
summary: "Assurance qualite automatisee : 117 tests verifient l'ensemble du vocabulaire IEC 61131-3, tous les blocs standard et le systeme multi-tache"
---

ForgeIEC est protege par une suite de tests automatises complete.
Chaque commit est verifie avant le merge par **117 tests unitaires** qui
couvrent l'ensemble du vocabulaire IEC 61131-3 Structured Text, tous les
blocs fonctionnels standard et le systeme de multi-tache.

## Apercu des suites de tests

| Suite | Tests | Verifie |
|-------|------:|---------|
| **FStCompilerTest** | 101 | Vocabulaire ST complet |
| **FStLibraryTest** | 8 | Les 132 blocs standard (FBs + FCs) |
| **FCodeGeneratorThreadingTest** | 8 | Ordonnancement multi-tache + synchronisation lock-free |
| **Total** | **117** | **0 erreur** |

---

## 1. Vocabulaire ST (FStCompilerTest)

101 tests verifient chaque construction du langage IEC 61131-3 Structured Text
prise en charge. Chaque test compile un fragment ST via le
FStCompiler et verifie le code C++ genere.

### 1.1 Affectations

| Test | Code ST | Verifie |
|------|---------|---------|
| `assignSimple` | `a := 42;` | Affectation simple |
| `assignExpression` | `a := b + 1;` | Affectation avec expression |
| `assignExternal` | `ExtVar := 10;` | Acces VAR_EXTERNAL |
| `assignGvlQualified` | `GVL.ExtVar := 5;` | Chemin GVL qualifie |

### 1.2 Operateurs arithmetiques

| Test | Code ST | Operateur C |
|------|---------|-------------|
| `arithmeticAdd` | `a := b + 1;` | `+` |
| `arithmeticSub` | `a := b - 1;` | `-` |
| `arithmeticMul` | `a := b * 2;` | `*` |
| `arithmeticDiv` | `a := b / 2;` | `/` |
| `arithmeticMod` | `a := b MOD 3;` | `%` |
| `arithmeticPower` | `c := x ** 2.0;` | `EXPT()` |
| `arithmeticNegate` | `a := -b;` | `-(...)` |
| `arithmeticParentheses` | `a := (b + 1) * 2;` | Parenthesage |

### 1.3 Operateurs de comparaison

| Test | Code ST | Operateur C |
|------|---------|-------------|
| `compareEqual` | `flag := a = b;` | `==` |
| `compareNotEqual` | `flag := a <> b;` | `!=` |
| `compareLess` | `flag := a < b;` | `<` |
| `compareGreater` | `flag := a > b;` | `>` |
| `compareLessEqual` | `flag := a <= b;` | `<=` |
| `compareGreaterEqual` | `flag := a >= b;` | `>=` |

### 1.4 Operateurs booleens

| Test | Code ST | Operateur C |
|------|---------|-------------|
| `boolAnd` | `flag := flag AND flag;` | `&&` |
| `boolOr` | `flag := flag OR flag;` | `\|\|` |
| `boolXor` | `flag := flag XOR flag;` | `^` |
| `boolNot` | `flag := NOT flag;` | `!` |

### 1.5 Litteraux

| Test | Code ST | Verifie |
|------|---------|---------|
| `literalInteger` | `a := 12345;` | Entier |
| `literalReal` | `c := 3.14;` | Virgule flottante |
| `literalBoolTrue` | `flag := TRUE;` | Valeur booleenne |
| `literalBoolFalse` | `flag := FALSE;` | Valeur booleenne |
| `literalString` | `text := 'hello';` | Chaine de caracteres |
| `literalTime` | `counter := T#500ms;` | Constante temporelle |

### 1.6 Structures de controle

**IF / ELSIF / ELSE / END_IF**

| Test | Verifie |
|------|---------|
| `ifSimple` | Condition simple |
| `ifElse` | Branchement If-Else |
| `ifElsif` | Branchement multiple avec ELSIF |
| `ifNested` | Blocs IF imbriques |

**FOR / WHILE / REPEAT**

| Test | Verifie |
|------|---------|
| `forSimple` | FOR idx := 0 TO 10 DO |
| `forWithBy` | FOR avec pas BY |
| `whileLoop` | Boucle WHILE |
| `repeatUntil` | Boucle REPEAT/UNTIL |

**CASE**

| Test | Verifie |
|------|---------|
| `caseStatement` | CASE/OF avec plusieurs labels + switch/case/break |

**RETURN / EXIT**

| Test | Verifie |
|------|---------|
| `returnStatement` | RETURN → goto __end |
| `exitStatement` | EXIT dans un FOR → break |

### 1.7 Blocs fonctionnels (appels FB)

| Test | Verifie |
|------|---------|
| `fbCallWithInputs` | `MyTon(IN := flag, PT := T#500ms);` |
| `fbCallWithOutputAssign` | `MyTimer(IN := flag, Q => flag);` — affectation OUT => |

### 1.8 Acces aux tableaux

| Test | Verifie |
|------|---------|
| `arrayReadSubscript` | `a := arr[3];` |
| `arrayWriteSubscript` | `arr[5] := 42;` |
| `arrayComputedIndex` | `a := arr[idx + 1];` |
| `arrayInForLoop` | Acces tableau dans une boucle FOR |

### 1.9 Conversions de type

Le compilateur reconnait le motif `XXX_TO_YYY` et genere
des casts C (`(TYPE)value`), conformement a la norme IEC.

| Test | Code ST | Genere |
|------|---------|--------|
| `typeConvIntToReal` | `INT_TO_REAL(a)` | `(REAL)a` |
| `convRealToInt` | `REAL_TO_INT(c)` | `(INT)c` |
| `convBoolToInt` | `BOOL_TO_INT(flag)` | `(INT)flag` |
| `convIntToBool` | `INT_TO_BOOL(a)` | `(BOOL)a` |
| `convDintToReal` | `DINT_TO_REAL(counter)` | `(REAL)counter` |
| `convIntToDint` | `INT_TO_DINT(a)` | `(DINT)a` |

### 1.10 Acces aux membres de structure

| Test | Verifie |
|------|---------|
| `structMemberAccess` | `pos.x := 42;` → `data__->pos.value.x` |

### 1.11 Variables inter-taches (multi-tache)

| Test | Verifie |
|------|---------|
| `crossPrimitiveGet` | `__GET_EXTERNAL_ATOMIC` pour lecture lock-free |
| `crossPrimitiveSet` | `__SET_EXTERNAL_ATOMIC` pour ecriture lock-free |
| `crossStructuredGet` | `__snap_` acces snapshot thread-local |
| `crossStructuredMemberAccess` | `__snap_Struct.field` acces |

### 1.12 Blocs fonctionnels standard

Chaque FB standard IEC est instancie et appele :

| Test | Type FB | Verifie |
|------|---------|---------|
| `fbTon` | TON | Temporisation a l'enclenchement |
| `fbTof` | TOF | Temporisation au declenchement |
| `fbTp` | TP | Timer d'impulsion |
| `fbCtu` | CTU | Compteur croissant |
| `fbCtd` | CTD | Compteur decroissant |
| `fbRtrig` | R_TRIG | Front montant |
| `fbFtrig` | F_TRIG | Front descendant |
| `fbRs` | RS | Reset-dominant |
| `fbSr` | SR | Set-dominant |

### 1.13 Fonctions standard

| Categorie | Tests | Fonctions |
|-----------|------:|-----------|
| Mathematiques | 12 | ABS, SQRT, SIN, COS, TAN, ASIN, ACOS, ATAN, EXP, LN, LOG, TRUNC |
| Selection | 4 | SEL, LIMIT, MIN, MAX |
| Chaines | 6 | LEN, LEFT, RIGHT, MID, CONCAT, FIND |
| Decalage binaire | 4 | SHL, SHR, ROL, ROR |
| Conversion de type | 6 | INT_TO_REAL, REAL_TO_INT, BOOL_TO_INT, ... |

### 1.14 Cas limites

| Test | Verifie |
|------|---------|
| `complexNestedExpression` | Expressions imbriquees |
| `multipleStatementsOnSeparateLines` | Programmes multi-lignes |
| `emptyBody` | Corps POU vide |
| `commentOnlyBody` | Uniquement des commentaires |
| `caseInsensitiveKeywords` | IF/if/If |
| `caseInsensitiveVariables` | Casse des variables |

---

## 2. Bibliotheque standard (FStLibraryTest)

8 tests pilotes par les donnees verifient **les 132 blocs** de la
bibliotheque standard (`standard_library.sql`) automatiquement.

### 2.1 Blocs fonctionnels (13 FBs)

| Test | Verifie |
|------|---------|
| `fbSingleInstance` | Chaque FB instanciable et appelable individuellement |
| `fbDoubleInstance` | Deux instances du meme type FB simultanement |
| `fbOutputRead` | Toutes les sorties lisibles apres l'appel |

**FBs couverts :** SR, RS, R_TRIG, F_TRIG, CTU, CTD, CTUD, TON, TOF, TP,
RTC, SEMA, RampGen

### 2.2 Fonctions (119 FCs)

| Test | Verifie |
|------|---------|
| `fcCall` | Chaque FC appelable avec les parametres corrects (104 testees) |
| `fcInExpression` | Valeur de retour FC utilisable dans les expressions |

**Categories couvertes :**

- **Arithmetique :** ADD, SUB, MUL, DIV, MOD, EXPT, ABS
- **Comparaison :** EQ, NE, LT, GT, LE, GE
- **Trigonometrie :** SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2
- **Logarithme :** EXP, LN, LOG, SQRT
- **Selection :** SEL, MUX, LIMIT, MIN, MAX, MOVE, CLAMP
- **Chaines :** LEN, LEFT, RIGHT, MID, CONCAT, INSERT, DELETE, REPLACE, FIND
- **Decalage binaire :** SHL, SHR, ROL, ROR
- **Conversion de type :** 60+ fonctions de conversion (BOOL_TO_INT, INT_TO_REAL, ...)
- **Extensions ForgeIEC :** LERP, MAP_RANGE, HYPOT, DEG, RAD, IK_2Link,
  CABS, CADD, CMUL, CSUB, CARG, CCONJ, CPOLAR, CRECT

---

## 3. Multi-tache (FCodeGeneratorThreadingTest)

8 tests verifient le systeme complet d'ordonnancement multi-tache conformement
a la specification de conception (MT-spec, docs/design/multi-task-scheduler.md).

| Test | Verifie |
|------|---------|
| `singleProgramDefaultTask` | Un PROGRAM sans tache explicite → synthese DefaultTask, pas de threading |
| `twoProgramsTwoTasks` | Deux taches → RESOURCE0_start__, Legacy-Shim config_run__, les deux threads de tache |
| `crossPrimitiveAtomicEmission` | Variable INT partagee → stockage Location `std::atomic<>`, `__GET_EXTERNAL_ATOMIC` dans le corps |
| `crossStructuredDoubleBuffer` | STRUCT partage → `__DBUF_[2]` + `thread_local __snap_` + copie Double-Buffer entree/sortie |
| `localVarNoSync` | Variable dans une seule tache → `__SET_EXTERNAL` normal, pas d'Atomic |
| `conflictTwoWriters` | Deux taches ecrivent la meme variable → avertissement de compilation |
| `singleProgramDefaultTask` | Retrocompatibilite : les projets existants fonctionnent sans modification |

### Architecture multi-tache

```
Primary Task (Task 0)          Secondary Tasks (1..N)
    |                               |
    | config_run__()                | RESOURCE0_task_thread__()
    |   ├─ sync_in                  |   ├─ dbuf_rd (copy-in)
    |   ├─ TASK0_body__()           |   ├─ TASKn_body__()
    |   └─ sync_out                 |   └─ dbuf_wr (copy-out)
    |                               |
    | [sous bufferLock]             | [lock-free]
```

**Mecanismes de synchronisation :**
- **CrossPrimitive** (BOOL, INT, REAL, ...) : `std::atomic<T>` sur la variable Location, `__GET_EXTERNAL_ATOMIC` / `__SET_EXTERNAL_ATOMIC` dans le code du corps
- **CrossStructured** (STRUCT, ARRAY, STRING) : Double-Buffer `__DBUF_[2]` avec index d'ecriture atomique, snapshots `thread_local` `__snap_` pour la coherence du Set

---

## Assurance qualite

### Verification automatisee

Les tests s'executent a chaque build avec `-DBUILD_TESTS=ON`.
L'integration dans le pipeline CI (Forgejo Actions) est preparee.

### Tests pilotes par les donnees

Les tests de bibliotheque (`FStLibraryTest`) lisent les definitions de blocs
directement depuis `standard_library.sql`. Lorsque de nouveaux blocs sont
ajoutes, ils sont automatiquement testes — aucune creation manuelle de cas
de test necessaire.

### Completude

La suite de tests couvre l'ensemble du vocabulaire IEC 61131-3 Structured Text
tel que pris en charge par ForgeIEC :

- Tous les operateurs (arithmetiques, comparaison, booleens, decalage binaire)
- Toutes les structures de controle (IF, FOR, WHILE, REPEAT, CASE)
- Tous les types de litteraux (Integer, Real, Bool, String, Time)
- Tous les FBs et FCs standard (132 blocs)
- Acces aux tableaux et structures
- Variables qualifiees GVL
- Synchronisation inter-taches (Atomics + Double-Buffer)
- Conversions de type (generation de casts C)
