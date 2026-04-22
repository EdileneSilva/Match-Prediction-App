// Utiliser le proxy nginx pour toutes les requêtes API
const API_BASE_URL = ''; // Vide pour utiliser le domaine courant

async function request(endpoint, options = {}) {
  // Récupération dynamique du token
  const token = localStorage.getItem('token');
  
  // Router les requêtes via le proxy nginx
  let finalEndpoint = endpoint;
  if (endpoint.startsWith('/auth') || endpoint.startsWith('/predictions') || endpoint.startsWith('/dashboard')) {
    finalEndpoint = `/api${endpoint}`;
  } else if (endpoint.startsWith('/ml') || endpoint.startsWith('/predict')) {
    finalEndpoint = `/api-ml${endpoint}`;
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

  const response = await fetch(`${API_BASE_URL}${finalEndpoint}`, config);

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
