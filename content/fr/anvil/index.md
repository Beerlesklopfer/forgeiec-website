---
title: "Anvil Technology\u00ae"
summary: "Vos donnees sont forgees sur notre enclume"
---

## L'Enclume : Coeur de chaque forge

Dans chaque forge, l'enclume est la piece maitresse — la ou le metal est
faconne, trempe et affine. **Anvil Technology\u00ae** est la couche intermediaire entre le
systeme d'execution de l'automate et les bridges de bus de terrain. C'est
ici que vos donnees de processus sont forgees : recues, transformees et
distribuees aux bons destinataires.

Anvil utilise en interne un transport proprietaire de memoire partagee
zero-copie pour la communication inter-processus. Pas de
serialisation, pas de copies, pas de compromis.

---

## Architecture

```
┌──────────────┐         ┌────────────┐         ┌──────────────────┐
│              │         │            │         │                  │
│ Programme    │◄───────►│  anvild  │◄───────►│  Bridge Modbus   │──► Peripheriques
│  automate    │  gRPC   │  (Daemon)  │  Anvil  │  Bridge EtherCAT │──► Variateurs
│  (IEC)       │         │            │ Anvil   │  Bridge Profibus  │──► Capteurs
└──────────────┘         └────────────┘         │  Bridge OPC-UA   │──► SCADA
                                                └──────────────────┘

                         ◄── Anvil ──►
                         Zero-Copy IPC
                         Memoire partagee
```

L'echange de donnees entre `anvild` et les bridges de protocole passe
par **Anvil Technology\u00ae** — un canal IPC haute performance base sur la memoire partagee
zero-copie. Chaque segment dispose de son propre canal de communication.

---

## Pourquoi Anvil Technology\u00ae ?

### Latence microseconde

Les mecanismes IPC conventionnels (pipes, sockets, files de messages)
copient les donnees entre les processus. Anvil elimine chaque copie.
Les donnees resident en memoire partagee — le recepteur lit directement.

| Methode | Latence typique | Copies |
|---------|----------------|--------|
| Socket TCP | 50–200 us | 2–4 |
| Socket Unix | 10–50 us | 2 |
| **Anvil Technology\u00ae** | **< 1 us** | **0** |

### Qualite industrielle

- Comportement deterministe — pas d'allocation dynamique dans le chemin critique
- Algorithmes sans verrou — pas de blocage, pas de deadlock
- Modele publish/subscribe — couplage lache entre producteur et consommateur
- Gestion automatique du cycle de vie — les bridges sont surveillees et redemarrees en cas de crash

### PUBLISH/SUBSCRIBE dans le programme IEC

Anvil Technology\u00ae s'integre de maniere transparente dans la programmation IEC 61131-3 :

```iec
VAR_GLOBAL PUBLISH 'Moteurs'
    K1_Mains    AT %QX0.0 : BOOL;
    K1_Speed    AT %QW10  : INT;
END_VAR

VAR_GLOBAL SUBSCRIBE 'Capteurs'
    Temperature AT %IW0   : INT;
    Pression    AT %IW2   : INT;
END_VAR
```

Les mots-cles PUBLISH/SUBSCRIBE sont une extension ForgeIEC de la norme
IEC 61131-3. Le compilateur genere automatiquement les liaisons Anvil.

---

## Protocoles supportes

| Protocole | Bridge | Statut |
|-----------|--------|--------|
| **Modbus TCP** | `tongs-modbustcp` | Disponible |
| **Modbus RTU** | `tongs-modbusrtu` | Disponible |
| **EtherCAT** | `tongs-ethercat` | En developpement |
| **Profibus DP** | `tongs-profibus` | En developpement |
| **OPC-UA** | `tongs-opcua` | Prevu |

Chaque bridge fonctionne comme un processus independant. `anvild` demarre,
surveille et redemarre les bridges automatiquement.

---

<div style="text-align:center; padding: 2rem;">

**Anvil Technology\u00ae — La ou les donnees sont forgees en commandes de controle.**

blacksmith@forgeiec.io

</div>
