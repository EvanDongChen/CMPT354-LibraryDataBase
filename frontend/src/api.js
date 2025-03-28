import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

console.log('Initializing API with URL:', API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('=== API Request Debug ===');
    console.log('Request URL:', config.url);
    console.log('Request Method:', config.method);
    console.log('Request Headers:', config.headers);
    console.log('Request Data:', config.data);
    console.log('Request Config:', config);
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('=== API Response Debug ===');
    console.log('Response Status:', response.status);
    console.log('Response Headers:', response.headers);
    console.log('Response Data:', response.data);
    return response;
  },
  (error) => {
    console.error('=== API Error Debug ===');
    console.error('Error Message:', error.message);
    console.error('Error Response:', error.response);
    console.error('Error Request:', error.request);
    console.error('Error Config:', error.config);
    if (error.response) {
      console.error('Error Response Data:', error.response.data);
      console.error('Error Response Status:', error.response.status);
      console.error('Error Response Headers:', error.response.headers);
    }
    return Promise.reject(error);
  }
);

export const getItems = () => api.get('/api/items');
export const login = (credentials) => api.post('/login', credentials);
export const logout = () => api.post('/logout');
export const searchItems = (query) => api.get(`/api/items/search?q=${encodeURIComponent(query)}`);

export const borrowItem = async (memberId, itemId) => {
  try {
    const response = await api.post('/api/items/borrow', {
      member_id: memberId,
      item_id: itemId
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const returnItem = async (itemId) => {
  try {
    const response = await api.post('/api/items/return', { item_id: itemId });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to return item');
  }
};

export const donateItem = async (itemData) => {
  try {
    const response = await api.post('/api/items/donate', itemData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to donate item');
  }
};