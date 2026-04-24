# Étape de build pour compiler l'application Vue.js
FROM node:18-alpine AS builder

WORKDIR /app

# Installer les dépendances
COPY package*.json ./
RUN npm install

# Copier le code source et builder
COPY . .
RUN npm run build

# Étape de production avec nginx
FROM nginx:alpine

# Copier les fichiers construits dans nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Copier la configuration nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
