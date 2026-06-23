# match_prediction_app-front - Frontend Context

## Purpose
This is the **Vue.js 3 frontend** component of the Match Prediction App, running on **port 8080**.

## Responsibilities

This frontend provides:
- **User Interface**: Interactive web application for match predictions
- **Authentication**: Login, registration, and logout flows
- **Prediction Interface**: Form to make match predictions
- **Results Display**: View prediction results and history
- **Favorites Management**: Track favorite teams
- **Responsive Design**: Works on desktop and mobile devices

## Architecture

```
match_prediction_app-front/
├── public/                 # Static files
│   ├── index.html          # Main HTML entry point
│   └── favicon.ico
├── 
├── src/
│   ├── main.js             # Vue application entry point
│   ├── App.vue             # Root Vue component
│   │
│   ├── assets/             # Static assets (images, styles)
│   │   ├── styles/         # Global CSS and SCSS
│   │   │   ├── main.scss   # Main stylesheet
│   │   │   └── variables.scss
│   │   └── images/          # Images and icons
│   │
│   ├── components/         # Vue components
│   │   ├── common/         # Reusable components
│   │   │   ├── Button.vue
│   │   │   ├── Card.vue
│   │   │   ├── Loader.vue
│   │   │   └── Modal.vue
│   │   ├── auth/           # Authentication components
│   │   │   ├── LoginForm.vue
│   │   │   └── RegisterForm.vue
│   │   ├── predictions/    # Prediction-related components
│   │   │   ├── PredictionForm.vue
│   │   │   ├── PredictionResult.vue
│   │   │   └── PredictionList.vue
│   │   ├── favorites/      # Favorite teams components
│   │   │   ├── FavoriteList.vue
│   │   │   └── FavoriteButton.vue
│   │   ├── teams/          # Team-related components
│   │   │   ├── TeamCard.vue
│   │   │   └── TeamSelect.vue
│   │   └── layout/         # Layout components
│   │       ├── Header.vue
│   │       ├── Footer.vue
│   │       ├── Sidebar.vue
│   │       └── NavBar.vue
│   │
│   ├── views/              # Page-level components (routes)
│   │   ├── Home.vue        # Home page (dashboard)
│   │   ├── Login.vue       # Login page
│   │   ├── Register.vue    # Registration page
│   │   ├── Predict.vue     # Make prediction page
│   │   ├── History.vue     # Prediction history page
│   │   ├── Favorites.vue   # Favorite teams page
│   │   ├── Profile.vue     # User profile page
│   │   └── NotFound.vue    # 404 page
│   │
│   ├── router/             # Vue Router configuration
│   │   └── index.js        # Route definitions with auth guards
│   │
│   ├── store/              # Vuex/Pinia state management
│   │   ├── index.js        # Store configuration
│   │   ├── auth.js         # Auth state
│   │   ├── user.js         # User state
│   │   ├── predictions.js  # Predictions state
│   │   └── favorites.js    # Favorites state
│   │
│   ├── api/                # API client configuration
│   │   ├── client.js       # Axios instance with interceptors
│   │   ├── auth.js         # Auth API calls
│   │   ├── users.js        # User API calls
│   │   ├── predictions.js  # Prediction API calls
│   │   └── favorites.js    # Favorite API calls
│   │
│   ├── utils/              # Utility functions
│   │   ├── helpers.js      # Helper functions
│   │   ├── validators.js   # Form validation
│   │   └── formatters.js   # Data formatting
│   │
│   └── styles/             # Global styles (if not in assets)
│
├── tests/                  # Unit and component tests
│   ├── unit/               # Unit tests
│   │   ├── components/
│   │   └── views/
│   └── e2e/                # End-to-end tests
├── 
├── .env                    # Frontend environment variables
├── jest.config.js          # Jest test configuration
├── jsconfig.json           # JavaScript configuration
├── nginx.conf              # Nginx configuration (for production)
├── package.json            # Node.js dependencies and scripts
├── vue.config.js           # Vue CLI configuration
└── README.md               # Frontend-specific documentation
```

## Environment Variables

Frontend configuration via `vue.config.js` or `.env`:

```env
# API Base URL (development)
VUE_APP_API_URL=http://localhost:8000

# API Base URL (production)
# VUE_APP_API_URL=https://api.yourdomain.com
```

## Key Dependencies

- **Vue.js 3**: Progressive JavaScript framework
- **Vue Router**: Official router for Vue.js
- **Vuex or Pinia**: State management
- **Axios**: HTTP client for API calls
- **Bootstrap/Vuetify/Tailwind**: UI framework (depending on project)
- **Sass**: CSS preprocessor
- **Jest**: Testing framework
- **@vue/test-utils**: Vue test utilities
- **vue-axios**: Axios integration for Vue

## API Integration

The frontend communicates with the **FastAPI_App** (port 8000) via Axios.

### Axios Client Configuration

The `src/api/client.js` file contains the Axios instance with:
- Base URL configuration
- JWT token interceptor (adds `Authorization: Bearer <token>` to requests)
- Response error handling
- Request/response interceptors

