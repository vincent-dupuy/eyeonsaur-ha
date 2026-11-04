# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.1.13-vd1] - 2026-11-04

### Fixed
- 🛠️ Index théorique calculé même si la date d'ancre (relevé technicien) n'est pas dans la table journalière : cumul recalé sur la date la plus proche, puis accumulation avant / arrière
- 🛠️ Les erreurs de conversion ne sont plus avalées par `print()`, elles sont journalisées
- 🛠️ Le backfill initial récupère tous les mois entre l'installation et le mois courant (plus de blocage si le premier mois est vide)
- 🛠️ Compatibilité Home Assistant 2026.11 : `mean_type=StatisticMeanType.NONE` et `unit_class` volume pour les statistiques de somme, avec repli pour les versions antérieures

## [v1.1.11] - 2024-02-28 (+v1.1.9 + fix DEV + FIX pypi + fix UTC)

### Added
- ✨ Ajout du capteur **Date Installation**
- ✨ Ajout du capteur **Date Contrat**
- ✨ Ajout du capteur **Date Relevé physique**
- ✨ Ajout du capteur **Valeur Relevé physique**
- ✨ Ajout du capteur **Numéro de série**
- ⚡ Ajout du capteur **Valeur pour Panneau Énergie**
- 🔄 Gestion de tous les **compteurs actifs**
- 📦 Regroupement des **compteurs actifs par contrats**
- ✨ Récupération et persistance des données **Saur** de manière efficace
- 🚀 Récupération des points de livraison en **parallèle**
- 🚀 Récupération des dernières données connues en **parallèle**
- 🔑 Mise à jour de l'entrée de configuration avec le **token**
- ⚡ Amélioration du **flux de configuration** et de la gestion de l'authentification
- 🔐 Utilisation de **TextSelector** pour le login/mot de passe
- 📝 Simplification de la vérification des **identifiants**
- 💾 Enregistrement du **clientId** et du **compteurId**
- 🔧 Enregistrement du **unique_id** dans `hass.data`
- 🎛️ Ajout de **données API mockées** pour les tests
- 🧪 Ajout de `area.json`, `auth.json`, et `weekly.json`

### Fixed
- 🛠️ Rétablissement du **dernier relevé** dans les attributs du capteur
- 🛠️ Correction du **mode DEV** et ajout de **CONF_CLIENT_ID**
- 🔄 Définir DEV sur True au moment de l'exécution
- 🔑 Ajout de la constante **CONF_CLIENT_ID**
- 🔧 Correction du **blocage des sockets dans les tests**
- 🚪 Autorisation de tous les sockets dans les tests
- 🔧 Correction du **FLAG DEV**

### Changed
- 📜 Le fichier `manifest.json` utilise maintenant **PyPi**
- ⬆️ Mise à jour de la dépendance `Saur_fr_clientr` vers la version **0.3.2** de **PyPi**
- 🔨 Refactorisation de l'**extraction des données des dispositifs**
- 📦 Refactorisation de la classe `Compteur`
- 📡 Extraction depuis le **point de terminaison AREA**
- 🗂️ Ajout de la collection **Compteurs**
- ⚙️ Mise à jour des dépendances et de la configuration
- 📜 Mise à jour de la **configuration pyright**
- 🚀 Mise à jour de la **liste d'exclusion ruff**
- 📈 Mise à jour des **sources de couverture**

### Dependency Updates
- ⬆️ Mise à jour de la dépendance `Saur_fr_clientr` vers la version **0.3.2** de **PyPi**

### Deprecated
- 🚫 Fonctionnalité dépréciée : **Aucune**

### Removed
- 🗑️ Fonctionnalité supprimée : **Aucune**
