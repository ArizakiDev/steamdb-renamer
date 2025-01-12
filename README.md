# 🎮 SteamDB renamer

> Un outil pour renomer vos appID en jeux steam via l'api de steam
[![Python version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

## 📋 Description

Cette collection d'outils Python permet de :
- Renommer automatiquement vos fichiers Steam en utilisant les données de l'API
- Obtenir des informations détaillées sur vos jeux
- Interface utilisateur moderne avec des indicateurs de progression en temps réel

## 🚀 Installation

1. Clonez le repository :
```bash
git clone https://github.com/ArizakiDev/steamdb-renamer.git
cd steam-tools
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez votre clé API Steam :
   - Mettez-y votre clé API steam

## 🔧 Configuration requise

- Python 3.8 ou supérieur
- Clé API Steam (voir notre [guide de configuration](readme.html))
- Connexion Internet pour les requêtes API

## 📖 Utilisation

### Renommage des fichiers Steam

```bash
python renamerDB.py <chemin_dossier>
```

Exemple :
```bash
python renamerDB.py ./mes_jeux
```
## ✨ Fonctionnalités

- 🔄 Renommage automatique des fichiers avec les noms officiels des jeux
- 📊 Interface utilisateur riche avec barres de progression
- 🌐 Support multilingue (Français/Anglais)
- 📝 Journalisation détaillée des opérations
- 🔒 Gestion sécurisée des clés API
- 🎨 Sortie console colorée et formatée

## 🙏 Remerciements

- [Rich](https://github.com/Textualize/rich) pour l'interface console
- [Requests](https://github.com/psf/requests) pour les requêtes HTTP
- La communauté Steam pour son support

## 🔍 Notes de version

### v2.0.0 (2025-01-12)
- ✨ Ajout du support multilingue
- 🎨 Nouvelle interface utilisateur
- 🔧 Amélioration de la gestion des erreurs
- 📝 Documentation mise à jour

### v1.0.0 (2025-01-12)
- 🚀 Version initiale
- 📦 Fonctionnalités de base
