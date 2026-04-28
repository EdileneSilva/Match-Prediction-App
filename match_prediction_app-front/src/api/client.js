// Configuration directe des APIs backend (localhost car le JavaScript s'exécute dans le navigateur)
const APP_API_BASE_URL = 'http://localhost:8000';  // API Application (auth, users, etc.)
const ML_API_BASE_URL = 'http://localhost:8001';   // API ML (predictions, training)

async function request(endpoint, options = {}) {
  // Récupération dynamique du token
  const token = localStorage.getItem('token');
  
  // Router les requêtes vers les bons services
  let baseUrl;
  let finalEndpoint = endpoint;
  
  // Les endpoints sont déjà corrects, pas besoin de préfixe /api
  if (endpoint.startsWith('/auth') || endpoint.startsWith('/predictions') || endpoint.startsWith('/dashboard')) {
    baseUrl = APP_API_BASE_URL;
  } else if (endpoint.startsWith('/ml') || endpoint.startsWith('/predict')) {
    baseUrl = ML_API_BASE_URL;
  } else {
    // Par défaut, utiliser l'API Application
    baseUrl = APP_API_BASE_URL;
  }

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Ajout du token si présent
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers,
  };

  const response = await fetch(`${baseUrl}${finalEndpoint}`, config);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Une erreur est survenue');
  }

  return response.json();
}

export const apiClient = {
  get: (endpoint) => request(endpoint, { method: 'GET' }),
  post: (endpoint, body) => request(endpoint, { method: 'POST', body: JSON.stringify(body) }),
  put: (endpoint, body) => request(endpoint, { method: 'PUT', body: JSON.stringify(body) }),
  delete: (endpoint) => request(endpoint, { method: 'DELETE' }),
};
