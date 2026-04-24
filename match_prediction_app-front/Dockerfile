# Dockerfile simple pour développement Vue.js
FROM node:18-alpine

WORKDIR /app

# Installer les dépendances
COPY package*.json ./
RUN npm install

# Copier le code source
COPY . .

# Exposer le port de développement
EXPOSE 8080

# Démarrer le serveur de développement Vue.js
CMD ["npm", "run", "serve"]
