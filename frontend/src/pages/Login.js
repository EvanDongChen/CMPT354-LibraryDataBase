import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, getEvents, registerForEvent } from '../api';

function Login({ onLogin }) {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('login');
  const [credentials, setCredentials] = useState({
    member_id: '',
    phone: ''
  });
  const [error, setError] = useState('');
  const [events, setEvents] = useState([]);
  const [eventMessage, setEventMessage] = useState({ type: '', text: '' });
  const [registrationForms, setRegistrationForms] = useState({});

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await getEvents();
        setEvents(response.data);
        
        // Initialize an empty form for each event
        const initialForms = {};
        response.data.forEach(event => {
          initialForms[event.EventID] = {
            first_name: '',
            last_name: '',
            phone: '',
            email: ''
          };
        });
        setRegistrationForms(initialForms);
      } catch (err) {
        // Silent fail - events will be empty array
      }
    };
    fetchEvents();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await login(credentials);
      if (response.data.success) {
        onLogin(response.data);
        navigate('/home');
      } else {
        setError('Invalid credentials');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleRegistrationChange = (eventId, e) => {
    const { name, value } = e.target;
    setRegistrationForms(prev => ({
      ...prev,
      [eventId]: {
        ...prev[eventId],
        [name]: value
      }
    }));
  };

  const handleEventRegistration = async (eventId) => {
    try {
      await registerForEvent({
        event_id: eventId,
        is_new_registration: true,
        ...registrationForms[eventId]
      });
      
      // API returns the response directly, not wrapped in response.data
      setEventMessage({ 
        type: 'success', 
        text: 'Successfully registered for this event! You will receive a confirmation email shortly.' 
      });
      
      // Refresh events list
      const eventsResponse = await getEvents();
      setEvents(eventsResponse.data);
      
      // Reset form for this specific event
      setRegistrationForms(prev => ({
        ...prev,
        [eventId]: {
          first_name: '',
          last_name: '',
          phone: '',
          email: ''
        }
      }));

      // Clear success message after 5 seconds
      setTimeout(() => {
        setEventMessage({ type: '', text: '' });
      }, 5000);
    } catch (error) {
      setEventMessage({ 
        type: 'error', 
        text: error.response?.data?.error || 'Failed to register for event. Please try again.' 
      });
      setTimeout(() => {
        setEventMessage({ type: '', text: '' });
      }, 5000);
    }
  };

  return (
    <div className="login-container">
      <div className="login-header">
        <img src="/images/library-logo-ver2.png" alt="Library Logo" className="login-logo" />
      </div>
      
      <div className="tab-buttons">
        <button 
          className={`tab-button ${activeTab === 'login' ? 'active' : ''}`}
          onClick={() => setActiveTab('login')}
        >
          Member Login
        </button>
        <button 
          className={`tab-button ${activeTab === 'events' ? 'active' : ''}`}
          onClick={() => setActiveTab('events')}
        >
          Events
        </button>
      </div>

      {activeTab === 'login' ? (
        <>
          <h2>Member Login</h2>
          {error && <div className="error-message">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Member ID:</label>
              <input
                type="text"
                name="member_id"
                value={credentials.member_id}
                onChange={handleChange}
                placeholder="Enter your Member ID"
                required
              />
            </div>
            <div className="form-group">
              <label>Phone Number:</label>
              <input
                type="text"
                name="phone"
                value={credentials.phone}
                onChange={handleChange}
                placeholder="Enter your phone number"
                required
              />
            </div>
            <button type="submit">Login</button>
          </form>
        </>
      ) : (
        <>
          <h2>Library Events</h2>
          {eventMessage.text && (
            <div className={`message ${eventMessage.type}`}>
              {eventMessage.text}
            </div>
          )}
          <div className="events-list">
            {events.map((event) => (
              <div key={event.EventID} className="event-card">
                <h3>{event.EventName}</h3>
                <p><strong>Type:</strong> {event.Type}</p>
                <p><strong>Date:</strong> {new Date(event.EventDate).toLocaleString()}</p>
                <p><strong>Location:</strong> {event.Location}</p>
                <p><strong>Capacity:</strong> {event.Capacity}</p>
                <p><strong>Audience:</strong> {event.Audience}</p>
                <form onSubmit={(e) => {
                  e.preventDefault();
                  handleEventRegistration(event.EventID);
                }}>
                  <div className="form-group">
                    <label>First Name:</label>
                    <input
                      type="text"
                      name="first_name"
                      value={registrationForms[event.EventID]?.first_name || ''}
                      onChange={(e) => handleRegistrationChange(event.EventID, e)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Last Name:</label>
                    <input
                      type="text"
                      name="last_name"
                      value={registrationForms[event.EventID]?.last_name || ''}
                      onChange={(e) => handleRegistrationChange(event.EventID, e)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Phone:</label>
                    <input
                      type="tel"
                      name="phone"
                      value={registrationForms[event.EventID]?.phone || ''}
                      onChange={(e) => handleRegistrationChange(event.EventID, e)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Email:</label>
                    <input
                      type="email"
                      name="email"
                      value={registrationForms[event.EventID]?.email || ''}
                      onChange={(e) => handleRegistrationChange(event.EventID, e)}
                      required
                    />
                  </div>
                  <button type="submit" className="register-button">Register for Event</button>
                </form>
              </div>
            ))}
            {events.length === 0 && (
              <p>No upcoming events at the moment.</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default Login;