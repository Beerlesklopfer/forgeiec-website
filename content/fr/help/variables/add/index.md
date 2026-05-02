---
title: "Ajouter une variable"
summary: "Le FAddVariableDialog — chaque champ dans une seule modale, patterns de plage pour la création groupée, wrapper de tableau"
---

## Vue d'ensemble

Le **FAddVariableDialog** est la fenêtre modale utilisée pour ajouter
une nouvelle variable à un POU ou au pool. Il rassemble chaque champ en
une seule étape et affiche un **aperçu en direct** de la déclaration ST
IEC résultante juste sous le formulaire — ce que vous tapez s'affiche
immédiatement sous forme de fragment `VAR ... END_VAR` terminé.

La boîte de dialogue fonctionne dans deux modes :

  - **Mode ajout** : champs vides, OK crée une nouvelle variable.
    Atteint via l'icône plus dans le panneau Variables ou Ctrl+N dans
    l'éditeur de POU.
  - **Mode édition** : double-clic sur une variable existante dans le
    panneau — même boîte de dialogue, chaque champ pré-rempli.

## Champs

| Champ | Requis | Signification |
|---|---|---|
| **Name** | oui | Nom visible par le programmeur. Validé contre les règles d'identifiant IEC (lettre + lettres/chiffres/`_`). Utilisé pour la création groupée avec un pattern de plage (voir ci-dessous). |
| **Type** | oui | Combo avec types élémentaires IEC, FB standard, FB du projet, types de données utilisateur. La création de tableau est gérée par la case à cocher du wrapper. |
| **Direction** | dépend du POU | Var-class — voir ci-dessous. |
| **Initial** | non | Valeur initiale (`FALSE`, `0`, `T#100ms`, `'OFF'`). |
| **Address** | non | Seulement pour les POU VarList. Vide = `pool->nextFreeAddress` alloue automatiquement à la création. |
| **Retain** | non | Case à cocher — RETAIN, la valeur survit à une coupure de courant. |
| **Constant** | non | Case à cocher — `VAR CONSTANT`, non inscriptible à l'exécution. |
| **Array wrapper** | non | Encapsule le type sélectionné dans `ARRAY [..] OF`. |
| **Documentation** | non | Commentaire en texte libre, stocké comme `<documentation>` dans PLCopen XML. |

## Pattern de plage pour la création groupée

Au lieu de taper `LED_0`, `LED_1`, ... `LED_7` individuellement, vous
pouvez spécifier un **pattern de plage** dans le champ nom :

| Saisie | Effet |
|---|---|
| `LED_0..7` | Crée huit variables `LED_0` à `LED_7`. |
| `LED_0-7` | Synonyme, même effet. |
| `Sensor_1..3` | Crée trois variables `Sensor_1` à `Sensor_3`. |

À chaque création groupée, l'adresse est incrémentée si elle est
définie : `%QX0.0` → `%QX0.0`, `%QX0.1`, ..., `%QX0.7`.

## Case à cocher Array wrapper

Si vous voulez **une** variable déclarée comme tableau, cochez la case
array. Deux compteurs apparaissent pour la plage d'index et le type est
encapsulé à l'exécution comme `ARRAY [..] OF <type>`.

| Combo Type | Case Array | Plage d'index | Déclaration résultante |
|---|---|---|---|
| `INT` | off | — | `: INT;` |
| `INT` | on | `0..7` | `: ARRAY [0..7] OF INT;` |
| `BOOL` | on | `1..16` | `: ARRAY [1..16] OF BOOL;` |
| `T_Motor` (struct utilisateur) | on | `0..3` | `: ARRAY [0..3] OF T_Motor;` |

Le wrapper vit délibérément sur une case à cocher plutôt que dans le
combo de type — cela garde le combo épuré et vous laisse construire
des tableaux de n'importe quoi sans fouiller le combo.

## Combo Type

Le combo agrège quatre sources en une liste unique :

  1. **Types élémentaires IEC** : `BOOL`, `BYTE`, `WORD`, `DWORD`, `LWORD`,
     `INT`, `DINT`, `LINT`, `UINT`, `UDINT`, `ULINT`, `REAL`, `LREAL`,
     `TIME`, `DATE`, `TIME_OF_DAY`, `DATE_AND_TIME`, `STRING`, `WSTRING`.
  2. **FB standard** de la bibliothèque : `TON`, `TOF`, `TP`, `R_TRIG`,
     `F_TRIG`, `CTU`, `CTD`, `CTUD`, `SR`, `RS`, ...
  3. **Blocs fonctionnels du projet** — chaque FB déclaré dans le projet
     courant (bibliothèque utilisateur).
  4. **Types de données utilisateur** depuis `<dataTypes>` : STRUCT,
     enums, alias.

Les modèles ARRAY n'apparaissent **pas** dans le combo — ils passent par
la case à cocher du wrapper.

## Direction (var-class) par type de POU

Les valeurs de direction proposées dépendent du type de POU :

| Type de POU | Direction disponible |
|---|---|
| `PROGRAM` / `FUNCTION_BLOCK` / `FUNCTION` | `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` |
| `GlobalVarList` (GVL) | `VAR_GLOBAL` fixe — combo masqué. |
| `AnvilVarList` | `VAR_GLOBAL` fixe (auto-généré) — combo masqué. |
| Globales de pool (sans conteneur POU) | Pas de direction — l'adresse `%I`/`%Q` la définit implicitement. |

## Mode édition

Un double-clic sur une variable existante dans le panneau Variables
ouvre la même boîte de dialogue. Chaque champ est pré-rempli ; à OK,
les modifications sont routées via `pou->renameVariable` /
`pool->rebind` (pour que les indices `byAddress` restent synchronisés).
La boîte de dialogue détecte le mode édition par `existing != nullptr`.

## Exemple — 8 LED en un seul bloc

Huit LED de sortie comme variables de pool, en une seule étape :

  - **Name** : `LED_0..7`
  - **Type** : `BOOL`
  - **Direction** : masquée (globale de pool)
  - **Address** : `%QX0.0` (auto-incrément)
  - **Initial** : `FALSE`

OK crée huit entrées de pool :

```text
LED_0  AT %QX0.0 : BOOL := FALSE;
LED_1  AT %QX0.1 : BOOL := FALSE;
LED_2  AT %QX0.2 : BOOL := FALSE;
LED_3  AT %QX0.3 : BOOL := FALSE;
LED_4  AT %QX0.4 : BOOL := FALSE;
LED_5  AT %QX0.5 : BOOL := FALSE;
LED_6  AT %QX0.6 : BOOL := FALSE;
LED_7  AT %QX0.7 : BOOL := FALSE;
```

Les huit variables peuvent ensuite être sélectionnées dans le panneau
Variables et assignées à un groupe HMI via une opération groupée — par
ex. `Set HMI Group... -> Frontpanel`.

## Sujets liés

  - [Gestion des variables](../) — le panneau Variables avec colonnes,
    filtres et opérations groupées.
  - [Format de fichier de projet](../../file-format/) — comment le pool
    est persisté en bloc `<addData>` dans PLCopen XML.
