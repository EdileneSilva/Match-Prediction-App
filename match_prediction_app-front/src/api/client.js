// Use relative paths - requests will be proxied by nginx or vue-cli-server
// In Docker production: nginx proxies to app-api:8000 and ml-api:8001
// In development: vue-cli-service proxies to localhost:8000 and localhost:8001
const AUTH_URL = '';
const ML_URL = '';

async function request(endpoint, options = {}) {
  // Récupération dynamique du token
  const token = localStorage.getItem('token');
  
  // Automagical routing based on endpoint prefix
  const baseUrl = (endpoint.startsWith('/auth') || endpoint.startsWith('/predictions') || endpoint.startsWith('/dashboard')) ? AUTH_URL : ML_URL;

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

  const response = await fetch(`${baseUrl}${endpoint}`, config);

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
