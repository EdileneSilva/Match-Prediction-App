# Logbook - Feature: Futuristic Landing Page & Team Dev Access

Ce logbook résume les modifications apportées à la branche `feature/futuristic-landing-page` pour optimiser le pipeline de prédiction et permettre un accès de développement facilité pour l'équipe.

## 🚀 Modifications Apportées

### 1. Intelligence Artificielle (Pipeline v3)
- **Modèle Ensemble (Stacking)** : Intégration d'un modèle de Stacking combinant **Random Forest**, **XGBoost** et **Logistic Regression**.
- **Calibration des Probabilités** : Utilisation de `CalibratedClassifierCV` pour des probabilités plus fiables (Accuracy: 57.55%, Log Loss: 0.9299).
- **Market Intelligence** : Utilisation des cotes moyennes de paris comme indicateurs de force des équipes.

### 2. Accès de Développement (Auth Bypass)
- **Frontend** : 
    - Bypass du middleware d'authentification dans `src/router/index.js`.
    - Ajout de liens directs vers "Prédictions" et "Historique" dans la `NavBar` pour une navigation sans compte.
    - Correction de bug dans `HistoryView.vue` (gestion des détails et calculs de stats).
- **Backend (FastAPI_App & FastAPI_ML)** :
    - Suppression temporaire des dépendances `get_current_user` sur les routes de prédiction et d'historique.
    - Configuration CORS mise à jour pour le développement local.

### 3. Transition vers SQLite (Zero Config)
- **Migration PostgreSQL -> SQLite** : Passage temporaire à SQLite pour supprimer la dépendance à un serveur Postgres externe.
- **Auto-Initialization** : Création automatique des tables au démarrage si elles n'existent pas.
- **Seeding Automatique** : Création d'un utilisateur par défaut (`id=1`) et chargement automatique de la liste des équipes de Premier League dans la base de données ML au lancement.

---

## 🛠️ Instructions de Lancement

Pour lancer l'environnement complet, ouvrez **3 terminaux séparés** :

### Terminal 1 : Backend API (Main)
```bash
cd FastAPI_App
python3 -m uvicorn app.main:app --port 8000 --reload
```
*Note : Utilise la base `FastAPI_App/app.db`.*

### Terminal 2 : Moteur ML (Intelligence Engine)
```bash
cd FastAPI_ML
python3 -m uvicorn app.main:app --port 8001 --reload
```
*Note : Utilise la base `FastAPI_ML/ml_app.db`.*

### Terminal 3 : Frontend (Vue.js)
```bash
cd match_prediction_app-front
npm run serve
```
*Accès : http://localhost:8080*

---

## 🛡️ Rappels de Sécurité
> [!WARNING]
> Ces modifications sont strictement destinées au développement et aux tests internes. L'authentification est désactivée. Avant de fusionner sur `main`, il est impératif de restaurer la sécurité et les configurations PostgreSQL.

---

## 🌌 Récents Développements (Branche `feature/cosmic-glassmorphism-style`)

### 1. Refonte Interface Utilisateur (UI/UX)
- **Thème "Cosmic Glassmorphism"** : Mise en place d'un design futuriste avec des effets de transparence sur verre (glassmorphism), des gradients spatiaux et des incrustations néon.
- **Réactivité & Micro-animations** : Ajout de transitions fluides et de halos interactifs au survol (hover) sur les cartes d'équipe et l'arène de prédiction pour un rendu nettement plus premium et immersif.
- **Médias Démonstratifs** : Intégration d'images conceptuelles ciblées (ballons futuristes, nébuleuses, stades) sur l'ensemble du parcours utilisateur.

### 2. Correction et Stabilisation du Pipeline de Prédiction
- **Erreur 422 Unprocessable Entity ("Load failed")** : 
  - **Le Problème** : L'API principale (`FastAPI_App`) envoyait uniquement les identifiants numériques (`home_team_id`, `away_team_id`) au service Machine Learning (`FastAPI_ML`), alors que ce dernier (récemment mis à jour) exigeait les noms texte complets, la saison, la journée et le nom de l'arbitre.
  - **La Solution** : Remaniement de la fonction d'appel dans `FastAPI_App/routes/prediction.py` pour transmettre au modèle le bon format de payload requis.
- **Erreurs 500 Internal Server Error (PostgreSQL & KeyErrors)** :
  - **Problème A (Dictionnaire)** : L'application plantait en lisant la réponse du modèle ML : ce dernier envoyait les attributs `prediction` et `confidence`, tandis que l'application tentait de lire aveuglément `predicted_result` et `confidence_score`.
  - **Solution A** : Correction du mapping dans le backend principal.
  - **Problème B (Base de données désynchronisée)** : Plantage complet lors de la sauvegarde d'historique (renvoyant une autre erreur CORS masquée en "Load failed" sur le frontend) car la table PostgreSQL `prediction_history` manquait de 4 colonnes récemment ajoutées aux ORM (`home_team_logo_url`, `away_team_logo_url`, `predicted_result`, `confidence_score`).
  - **Solution B** : Exécution de séquences directes `ALTER TABLE` via `psql` pour injecter immédiatement ces colonnes dans la base locale et débloquer les sauvegardes sans toucher à la structure de migration de base.

---

## 📊 Expansion du Dashboard & Synchronisation ML

### 1. Dashboard de Ligue 1 Complet
- **Classement National** : Intégration d'un scraper LFP robuste pour afficher le classement officiel de la Ligue 1 en temps réel (Points, MJ, GA).
- **Matchs à Venir** : Extension de la liste des rencontres (passage de 3 à 15 matchs) pour couvrir l'intégralité d'une journée de championnat.
- **Rafraîchissement Dynamique** : Ajout d'un bouton d'actualisation avec animations GSAP pour synchroniser les données sans recharger la page.

### 2. Fiabilité de l'Intelligence Artificielle
- **Mapping des Équipes** : Création d'un utilitaire de mapping (`team_mapper.py`) pour faire la jonction entre les noms complets LFP et les noms abrégés du modèle ML (ex: "Paris Saint-Germain" ➔ "Paris SG").
- **Fin des Fallbacks Aléatoires** : Suppression des valeurs de confiance aléatoires. Le dashboard affiche désormais le véritable indice de probabilité (XGBoost) ou une valeur neutre explicite en cas d'absence de données.
- **Transparence UI** : Ajout d'une icône d'information sur les cartes de match expliquant l'origine de l'indice de confiance IA.

### 3. Optimisation de l'Expérience Utilisateur (UX)
- **Correction du Scroll** : Suppression des contraintes CSS (`height: 100%`) et des zones de défilement imbriquées qui bloquaient la navigation au trackpad/finger-scroll. La page défile désormais de manière fluide et naturelle.
- **Design Premium** : Amélioration des contrastes et de l'accessibilité visuelle des badges de prédiction.
