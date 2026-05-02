---
title: "Gestion des variables"
summary: "Le panneau Variables comme vue centrale sur le FAddressPool — colonnes, filtres, opérations groupées, interrupteurs de sécurité"
---

## Vue d'ensemble

Le **panneau Variables** est la vue centrale sur le **FAddressPool** —
la source unique de vérité pour chaque variable d'un projet ForgeIEC.
Chaque variable existe exactement une fois dans le pool, indexée par
son adresse IEC (`%IX0.0`, `%QW3`, ...). Les conteneurs comme GVL,
AnvilVarList, HmiVarList ou les interfaces de POU ne sont que des
**vues** sur ce pool — aucune variable ne vit dans deux stores en
parallèle.

```
FAddressPool  (single source of truth)
   |
   +-- FAddressPoolModel  (Qt table)
         |
         +-- FVariablesPanel  (filters + bulk ops + clipboard)
               |
               +-- Tree filter sets FilterMode + tag
```

Le panneau s'amarre en bas de la fenêtre principale et reflète chaque
modification immédiatement dans toutes les autres vues (éditeur de POU,
compilateur ST, sauvegarde PLCopen-XML).

## Colonnes

Le tableau a **15 colonnes** ; chacune peut être basculée individuellement
via le menu contextuel de l'en-tête — chaque instance d'éditeur de POU
mémorise sa visibilité de colonnes indépendamment.

| Colonne | Contenu |
|---|---|
| **Name** | Nom visible par le programmeur. Les entrées de pool qualifiées apparaissent avec leur chemin complet : `Anvil.Pfirsich.T_1`, `Bellows.Stachelbeere.T_Off`, `GVL.Motor.K1_Mains`. |
| **Type** | Type élémentaire IEC ou type défini par l'utilisateur. Les tableaux apparaissent comme `ARRAY [0..7] OF BOOL`. |
| **Direction** | Var-class IEC : `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` pour les locales de POU ; `in`/`out` pour les globales du pool (dérivé de `%I` vs. `%Q`). |
| **Address** | Adresse IEC — la clé primaire. `%IX0.0` pour une entrée bit, `%QW1` pour une sortie mot, `%MX10.3` pour un bit de marqueur. |
| **Initial** | Valeur initiale (`FALSE`, `0`, `T#100ms`, `'OFF'`). Chargée dans la variable au premier cycle. |
| **Bus Device** | UUID du périphérique de bus (esclave Modbus etc.) auquel cette variable est liée — éditable comme combo. |
| **Bus Addr** | Décalage de registre Modbus relatif à l'esclave (`0`, `1`, ...). |
| **R** (Retain) | Case à cocher — la valeur survit-elle à une coupure de courant ? |
| **C** (Constant) | Case à cocher — constante IEC (`VAR CONSTANT`), valeur non inscriptible à l'exécution. |
| **RO** (ReadOnly) | Case à cocher — lecture seule depuis le code programme. |
| **Sync** | Classe de synchronisation multi-tâche (`L`/`A`/`D`), produite par la dernière exécution du compilateur ST. |
| **Used by** | Quelles tâches lisent/écrivent cette variable, par ex. `PROG_Fast (R/W), PROG_Slow (R)`. |
| **Monitor** / **HMI** / **Force** | Interrupteurs de sécurité par variable. **Cluster A** dans le backlog — opt-ins explicites, distincts du tag `hmiGroup`. Le compilateur ST vérifie avant la génération de code que les accès Force/HMI ne ciblent que des variables qui portent le drapeau. |
| **Live** | Valeur d'exécution en mode en ligne (alimentée par le store de valeurs en direct anvild ; cachée quand déconnecté). |
| **Scope** | Case de visibilité oscilloscope — envoie la variable au panneau d'oscilloscope. |
| **Documentation** | Commentaire en texte libre. |

## Modes de filtre

Le panneau ne montre pas tout le pool d'un coup — l'**arborescence du
projet à gauche** choisit quelle tranche est visible. Cliquer sur un
nœud d'arborescence fait définir par la fenêtre principale le
`FilterMode` plus le tag :

