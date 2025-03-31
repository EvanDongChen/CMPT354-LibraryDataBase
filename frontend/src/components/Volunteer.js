import React, { useState, useEffect } from 'react';
import { registerVolunteer, getVolunteers } from '../api';

const Volunteer = () => {
  const [formData, setFormData] = useState({
    role: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [volunteers, setVolunteers] = useState([]);

  useEffect(() => {
    loadVolunteers();
  }, []);

  const loadVolunteers = async () => {
    try {
      const response = await getVolunteers();
      setVolunteers(response);
    } catch (error) {
      console.error('Error loading volunteers:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user.people_id) {
      setError('You must be logged in to register as a volunteer');
      return;
    }

    try {
      await registerVolunteer({
        people_id: user.people_id,
        role: formData.role
      });
      setSuccess('Successfully registered as a volunteer!');
      setFormData({ role: '' });
      loadVolunteers();
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="volunteer-container">
      <h2>Volunteer Registration</h2>
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="role">Volunteer Role:</label>
          <select
            id="role"
            value={formData.role}
            onChange={(e) => setFormData({ ...formData, role: e.target.value })}
            required
          >
            <option value="">Select a role</option>
            <option value="Book Shelver">Book Shelver</option>
            <option value="Event Helper">Event Helper</option>
            <option value="Program Assistant">Program Assistant</option>
            <option value="Library Guide">Library Guide</option>
            <option value="Administrative Support">Administrative Support</option>
          </select>
        </div>
        <button type="submit" className="submit-button">Register as Volunteer</button>
      </form>

      <div className="volunteers-list">
        <h3>Current Volunteers</h3>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Role</th>
              <th>Status</th>
              <th>Join Date</th>
            </tr>
          </thead>
          <tbody>
            {volunteers.map((volunteer) => (
              <tr key={volunteer.volunteer_id}>
                <td>{volunteer.name}</td>
                <td>{volunteer.role}</td>
                <td>{volunteer.status}</td>
                <td>{volunteer.join_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Volunteer; 