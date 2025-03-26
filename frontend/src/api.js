import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true
});

export const getItems = () => api.get('/api/items');
export const login = (credentials) => api.post('/login', credentials);
export const logout = () => api.post('/logout');
export const searchItems = (query) => api.get(`/api/items/search?q=${encodeURIComponent(query)}`);

export const borrowItem = async (memberId, itemId) => {
  console.log('=== Borrow Request Debug ===');
  console.log('Request Data:', { member_id: memberId, item_id: itemId });
  console.log('User Data:', localStorage.getItem('user'));
  
  try {
    console.log('Making API request...');
    const response = await api.post('/api/items/borrow', {
      member_id: memberId,
      item_id: itemId
    });
    console.log('API Response:', response.data);
    console.log('Response Headers:', response.headers);
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    console.error('Error Response:', error.response?.data);
    console.error('Error Status:', error.response?.status);
    console.error('Error Headers:', error.response?.headers);
    throw error.response?.data || error.message;
  }
};

export const returnItem = async (itemId) => {
  try {
    console.log('Attempting to return item:', itemId);
    const response = await api.post('/api/items/return', { item_id: itemId });
    console.log('Return response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Return error:', error);
    console.error('Error response:', error.response?.data);
    throw new Error(error.response?.data?.error || 'Failed to return item');
  }
};