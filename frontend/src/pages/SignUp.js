import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser } from '../api';

function Signup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    phone: '',
    email: '',
    wantsToBecomeMember: false
  });
  const [message, setMessage] = useState({ type: '', text: '' });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await registerUser(formData);
      setMessage({ type: 'success', text: 'Registration successful!' });
      localStorage.setItem('user', JSON.stringify(response.data));
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (error) {
      setMessage({ type: 'error', text: error.message || 'Registration failed' });
    }
  };

  return (
    <div className="signup-container">
      <h2>Sign Up</h2>
      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>First Name:</label>
          <input
            type="text"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Last Name:</label>
          <input
            type="text"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Phone:</label>
          <input
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>
            <input
              type="checkbox"
              name="wantsToBecomeMember"
              checked={formData.wantsToBecomeMember}
              onChange={handleChange}
            />
            I want to become a library member (required to borrow items)
          </label>
        </div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default Signup; 