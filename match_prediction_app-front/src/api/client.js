const AUTH_URL = `http://127.0.0.1:8000`;
const ML_URL = `http://127.0.0.1:8001`;

async function request(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  
  // Automagical routing based on endpoint prefix
  const baseUrl = endpoint.startsWith('/auth') ? AUTH_URL : ML_URL;

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

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