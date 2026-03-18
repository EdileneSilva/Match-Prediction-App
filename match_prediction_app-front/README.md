# Match Prediction App - Frontend

Application frontend Vue.js pour la prédiction de matchs sportifs.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants sur votre machine :

- **Node.js** (version 16 ou supérieure) - [Télécharger Node.js](https://nodejs.org/)
- **npm** (généralement inclus avec Node.js) ou **yarn** comme gestionnaire de paquets
- **Git** pour cloner le dépôt

Pour vérifier vos installations :
```bash
node --version
npm --version
```

## Installation du projet

1. **Cloner le dépôt**
   ```bash
   git clone <url-du-dépôt>
   cd Match-Prediction-App/match_prediction_app-front
   ```

2. **Installer les dépendances**
   ```bash
   npm install
   ```
   Ou si vous préférez yarn :
   ```bash
   yarn install
   ```

## Démarrage du projet

### Pour le développement (avec hot-reload)
```bash
npm run serve
```
L'application sera accessible à l'adresse : `http://localhost:8080`

### Pour la production (build optimisé)
```bash
npm run build
```
Les fichiers de production seront générés dans le dossier `dist/`.

## Tests

### Lancer les tests unitaires
```bash
npm run test:unit
```

## Structure du projet

```
match_prediction_app-front/
├── public/          # Fichiers statiques
├── src/
│   ├── components/  # Composants Vue.js
│   ├── views/       # Pages/Vues de l'application
│   ├── router/      # Configuration du routeur
│   ├── assets/      # Ressources (images, styles)
│   └── main.js      # Point d'entrée de l'application
├── package.json     # Dépendances et scripts
└── README.md        # Ce fichier
```

## Technologies utilisées

- **Vue.js 3** - Framework JavaScript progressif
- **Vue Router 4** - Routage officiel pour Vue.js
- **Vue CLI 5** - Outil de développement pour Vue.js
- **Jest** - Framework de test JavaScript

## Dépannage

### Problèmes courants

**Erreur : "npm command not found"**
- Assurez-vous que Node.js est correctement installé
- Redémarrez votre terminal après l'installation

**Erreur : "EACCES: permission denied"**
- Essayez avec `sudo npm install` (non recommandé pour le développement)
- Ou configurez npm pour éviter les permissions : `npm config set prefix ~/.npm-global`

**Erreur de port 8080 déjà utilisé**
- Le serveur essaiera automatiquement le port suivant (8081, 8082, etc.)
- Ou spécifiez un autre port : `npm run serve -- --port 3000`

### Nettoyer les dépendances

Si vous rencontrez des problèmes, vous pouvez réinitialiser complètement le projet :

```bash
# Supprimer le dossier node_modules et le fichier package-lock.json
rm -rf node_modules package-lock.json

# Réinstaller les dépendances
npm install
```

## Configuration avancée

Pour personnaliser la configuration de Vue CLI, consultez la [documentation officielle](https://cli.vuejs.org/config/).

## Contribuer

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request
