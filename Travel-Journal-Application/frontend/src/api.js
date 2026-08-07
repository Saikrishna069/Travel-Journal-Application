import axios from 'axios';

// Initialize axios instance with relative baseURL
// Vercel will rewrite /auth, /journals, /expenses, /ai, /planner to backend via vercel.json
const api = axios.create({
  baseURL: '/', // Use root-relative path
  timeout: 20000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor: Add auth token to all requests
api.interceptors.request.use(
  (config) => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error reading token from localStorage:', error);
    }
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor: Handle errors globally
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', {
      status: error.response?.status,
      message: error.message,
      url: error.config?.url,
      method: error.config?.method
    });
    return Promise.reject(error);
  }
);

export default api;
