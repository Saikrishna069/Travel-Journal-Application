import axios from 'axios';

const LIVE_RENDER_BACKEND = 'https://travel-journal-application-ysdk.onrender.com';

let API_URL = import.meta.env.VITE_API_URL;
if (!API_URL || typeof API_URL !== 'string' || API_URL.trim() === '' || API_URL.includes('localhost')) {
  API_URL = LIVE_RENDER_BACKEND;
} else {
  API_URL = API_URL.trim().replace(/\/+$/, '');
}

// Force HTTPS scheme to prevent HTTP->HTTPS 301/302 redirect method downgrades
if (API_URL.startsWith('http://') && !API_URL.includes('localhost')) {
  API_URL = API_URL.replace('http://', 'https://');
}

const api = axios.create({
  baseURL: API_URL,
  timeout: 20000
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
