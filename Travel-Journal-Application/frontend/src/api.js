import axios from 'axios';

let API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
// Sanitize URL: Remove any trailing slashes to avoid //auth/register 404 errors
API_URL = API_URL.trim().replace(/\/+$/, '');

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
