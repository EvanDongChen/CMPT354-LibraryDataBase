import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api';

function Login({ onLogin }) {
  const [formData, setFormData] = useState({
    people_id: '',
    phone: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      const response = await login(formData);
      console.log('Login response:', response.data);  // Debug log
      
      if (response.data.success) {
        // Store the complete user data
        const userData = {
          ...response.data,
          member_id: response.data.member_id  // Ensure member_id is included
        };
        console.log('Storing user data:', userData);  // Debug log
        onLogin(userData);
        navigate('/home', { replace: true });
      } else {
        setError(response.data.message || 'Invalid credentials. Please try again.');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('An error occurred during login. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-header">
        <img 
          src="/images/library-logo.png" 
          alt="Library Logo" 
          className="login-logo"
        />
      </div>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>User ID</label>
          <input
            type="text"
            value={formData.people_id}
            onChange={(e) => setFormData({...formData, people_id: e.target.value})}
            required
          />
        </div>
        <div className="form-group">
          <label>Phone Number</label>
          <input
            type="text"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;