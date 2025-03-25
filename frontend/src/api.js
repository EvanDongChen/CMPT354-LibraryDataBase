import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  }
});

export const getItems = () => api.get('/items');
export const login = (credentials) => api.post('/login', credentials);