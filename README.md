# StartAllPatch (![PyPass-SAB v2 Unofficial](https://github.com/GuillaumeMCK/PyPass-SAB))

![StartAllPatch Logo](https://github.com/danbenba/StartAllPatch/blob/main/.assets/icon.png) <!-- Assurez-vous d'ajouter un logo dans le dossier assets -->

StartAllPatch est une application puissante conçue pour patcher le logiciel **StartAllBack**, offrant des fonctionnalités personnalisées telles que la désactivation des rappels d'essai et des mises à jour automatiques. Simplifiez et personnalisez votre expérience utilisateur avec StartAllPatch.

**Projet inspiré de ![PyPass-SAB](https://github.com/GuillaumeMCK/PyPass-SAB)**

---

## 🗂️ Table des Matières
1. [Introduction](#introduction)
2. [Fonctionnalités](#fonctionnalités)
3. [Installation](#installation)
4. [Configuration Initiale](#configuration-initiale)
5. [Utilisation](#utilisation)
   - [Application du Patch](#application-du-patch)
   - [Restauration des Fichiers](#restauration-des-fichiers)
   - [Désactivation des Mises à Jour](#désactivation-des-mises-à-jour)
6. [Capture d'Écran](#capture-décran)
7. [Dépannage](#dépannage)
8. [Contribution](#contribution)
9. [Licence](#licence)
10. [Notes de Version](#notes-de-version)
11. [Support](#support)

---

## ✨ Introduction

StartAllPatch est une solution dédiée à l'amélioration de **StartAllBack**, permettant aux utilisateurs de personnaliser et d'optimiser leur expérience. Que vous souhaitiez désactiver les rappels d'essai ou empêcher les mises à jour automatiques, StartAllPatch offre une interface conviviale pour gérer ces modifications en toute simplicité.

> **Lien GitHub** : [https://github.com/danbenba/StartAllPatch](https://github.com/danbenba/startallpatch)

---

## 🚀 Fonctionnalités

- **Désactivation des Rappels d'Essai** : Éliminez les notifications répétitives pour une utilisation ininterrompue.
- **Blocage des Mises à Jour Automatiques** : Contrôlez manuellement les mises à jour de StartAllBack.
- **Gestion des Backups** : Créez et restaurez facilement des sauvegardes de vos fichiers modifiés.
- **Interface Intuitive** : Une interface utilisateur claire et facile à naviguer.
- **Compatibilité Étendue** : Supporte plusieurs versions de StartAllBack (3.5.5 à 3.6.5).

---

## 🛠️ Installation

### Prérequis

- **Système d'exploitation** : Windows 10 ou supérieur.
- **StartAllBack** : Version 3.5.5 à 3.6.5 installée.
- **Python 3.8+** (si vous utilisez les sources).

### Étapes d'Installation

1. **Téléchargement**
   - Téléchargez les fichiers sources ou l'exécutable depuis le [référentiel GitHub](https://github.com/danbenba/startallpatch).

2. **Installation des Dépendances (pour les sources)**
   ```bash
   pip install -r requirements.txt
   ```

3. **Exécution de l'Application**
   - **Exécutable** : Double-cliquez sur `StartAllPatch.exe`.
   - **Sources** :
     ```bash
     python src/app.py
     ```

4. **Installation via Package Manager** *(Optionnel)*
   - Si disponible, vous pouvez installer via un gestionnaire de paquets comme `pip`.

---

## ⚙️ Configuration Initiale

1. **Mode Thème**
   - **Sombre/Clair** : Le thème par défaut est sombre. Vous pouvez le changer dans les paramètres de l'application.

2. **Chemin des Actifs**
   - Les ressources nécessaires, telles que les icônes et images, sont chargées automatiquement depuis le dossier `src/assets`.

3. **Paramètres Avancés**
   - Accédez aux paramètres avancés pour personnaliser davantage les fonctionnalités selon vos besoins.

---

## 🖥️ Utilisation

### 🛠️ Application du Patch

1. **Lancer l'Application**
   - Exécutez l'application en tant qu'administrateur pour garantir les permissions nécessaires.

2. **Vérification Préalable**
   - Cliquez sur le bouton `Check` pour vérifier l'éligibilité du fichier `StartAllBackX64.dll`.

3. **Appliquer le Patch**
   - Si le fichier est éligible, cliquez sur le bouton `Patch`. Un backup sera automatiquement créé si l'option "Backup" est activée.

4. **Confirmation des Résultats**
   - Consultez les messages de statut dans l’interface ou dans l’Event Viewer pour confirmer la réussite du patch.

### 🔄 Restauration des Fichiers

1. **Depuis un Backup Existant**
   - Cliquez sur `Restore` pour restaurer les fichiers depuis la dernière sauvegarde.

2. **Sélection Manuelle**
   - Si aucun backup n’est détecté, un explorateur de fichiers s’ouvrira pour sélectionner manuellement le fichier à restaurer.

### ⛔ Désactivation des Mises à Jour

1. **Démarrer le Processus**
   - Cliquez sur `Disable Updates` pour désactiver les mises à jour automatiques de StartAllBack.

2. **Exclusions de Windows Defender**
   - Le fichier `UpdateCheck.exe` sera automatiquement ajouté aux exclusions de Windows Defender pour éviter toute interférence.

---

## 📷 Capture d'Écran

![Interface StartAllPatch](https://github.com/danbenba/StartAllPatch/blob/main/.assets/banner.png) <!-- Ajoutez une capture d'écran dans le dossier assets -->

*Interface utilisateur de StartAllPatch montrant les options principales.*

---

## 🛠️ Dépannage

1. **Message d’Erreur "Fichier introuvable"**
   - **Solution** : Vérifiez que `StartAllBackX64.dll` est bien installé dans `C:/Program Files/StartAllBack/`.

2. **Patch Échoué**
   - **Solution** : Assurez-vous que l'application est lancée avec des droits administrateurs. Réessayez également de redémarrer l'application.

3. **Problèmes de Compatibilité**
   - **Solution** : Vérifiez que vous utilisez une version compatible de StartAllBack (3.5.5 à 3.6.5). Contactez le support si le problème persiste.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer à **StartAllPatch**, veuillez suivre les étapes ci-dessous :

1. **Fork le Projet**
2. **Créez une Branche** pour votre fonctionnalité (`git checkout -b feature/nom-de-la-fonctionnalité`)
3. **Commitez Vos Changements** (`git commit -m 'Ajout de la fonctionnalité X'`)
4. **Poussez la Branche** (`git push origin feature/nom-de-la-fonctionnalité`)
5. **Ouvrez une Pull Request**

Pour des contributions majeures, veuillez ouvrir une issue au préalable pour discuter des changements.

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](https://github.com/danbenba/StartAllPatch/blob/main/LICENSE) pour plus de détails.

---

## 📝 Notes de Version

### **Version 0.9.5**
- Compatibilité étendue avec StartAllBack 3.x.x (Parfois INSTABLE).
- Support complet pour les versions 3.5.5 à 3.6.5.
- Gestion améliorée des fonctions `CheckLicense` et `CompareFileTime`.
- Optimisations de performance et corrections de bugs mineurs.

### **Version 0.8.3**
- Support UNIQUEMENT pour les versions 3.5.5 à 3.6.5.
- Interface utilisateur initiale avec options de base.
- Support des opérations de backup et restauration.
- Améliorations de la stabilité générale.

---

## 📞 Support

Pour tout problème ou question, veuillez :

- **Consulter le [dépôt GitHub](https://github.com/danbenba/startallpatch)** : Recherchez des issues similaires ou ouvrez-en une nouvelle.
- **Rejoindre la Communauté** : Participez aux discussions sur notre [forum Discord](https://discord.gg/yourdiscordlink) *(remplacez par votre lien Discord si disponible)*.
- **Envoyer un Email** : Contactez-nous directement à [danbenba@proton.me](mailto:danbenba@proton.me).

---

Merci d'utiliser **StartAllPatch** ! Votre soutien et vos contributions nous aident à améliorer continuellement cette application.
