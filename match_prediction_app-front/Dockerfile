# =============================================================================
# Match Prediction App - Vue.js Frontend
# =============================================================================
# Multi-stage build for production-optimized image

# Stage 1: Build stage
FROM node:20-alpine as builder

WORKDIR /app

# Copy package files first for better caching
COPY package.json .
COPY package-lock.json .

# Install dependencies
RUN npm ci

# Copy all source files
COPY src/ ./src/
COPY public/ ./public/
COPY vue.config.js .

# Build the application
RUN npm run build

# =============================================================================
# Stage 2: Runtime stage
FROM nginx:alpine

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Run nginx
CMD ["nginx", "-g", "daemon off;"]
