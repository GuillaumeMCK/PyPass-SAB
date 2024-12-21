#StartAllPatch

---

#### Table des Matières
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration Initiale](#configuration-initiale)
4. [Utilisation](#utilisation)
   - [Application du Patch](#application-du-patch)
   - [Restauration des Fichiers](#restauration-des-fichiers)
   - [Désactivation des Mises à Jour](#désactivation-des-mises-à-jour)
5. [Dépannage](#dépannage)
6. [Notes de Version](#notes-de-version)

---

#### Introduction

StartAllPatch est une application conçue pour patcher le logiciel **StartAllBack** et ajouter des fonctionnalités personnalisées telles que la désactivation des rappels d'essai et des mises à jour automatiques. 

> **Lien GitHub** : [https://github.com/danbenba/StartAllPatch](https://github.com/danbenba/startallpatch)

---

#### Installation

1. Téléchargez les fichiers sources ou l'exécutable depuis le [référentiel GitHub](https://github.com/danbenba/startallpatch).
2. Si vous utilisez les sources, installez les dépendances nécessaires :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancez le fichier principal :
   ```bash
   python src/app.py
   ```

---

#### Configuration Initiale

1. **Mode Sombre/Clair** : Le thème de l'application est configuré en mode sombre par défaut.
2. **Chemin des Actifs** : Les actifs nécessaires, tels que les icônes, sont automatiquement chargés depuis `src/assets`.

---

#### Utilisation

##### Application du Patch

1. **Lancer le programme :**
   - Exécutez l'application en tant qu'administrateur.
2. **Vérification préalable :**
   - Cliquez sur le bouton `Check` pour vérifier si le fichier `StartAllBackX64.dll` est éligible.
3. **Appliquer le patch :**
   - Si éligible, cliquez sur le bouton `Patch`. Un backup sera créé si l'option "Backup" est activée.
4. **Résultats :**
   - Vérifiez les messages de statut dans l’interface Event Viewer pour confirmation.

##### Restauration des Fichiers

1. **Restauration depuis un backup existant :**
   - Cliquez sur `Restore`.
2. **Sélection manuelle du fichier :**
   - Si aucun backup n’est détecté, un explorateur de fichiers s’ouvrira pour sélectionner le fichier.

##### Désactivation des Mises à Jour

1. **Lancer le processus :**
   - Cliquez sur `Disable Updates`.
2. **Ajout aux exclusions de Windows Defender :**
   - Le fichier `UpdateCheck.exe` sera automatiquement ajouté aux exclusions.

---

#### Dépannage

1. **Message d’erreur "Fichier introuvable" :**
   - Vérifiez que `StartAllBackX64.dll` est bien installé dans `C:/Program Files/StartAllBack/`.
2. **Patch échoué :**
   - Assurez-vous que l'application est lancée avec des droits administrateurs.

---

#### Notes de Version

- **Version 0.9.5**
  - Compatibilité étendue avec StartAllBack 3.x.x (Parfois INSTABLE).
  - Parfait support pour les versions 3.5.5 à 3.6.5.
  - Gestion des fonctions `CheckLicense` et `CompareFileTime` améliorée.

- **Version 0.8.3**
  - Support UNIQUEMENT pour les versions 3.5.5 à 3.6.5.
  - Interface utilisateur initiale.
  - Support des opérations de backup et restauration.

---

Pour tout problème ou contribution, veuillez consulter le [dépôt GitHub](https://github.com/danbenba/startallpatch).
