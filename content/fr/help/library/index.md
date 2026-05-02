---
title: "Bibliothèque (blocs fonctionnels + fonctions)"
summary: "Bibliothèque standard IEC 61131-3 + extensions ForgeIEC + blocs définis par l'utilisateur"
---

## Vue d'ensemble

La bibliothèque ForgeIEC est la collection centrale de tous les blocs
réutilisables qu'un programme applicatif peut appeler depuis un projet
`.forge` — couvrant à la fois les blocs fonctionnels et les fonctions
normalisés IEC 61131-3, ainsi que les extensions spécifiques au projet
ou à ForgeIEC.

La bibliothèque est affichée dans le **panneau Bibliothèque** (dock par
défaut : barre latérale droite). Appuyez sur **F1** lorsque le panneau
Bibliothèque a le focus pour ouvrir cette page.

```
Library
+-- Standard Function Blocks    (Bistable, Edge, Counter, Timer, ...)
+-- Standard Functions          (Arithmetic, Comparison, Bitwise, ...)
+-- User Library                (project-specific blocks)
```

La bibliothèque livre actuellement **près de 100 blocs** et **un peu
plus de 30 fonctions**. Chaque entrée porte :

  - **Nom** (par ex. `TON`, `JK_FF`)
  - **Liste de broches** (entrées + sorties avec type et position)
  - **Type** (`FUNCTION_BLOCK` avec état, ou `FUNCTION` sans état)
  - **Description** + **texte d'aide** avec notes d'utilisation
  - **Exemple de code** (visible dans le panneau d'aide de la bibliothèque)

## Arborescence des catégories

### Blocs fonctionnels standard

| Groupe | Blocs |
|---|---|
| **Bistable** | `SR`, `RS` — set/reset avec priorité |
| **Détection de fronts** | `R_TRIG`, `F_TRIG` — front montant/descendant |
| **Compteurs** | `CTU`, `CTD`, `CTUD` — comptage haut / bas / les deux |
| **Temporisateurs** | `TON`, `TOF`, `TP` — retard à l'enclenchement / au déclenchement / impulsion |
| **Mouvement** | profils, rampes, trajectoires (en préparation) |
| **Génération de signaux** | FB générateurs pour signaux de test et de validation |
| **Manipulateurs de fonctions** | hold, latch, historique |
| **Régulation en boucle fermée** | PID, hystérésis, deux points |
| **Application** *(ForgeIEC)* | `JK_FF`, `DEBOUNCE` — blocs proches de l'application qui se sont avérés universellement utiles en pratique |

### Fonctions standard

| Groupe | Contenu |
|---|---|
| **Arithmétique** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` (sur tout type ANY_NUM) |
| **Comparaison** | `EQ`, `NE`, `LT`, `LE`, `GT`, `GE` |
| **Bit à bit** | `AND`, `OR`, `XOR`, `NOT` (sur ANY_BIT — voir `help/st`) |
| **Décalage de bits** | `SHL`, `SHR`, `ROL`, `ROR` |
| **Sélection** | `SEL`, `MAX`, `MIN`, `LIMIT`, `MUX` |
| **Numérique** | `ABS`, `SQRT`, `LN`, `LOG`, `EXP`, `SIN`, `COS`, `TAN`, `ASIN`, `ACOS`, `ATAN` |
| **Chaîne** | `LEN`, `LEFT`, `RIGHT`, `MID`, `CONCAT`, `INSERT`, `DELETE`, `REPLACE`, `FIND` |
| **Conversion de type** | `BOOL_TO_INT`, `REAL_TO_DINT`, `STRING_TO_INT`, ... |

### Bibliothèque utilisateur

Blocs fonctionnels et fonctions définis par le projet — tout ce qui
est déclaré comme `FUNCTION_BLOCK` ou `FUNCTION` arrive automatiquement
dans cette catégorie et peut être appelé depuis n'importe où dans le
projet, exactement comme les blocs standard.

## Panneau Bibliothèque — utilisation

| Action | Effet |
|---|---|
| **Recherche** (loupe en haut) | Filtre l'arborescence par nom de bloc — taper `to` trouve `TON`. |
| **Double-clic** sur un bloc | Ouvre l'aide du bloc dans un volet de détail : descriptions des broches + exemple de code. |
| **Glisser** sur l'éditeur ST | Insère l'appel du bloc à la position du curseur, y compris la déclaration d'instance dans la section locale `VAR_INST`. |
| **Clic droit > « Insert Call... »** | Identique au glisser, via le menu contextuel. |
| **F1** sur un bloc | Ouvre cette page. |

## Exemple 1 — Anti-rebond de bouton avec `DEBOUNCE`

`DEBOUNCE` filtre les courtes impulsions de bruit issues d'un contact
mécanique de bouton. `Q` ne change qu'une fois que `IN` est resté stable
pendant la durée complète `T_Debounce` — sur les fronts montants comme
descendants.

### Disposition des broches

| Broche | Direction | Type | Signification |
|---|---|---|---|
| `IN`         | INPUT  | `BOOL` | Entrée brute (typiquement `%IX`, mécaniquement instable) |
| `tDebounce`  | INPUT  | `TIME` | Temps minimum de stabilité (typiquement `T#10ms`...`T#50ms`) |
| `Q`          | OUTPUT | `BOOL` | Sortie débruitée |

### Exemple de code

Corps de PROGRAM qui débruite un bouton-poussoir sur `%IX0.0` et
transmet le signal débruité comme un front à coup unique vers un
contacteur auto-maintenu :

```text
PROGRAM PLC_PRG
VAR
    button_raw      AT %IX0.0 : BOOL;       (* bouncing contact *)
    button_clean    : BOOL;                  (* after DEBOUNCE *)
    button_pressed  : BOOL;                  (* single-shot per press *)
    relay_lamp      AT %QX0.0 : BOOL;        (* lamp as self-hold *)
    fbDeb           : DEBOUNCE;              (* instance *)
    fbTrig          : R_TRIG;                (* edge detector *)
END_VAR

fbDeb(IN := button_raw, tDebounce := T#20ms);
button_clean := fbDeb.Q;

fbTrig(CLK := button_clean);
button_pressed := fbTrig.Q;

(* Self-hold: toggle on every rising edge *)
IF button_pressed THEN
    relay_lamp := NOT relay_lamp;
END_IF;
END_PROGRAM
```

`DEBOUNCE` est construit en interne à partir de deux blocs `TON` (sens
haut et sens bas) — l'un fait passer `Q` à TRUE seulement après
`T_Debounce` de `IN` actif, l'autre le fait passer à FALSE seulement
après `T_Debounce` de `IN` inactif. Cela rend le filtre symétrique :
ni le rebond de contact à l'appui, ni au relâchement, ne produisent de
parasite.

> **Utilisation typique :** boutons-poussoirs mécaniques, fins de
> course, capteurs à contact. Pour un « coup unique par appui » — comme
> ci-dessus — chaînez un `R_TRIG` après `Q`.

## Exemple 2 — Auto-maintien avec mode forcé (`JK_FF`)

`JK_FF` est une bascule à bascule (toggle) avec anti-rebond intégré.
À chaque front montant stable de `xButton`, elle bascule `Q` entre TRUE
et FALSE — de sorte qu'un simple bouton-poussoir devient un commutateur
« on/off » **sans** que le programme applicatif n'ait à câbler à la
main DEBOUNCE + R_TRIG + logique de bascule.

### Disposition des broches

| Broche | Direction | Type | Signification |
|---|---|---|---|
| `xButton`    | INPUT  | `BOOL` | Contact brut du bouton (instable) |
| `tDebounce`  | INPUT  | `TIME` | Durée d'anti-rebond (typiquement `T#20ms`) |
| `J`          | INPUT  | `BOOL` | « Set » (force `Q` à TRUE tant qu'actif) |
| `K`          | INPUT  | `BOOL` | « Reset » (force `Q` à FALSE tant qu'actif) |
| `Q`          | OUTPUT | `BOOL` | État courant |
| `Q_N`        | OUTPUT | `BOOL` | État inversé (`NOT Q`) |
| `xStable`    | OUTPUT | `BOOL` | TRUE tant que `xButton` est resté stable pendant `tDebounce` |

### Exemple de code

Une commande de lampe avec trois boutons : `T1` bascule la lampe,
`T_Mains` la force à allumée (par ex. « éclairage général partout »),
`T_Off` force tout à éteint :

```text
PROGRAM PLC_PRG
VAR
    bButtons     AT %IX0.0 : ARRAY [0..3] OF BOOL;
    relay_lamp   AT %QX0.0 : BOOL;
    fbToggle     : JK_FF;
END_VAR

fbToggle(
    xButton    := bButtons[0],   (* toggle button T1 *)
    tDebounce  := T#20ms,
    J          := bButtons[1],   (* main light ON while held *)
    K          := bButtons[2]    (* main light OFF while held *)
);

relay_lamp := fbToggle.Q;
END_PROGRAM
```

Table de vérité des entrées `J`/`K` :

| `J` | `K` | Comportement |
|---|---|---|
| FALSE | FALSE | Bascule à chaque appui débruité |
| TRUE  | FALSE | Q := TRUE (set, écrase la bascule) |
| FALSE | TRUE  | Q := FALSE (reset, écrase la bascule) |
| TRUE  | TRUE  | indéfini — à éviter |

`xStable` permet d'implémenter une logique « le bouton est actuellement
maintenu » (par ex. une LED visualisant l'appui sans devoir attendre
que l'effet de bascule se manifeste).

## Synchronisation de la bibliothèque entre éditeur et automate

La bibliothèque standard vit en deux endroits :

  - **Côté éditeur :** `editor/resources/library/standard_library.json`
    (compilé dans le `.exe` via le système de ressources Qt).
  - **Côté automate :** sous-module anvild, même fichier JSON, inclus
    par l'étape `make` sur les sources C téléversées.

La **synchronisation de la bibliothèque** compare le SHA-256 des deux
versions à la connexion. En cas de divergence, un indice apparaît dans
le panneau de sortie ; la réaction est configurable :

  - `Preferences > Library > Auto-Push` désactivé (par défaut) : push
    manuel via `Tools > Sync Library`. Protège un runtime de production
    contre un écrasement accidentel par un éditeur plus ancien.
  - `Preferences > Library > Auto-Push` activé : la divergence
    déclenche un push automatique. Utile dans des configurations de
    développement avec un seul programmeur.

## Extensions ForgeIEC

Les blocs suivants ne sont pas normalisés dans IEC 61131-3, mais sont
livrés dans la bibliothèque standard car leur utilisation s'est avérée
universellement utile en pratique :

| Bloc | Rôle |
|---|---|
| `JK_FF` | Bascule (toggle) avec anti-rebond intégré (voir exemple 2). |
| `DEBOUNCE` | Anti-rebond symétrique de bouton (voir exemple 1). |

Ces blocs vivent sous *Standard Function Blocks / Application* et sont
marqués `isStandard: true` dans la source JSON, ce qui les désigne comme
« non supprimables » (c.-à-d. qu'ils ne peuvent pas être supprimés
accidentellement via le panneau Bibliothèque).

## Ajouter vos propres blocs à la bibliothèque utilisateur

Chaque déclaration `FUNCTION_BLOCK` et `FUNCTION` du projet courant
arrive automatiquement sous **User Library**. Délais de visibilité :

  1. **Dans le panneau Bibliothèque :** immédiatement après la
     déclaration et la sauvegarde du POU.
  2. **Dans la complétion de code (Ctrl-Espace) :** immédiatement.
  3. **Dans l'éditeur FBD/LD comme bloc :** immédiatement.
  4. **Sur l'automate** après `Compile + Upload`.

Pour réutiliser un bloc entre projets, exportez le POU via
`File > Export POU...` en tant que fichier `.forge-pou` et importez-le
dans le projet cible — une « bibliothèque d'espace de travail »
inter-projets est dans le backlog.

## Sujets liés

- [Syntaxe Structured Text](../st/) — à quoi ressemble un appel de bloc en ST.
- [Éditeur Function Block Diagram](../fbd/) — comment un bloc est câblé
  graphiquement.
- [Panneau Variables](../variables/) — comment le pool d'adresses voit
  l'instance.