| FilterMode | Affiche |
|---|---|
| `FilterAll` | Tout le pool — pas de restriction de tag. |
| `FilterByGvl` | Variables avec `gvlNamespace == tag` (par ex. seulement `GVL.Motor`). |
| `FilterByAnvil` | Variables avec `anvilGroup == tag` (un groupe IPC Anvil). |
| `FilterByHmi` | Variables avec `hmiGroup == tag` (un groupe HMI Bellows). |
| `FilterByBus` | Variables avec `busBinding.deviceId == tag` (toutes les variables d'un périphérique de bus). |
| `FilterByModule` | Comme `FilterByBus`, plus `moduleSlot` — format de tag `hostname:slot`. |
| `FilterByPou` | Locales de POU — variables avec `pouInterface == tag`. |
| `FilterCommentsOnly` | Seulement les séparateurs de commentaire, pas de variables. |

## Axes de filtre (composables)

Au-dessus du tableau se trouvent quatre axes supplémentaires qui
agissent tous en parallèle par-dessus le filtre d'arborescence :

  - **Recherche en texte libre** sur le nom, l'adresse et les tags —
    `to` trouve `T_Off`.
  - **Filtre de type IEC** comme combo (`all` / `BOOL` / `INT` /
    `REAL` / ...).
  - **Filtre de plage d'adresses** : `all` / `%I` (entrées) / `%Q`
    (sorties) / `%M` (marqueurs) ; au sein de `%M`, plus loin par
    taille de mot (`%MX` / `%MW` / `%MD` / `%ML`).
  - **Bascule TaggedOnly** — masque chaque entrée de pool sans aucun
    tag de conteneur (utile pour trouver un pool « orphelin »).

Chaque filtre est combiné en AND : tout ce qui ne correspond pas à tous
les axes actifs est masqué.

## Multi-sélection + opérations groupées

Comme dans tout tableau Qt : Maj-clic et Ctrl-clic sélectionnent des
plages ou des lignes individuelles. Le menu contextuel sur la sélection
propose :

  - **Set Anvil Group...** — définit `anvilGroup` sur chaque variable
    sélectionnée.
  - **Set HMI Group...** — idem pour `hmiGroup`.
  - **Set GVL Namespace...** — idem pour `gvlNamespace`.
  - **Clear Tag** — retire le tag du mode de filtre actif.
  - **Toggle Monitor / HMI / Force** — bascule groupée des interrupteurs
    de sécurité.

Chaque édition groupée passe par `FAddressPoolModel::applyToRows`,
résulte en un seul signal `dataChanged`, et est annulable comme une
seule étape d'undo.

## Presse-papiers (copier / couper / coller)

Les variables sélectionnées peuvent être copiées — **avec tous les tags
et drapeaux** — et collées dans une autre vue. La charge utile utilise
deux formats :

  - **MIME personnalisé** (`application/x-forgeiec-vars+json`) comme
    véhicule de roundtrip portant l'information complète du pool.
  - **TSV en texte brut** comme repli pour Excel / éditeurs de texte.

Au **collage**, le panneau retargete automatiquement les tags de
conteneur sur le **mode de filtre actif** : copier depuis
`FilterByAnvil` (groupe `Pfirsich`) et coller dans `FilterByHmi` (groupe
`Stachelbeere`) et les variables abandonnent leur `anvilGroup` et
adoptent `hmiGroup = Stachelbeere`. Les adresses et noms en conflit
sont dédupliqués (`T_1` → `T_1_1`).

## Glisser/déposer dans HmiVarList

Les variables peuvent être glissées du panneau principal dans un POU
HmiVarList. L'éditeur définit alors automatiquement le **drapeau
d'export HMI** de la variable et écrit le groupe HMI comme tag —
l'export Bellows est désormais armé.

## Interrupteurs de sécurité par variable

Trois interrupteurs par variable, chacun nécessitant un opt-in
explicite :

  - **HMI** — autorise Bellows à lire/écrire la variable.
  - **Monitor** — autorise l'observation en direct en mode en ligne.
  - **Force** — autorise le forçage d'une valeur d'exécution.

Ces drapeaux sont **distincts du tag `hmiGroup`**. Le tag décrit
l'appartenance au groupe ; le drapeau active l'effet. Avant chaque
génération de code, le compilateur ST vérifie que chaque accès Bellows
ou Force cible une variable dont le drapeau est défini — sinon il lève
une erreur de compilation.

## Sujets liés

  - [Ajouter une variable](add/) — le `FAddVariableDialog` avec patterns
    de plage et le wrapper de tableau.
  - [Format de fichier de projet](../file-format/) — comment le pool est
    persisté en bloc `<addData>` dans PLCopen XML.
  - [Bibliothèque](../library/) — comment les blocs fonctionnels voient
    leurs instances dans le pool.