```javascript
// src/api/client.js
import axios from 'axios';

const client = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT token to requests
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default client;
```

### API Service Modules

Each API module in `src/api/` provides functions for specific endpoints:

**auth.js**:
- `login(email, password)` - POST /auth/login
- `register(userData)` - POST /auth/register
- `getMe()` - GET /auth/me
- `logout()` - Clears token

**predictions.js**:
- `getTeams()` - GET /predictions/teams
- `createPrediction(predictionData)` - POST /predictions
- `getHistory()` - GET /predictions/history

**favorites.js**:
- `getFavorites()` - GET /favorites
- `addFavorite(teamId)` - POST /favorites
- `removeFavorite(favoriteId)` - DELETE /favorites/{id}

**users.js**:
- `getUser(userId)` - GET /users/{id}
- `updateUser(userId, userData)` - PUT /users/{id}

## Routing

The `src/router/index.js` file defines all application routes with authentication guards:

```javascript
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/predict',
    name: 'Predict',
    component: () => import('../views/Predict.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/History.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('../views/Favorites.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/404',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Authentication guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.meta.guestOnly && isAuthenticated) {
    next('/');
  } else {
    next();
  }
});

export default router;
```

## Authentication Flow

1. **Login**:
   - User enters email/password on Login page
   - `auth.login()` is called
   - On success: JWT token is stored in `localStorage`
   - User is redirected to home page

2. **Token Storage**:
   - Token stored in `localStorage` under key `token`
   - Token is automatically added to API requests via Axios interceptor

3. **Logout**:
   - Token is removed from `localStorage`
   - User is redirected to login page

4. **Token Expiration**:
   - Backend tokens expire after 60 minutes
   - Frontend automatically redirects to login on 401 errors

## State Management

The application uses **Pinia** (recommended) or **Vuex** for state management:

**Auth Store** (`src/store/auth.js`):
- `user`: Current user object
- `token`: JWT token
- `isAuthenticated`: Boolean flag
- Actions: `login`, `logout`, `checkAuth`

**User Store** (`src/store/user.js`):
- `user`: Detailed user profile
- `loading`: Loading state
- Actions: `fetchUser`, `updateUser`

**Predictions Store** (`src/store/predictions.js`):
- `predictions`: Array of prediction history
- `currentPrediction`: Current prediction being made
- Actions: `createPrediction`, `fetchHistory`

**Favorites Store** (`src/store/favorites.js`):
- `favorites`: Array of favorite teams
- Actions: `addFavorite`, `removeFavorite`, `fetchFavorites`

## Development Workflow

1. **Install dependencies**:
   ```bash
   cd match_prediction_app-front
   npm install
   ```

2. **Run development server**:
   ```bash
   npm run serve
   ```
   Access at: http://localhost:8080

3. **Build for production**:
   ```bash
   npm run build
   ```

4. **Run tests**:
   ```bash
   npm run test:unit
   ```

5. **Lint and fix**:
   ```bash
   npm run lint
   ```

## Testing

### Unit Tests
- Test individual Vue components
- Test utility functions
- Test store actions
- Located in `tests/unit/`

### Component Tests
- Test component rendering
- Test component methods
- Test user interactions
- Located in `tests/unit/components/`

### End-to-End Tests
- Test user flows (login, make prediction, etc.)
- Located in `tests/e2e/`

Run all tests:
```bash
npm run test
```

## UI Components

### Common Components
- **Button**: Reusable button with variants (primary, secondary, danger)
- **Card**: Container with shadow and padding
- **Loader**: Spinner for loading states
- **Modal**: Popup dialog
- **Alert**: Success/error message display

### Domain-Specific Components
- **PredictionForm**: Form for making match predictions
- **PredictionResult**: Display prediction results
- **PredictionList**: List of historical predictions
- **TeamCard**: Display team information
- **TeamSelect**: Dropdown for selecting teams
- **FavoriteButton**: Heart icon for adding/removing favorites

## Styling

The project uses **SCSS** for styling with:
- Variables for colors, spacing, etc. (`src/assets/styles/variables.scss`)
- Mixins for reusable style patterns
- BEM (Block-Element-Modifier) naming convention recommended

Main color scheme (if defined):
```scss
// src/assets/styles/variables.scss
$primary: #3498db;
$secondary: #2ecc71;
$danger: #e74c3c;
$warning: #f39c12;
$info: #9b59b6;
$light: #ecf0f1;
$dark: #2c3e50;
```

## Build Configuration

The `vue.config.js` file contains Vue CLI configuration:

```javascript
// vue.config.js
module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/match-prediction/' : '/',
  outputDir: 'dist',
  assetsDir: 'assets',
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
};
```

## Production Deployment

The frontend is served via **Nginx** in production:

```nginx
# nginx.conf
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Build and serve with Docker:
```bash
docker build -t match-prediction-frontend .
docker run -p 80:80 match-prediction-frontend
```
