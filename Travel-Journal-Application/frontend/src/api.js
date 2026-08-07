import axios from 'axios';

// Use relative paths - Vercel will rewrite to Render backend via vercel.json
// This avoids CORS issues and 405 errors
const api = axios.create({
  baseURL: '', // Empty baseURL means relative paths
  timeout: 20000
});

// Add authorization token to all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
