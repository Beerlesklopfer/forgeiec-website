---
title: "ForgeIEC"
---

<div style="text-align:center; padding: 3rem 1rem;">

# Forge pour l'industrie.

**Un environnement de developpement IEC 61131-3 de qualite industrielle. Open source.**

[Contact](mailto:blacksmith@forgeiec.io)

</div>

---

## Ce que nous construisons

ForgeIEC est un environnement de developpement IEC 61131-3 complet pour
l'automatisation industrielle — les cinq langages IEC, les systemes
de bus industriels, le debogage en temps reel.

Developpe avec l'ambition de rivaliser avec les systemes commerciaux etablis.
Chaque fonction est validee par des tests documentes avant publication.

---

## Pourquoi l'open source

L'automatisation industrielle est une technologie cle. Mais l'acces aux
outils professionnels est limite par les couts de licence et les systemes
proprietaires. ForgeIEC rend la valeur de l'automatisation accessible
a tous — sans dependance fournisseur, sans frais de licence.

En tant que projet open source, ForgeIEC appartient a la communaute.

---

## Démarrer

```bash
# Installer la clé de signature (une seule fois)
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://apt.forgeiec.io/forgeiec.gpg \
  | sudo tee /etc/apt/keyrings/forgeiec.gpg >/dev/null

# Ajouter la source du dépôt
echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/forgeiec.gpg] \
https://apt.forgeiec.io/trixie trixie main" \
  | sudo tee /etc/apt/sources.list.d/forgeiec.list

# Installer l'éditeur + le runtime
sudo apt update
sudo apt install forgeiec-studio forgeiec-anvil-server
```

Exemple pour Debian 13 (trixie). Pour Debian 12 (bookworm) ou Ubuntu 24.04 (noble), remplacez les deux occurrences de `trixie`. Toutes les distributions, RPM et les autres paquets : [Téléchargement](/download/).

---

<div style="text-align:center; padding: 2rem;">

**Nous publierons des informations detaillees des qu'une version
de qualite industrielle sera disponible.**

blacksmith@forgeiec.io

</div>
