import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  }
});

export const getItems = () => api.get('/api/items');
export const login = (credentials) => api.post('/login', credentials);
export const logout = () => api.post('/logout');