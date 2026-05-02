---
title: "Éditeur Function Block Diagram (FBD)"
summary: "Câblage graphique de fonctions, blocs fonctionnels et variables"
---

## Vue d'ensemble

Function Block Diagram (FBD) est l'un des trois langages graphiques
IEC 61131-3 pris en charge par ForgeIEC Studio. Un programme FBD est
constitué d'**appels de fonctions et de blocs fonctionnels** câblés
ensemble — et vers des variables d'entrée et de sortie — via des
**connexions filaires explicites**. Contrairement au Ladder Diagram,
FBD n'a **pas de rails d'alimentation** : chaque connexion est un fil
unique qui transporte une broche de sortie vers une ou plusieurs
broches d'entrée.

## Disposition de l'éditeur

L'éditeur FBD est un widget en trois parties :

```
+---------------------------------------------+
| Toolbar (Select | Wire | Block | Var | ...) |
+--------------------------------+------------+
|                                |            |
|       QGraphicsView            |  Variable  |
|       Grid + Zoom + Pan        |  table     |
|                                |  (right)   |
|                                |            |
+--------------------------------+------------+
```

* **Barre d'outils en haut :** changement d'outil (Select, Wire,
  Place Block, Place In-/Out-Variable, Comment, Zoom).
* **QGraphicsView :** la surface de dessin avec une grille de fond
  (10 px mineur, 50 px majeur) et un panoramique au bouton du milieu.
  La molette de souris zoome autour du curseur.
* **Tableau de variables à droite :** dockable, affiche les variables
  locales du POU. Le glisser-déposer depuis le tableau crée un élément
  variable d'entrée/sortie dans l'éditeur.

## Outils

| Outil | Effet |
|---|---|
| **Select** | Choisir, déplacer, supprimer des éléments. |
| **Wire** | Cliquer sur une broche de sortie, puis sur une broche d'entrée — la connexion est créée. |
| **Place Block** | Déposer une fonction ou un bloc fonctionnel de la bibliothèque. La liste de broches (entrées à gauche, sorties à droite) est tirée de la définition de la bibliothèque. |
| **InVar / OutVar** | Place un élément variable d'entrée ou de sortie. Le nom est saisi via une boîte de dialogue et peut être une variable qualifiée GVL, Anvil ou Bellows. |
| **Comment** | Note en texte libre sans effet sémantique. |

## Blocs et broches

Un **élément bloc** représente un appel à une fonction (`ADD`, `SEL`,
...) ou un bloc fonctionnel (`TON`, `CTU`, ...). L'élément affiche le
nom du type dans l'en-tête, en dessous le nom d'instance (FB
seulement), et sur les côtés les broches :

```
        +---- TON -----+
        | tonA         |
   IN --| IN          Q|-- timeUp
   PT --| PT         ET|-- elapsed
        +--------------+
```

Les entrées sont **toujours à gauche**, les sorties **toujours à
droite**. Les broches inversées sont marquées d'un petit cercle au
niveau de la broche.

## Glisser depuis la bibliothèque

Depuis le panneau Bibliothèque, n'importe quel bloc standard ou
utilisateur peut être **glissé-déposé directement dans l'éditeur**. Au
relâchement, la liste de broches est tirée de la définition de la
bibliothèque ; pour les blocs fonctionnels, l'éditeur crée
automatiquement une entrée d'instance `VAR` dans la section locale de
variables.

## Aller-retour vers ST

À la compilation, le compilateur ForgeIEC traduit le corps FBD en
Structured Text. Un tri topologique des blocs par flux de données
détermine l'ordre d'exécution. Par conséquent : **tout corps FBD est
sémantiquement équivalent à un corps ST**, et le choix du langage est
purement une question de lisibilité.

## Exemple — temporisateur à retard à l'enclenchement avec `TON`

Un `TON` (temporisateur à retard à l'enclenchement) retarde un signal
d'entrée d'une durée configurable. En FBD vous

  * câbleriez une **variable d'entrée** `start` dans la broche `IN` de
    l'instance `TON`,
  * câbleriez une **variable d'entrée** avec la valeur `T#5s` dans la
    broche `PT`,
  * connecteriez la sortie `Q` à une **variable de sortie** `lampe`.

En ST cela ressemble à ceci :

```text
PROGRAM PLC_PRG
VAR
    start  AT %IX0.0 : BOOL;
    lampe  AT %QX0.0 : BOOL;
    tmr    : TON;
END_VAR

tmr(IN := start, PT := T#5s);
lampe := tmr.Q;
END_PROGRAM
```

C'est exactement la forme que le compilateur génère depuis le diagramme
FBD — l'instance variable `tmr` est la boîte `Block`, et les deux fils
sont les deux affectations `:=`.

## Sujets liés

* [Bibliothèque](../library/) — quels blocs le sélecteur de bloc
  propose.
* [Panneau Variables](../variables/) — déclaration de variable et pool
  d'adresses.
* [Ladder Diagram](../ld/) — langage sœur orienté chemin de courant.
