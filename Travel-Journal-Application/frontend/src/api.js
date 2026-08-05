import axios from 'axios';

// Live Production Render Backend API Base URL
const LIVE_RENDER_BACKEND = 'https://travel-journal-application-ysdk.onrender.com';

let API_URL = import.meta.env.VITE_API_URL;

if (typeof API_URL === 'string' && API_URL.trim() !== '') {
  API_URL = API_URL.trim().replace(/\/+$/, '');
} else {
  // If VITE_API_URL is omitted or empty
  if (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
    API_URL = 'http://localhost:8000';
  } else {
    API_URL = LIVE_RENDER_BACKEND;
  }
}


const api = axios.create({
  baseURL: API_URL,
  timeout: 15000
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
