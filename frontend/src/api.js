import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

console.log('Initializing API with URL:', API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true,
  credentials: 'include'
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

export const getItems = () => {
  const user = JSON.parse(localStorage.getItem('user'));
  return api.get(`/api/items${user ? `?member_id=${user.member_id}` : ''}`);
};

export const login = (credentials) => api.post('/login', credentials);
export const logout = () => api.post('/logout');
export const searchItems = (query) => {
  const user = JSON.parse(localStorage.getItem('user'));
  return api.get(`/api/items/search?q=${query}${user ? `&member_id=${user.member_id}` : ''}`);
};

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

export const returnItem = (item_id) => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (!user || !user.member_id) {
    throw new Error('You must be logged in as a member to return items');
  }
  return api.post('/api/items/return', { 
    item_id,
    member_id: user.member_id
  });
};

export const donateItem = async (itemData) => {
  try {
    const response = await api.post('/api/items/donate', itemData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to donate item');
  }
};

export const getEvents = (peopleId) => api.get(`/api/events${peopleId ? `?people_id=${peopleId}` : ''}`);

export const registerForEvent = async (eventData) => {
  try {
    const response = await api.post('/api/events/register', eventData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to register for event');
  }
};

export const getEmployees = () => {
  return api.get('/api/employees');
};

export const getQuestions = (people_id) => {
  return api.get(`/api/questions?people_id=${people_id}`);
};

export const createQuestion = (people_id, question) => {
  return api.post('/api/questions', {
    people_id,
    question
  });
};

export const register = (userData) => {
  console.log('Registering user with data:', userData);
  return api.post('/api/register', userData, {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    withCredentials: true,
    credentials: 'include'
  });
};

export const registerVolunteer = async (volunteerData) => {
  try {
    const response = await api.post('/api/volunteer/register', volunteerData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to register as volunteer');
  }
};

export const getVolunteers = () => {
  return api.get('/api/volunteers');
};