import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true,
  credentials: 'include'
});

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
    return await api.post('/api/events/register', eventData);
  } catch (error) {
    throw error;
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
  return api.post('/api/register', userData, {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    withCredentials: true,
    credentials: 'include'
  });
};

export const registerVolunteer = async (peopleId, role) => {
  try {
    return await api.post('/api/volunteer/register', { people_id: peopleId, role });
  } catch (error) {
    throw error;
  }
};

export const getVolunteers = async () => {
  try {
    return await api.get('/api/volunteers');
  } catch (error) {
    throw error;
  }
};