import React, { useEffect, useState } from 'react';
import { getItems, searchItems, borrowItem, returnItem, donateItem, getEvents, registerForEvent, getEmployees, getQuestions, createQuestion, registerVolunteer, getVolunteers } from '../api';
import { useLocation } from 'react-router-dom';

function Home() {
  const [items, setItems] = useState([]);
  const [user, setUser] = useState(null);
  const [activeSection, setActiveSection] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [borrowMessage, setBorrowMessage] = useState({ type: '', text: '' });
  const [returnMessage, setReturnMessage] = useState({ type: '', text: '' });
  const [donateForm, setDonateForm] = useState({
    title: '',
    author: '',
    publication_year: '',
    type: 'Book',
    url: ''
  });
  const [donateMessage, setDonateMessage] = useState({ type: '', text: '' });
  const [events, setEvents] = useState([]);
  const [eventMessage, setEventMessage] = useState({ type: '', text: '' });
  const [employees, setEmployees] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState('');
  const [newQuestion, setNewQuestion] = useState('');
  const [questionMessage, setQuestionMessage] = useState({ type: '', text: '' });
  const [volunteerForm, setVolunteerForm] = useState({
    role: ''
  });
  const [volunteerMessage, setVolunteerMessage] = useState({ type: '', text: '' });
  const [volunteers, setVolunteers] = useState([]);
  const location = useLocation();

  useEffect(() => {
    // Get user data from localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }

    // Fetch all items on initial load
    const fetchData = async () => {
      try {
        const [itemsRes, eventsRes, volunteersRes] = await Promise.all([
          getItems(),
          getEvents(user?.people_id),
          getVolunteers()
        ]);
        setItems(itemsRes.data);
        setEvents(eventsRes.data);
        setVolunteers(volunteersRes.data);
      } catch (err) {
        // Silent fail
      }
    };
    fetchData();

    // Update search state from navigation
    if (location.state?.isSearching) {
      setSearchResults(location.state.searchResults);
      setSearchQuery(location.state.searchQuery);
    } else {
      setSearchResults([]);
      setSearchQuery('');
    }

    // Fetch employees for contact section
    const fetchEmployees = async () => {
      try {
        const res = await getEmployees();
        setEmployees(res.data);
      } catch (err) {
        // Silent fail
      }
    };

    // Fetch user's questions if logged in
    const fetchQuestions = async () => {
      if (user?.people_id) {
        try {
          const res = await getQuestions(user.people_id);
          setQuestions(res.data);
        } catch (err) {
          // Silent fail
        }
      }
    };

    fetchEmployees();
    fetchQuestions();
  }, [location.state, user?.people_id]); // Update when location state or user changes

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      return; // Do nothing if search is empty
    }

    try {
      const res = await searchItems(searchQuery);
      setSearchResults(res.data);
    } catch (err) {
      // Silent fail
    }
  };

  const handleShowAll = () => {
    setSearchResults([]);
    setSearchQuery('');
  };

  const handleNavClick = (section) => {
    setActiveSection(activeSection === section ? null : section);
  };

  const handleBorrow = async (itemId) => {
    if (!user) {
      setBorrowMessage({ type: 'error', text: 'Please log in to borrow items' });
      return;
    }

    try {
      const result = await borrowItem(user.member_id, itemId);
      setBorrowMessage({ type: 'success', text: `Item borrowed successfully! Due date: ${result.due_date}` });
      
      // Refresh the items list
      const res = await getItems();
      setItems(res.data);
      
      // If we're showing search results, refresh those too
      if (searchQuery) {
        const searchRes = await searchItems(searchQuery);
        setSearchResults(searchRes.data);
      }

      // Clear message after 3 seconds
      setTimeout(() => {
        setBorrowMessage({ type: '', text: '' });
      }, 3000);
    } catch (error) {
      setBorrowMessage({ type: 'error', text: error.message || 'Failed to borrow item' });
      // Clear error message after 3 seconds
      setTimeout(() => {
        setBorrowMessage({ type: '', text: '' });
      }, 3000);
    }
  };

  const handleReturn = async (itemId) => {
    if (!user) {
      setReturnMessage({ type: 'error', text: 'Please log in to return items' });
      return;
    }

    try {
      await returnItem(itemId);
      setReturnMessage({ type: 'success', text: 'Item returned successfully!' });
      
      // Refresh the items list
      const res = await getItems();
      setItems(res.data);
      
      // If we're showing search results, refresh those too
      if (searchQuery) {
        const searchRes = await searchItems(searchQuery);
        setSearchResults(searchRes.data);
      }

      // Clear message after 3 seconds
      setTimeout(() => {
        setReturnMessage({ type: '', text: '' });
      }, 3000);
    } catch (error) {
      setReturnMessage({ type: 'error', text: error.message || 'Failed to return item' });
      // Clear error message after 3 seconds
      setTimeout(() => {
        setReturnMessage({ type: '', text: '' });
      }, 3000);
    }
  };

  const handleDonateSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      setDonateMessage({ type: 'error', text: 'Please log in to donate items' });
      return;
    }

    try {
      await donateItem(donateForm);
      setDonateMessage({ type: 'success', text: 'Item donated successfully!' });
      
      // Reset form
      setDonateForm({
        title: '',
        author: '',
        publication_year: '',
        type: 'Book',
        url: ''
      });

      // Refresh the items list
      const res = await getItems();
      setItems(res.data);

      // Clear message after 3 seconds
      setTimeout(() => {
        setDonateMessage({ type: '', text: '' });
      }, 3000);
    } catch (error) {
      setDonateMessage({ type: 'error', text: error.message || 'Failed to donate item' });
      // Clear error message after 3 seconds
      setTimeout(() => {
        setDonateMessage({ type: '', text: '' });
      }, 3000);
    }
  };

  const handleDonateFormChange = (e) => {
    const { name, value } = e.target;
    setDonateForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleEventRegistration = async (eventId) => {
    if (!user) {
      // Show non-member registration form
      const firstName = prompt('Please enter your first name:');
      if (!firstName) return;
      
      const lastName = prompt('Please enter your last name:');
      if (!lastName) return;
      
      const phone = prompt('Please enter your phone number:');
      if (!phone) return;
      
      const email = prompt('Please enter your email:');
      if (!email) return;

      try {
        await registerForEvent({
          event_id: eventId,
          is_new_registration: true,
          first_name: firstName,
          last_name: lastName,
          phone: phone,
          email: email
        });
        
        setEventMessage({ type: 'success', text: 'Successfully registered for event!' });
        
        // Refresh events list
        const res = await getEvents();
        setEvents(res.data);
      } catch (error) {
        setEventMessage({ type: 'error', text: error.response?.data?.error || 'Failed to register for event' });
      }
      return;
    }

    try {
      await registerForEvent({
        event_id: eventId,
        people_id: user.people_id
      });
      setEventMessage({ type: 'success', text: 'Successfully registered for event!' });
      
      // Refresh events list with updated registration status
      const res = await getEvents(user.people_id);
      setEvents(res.data);

      setTimeout(() => {
        setEventMessage({ type: '', text: '' });
      }, 3000);
    } catch (error) {
      if (error.response?.data?.error === 'Already registered for this event') {
        setEventMessage({ type: 'success', text: 'Already registered for this event!' });
        const res = await getEvents(user.people_id);
        setEvents(res.data);
      } else {
        setEventMessage({ type: 'error', text: error.response?.data?.error || 'Failed to register for event' });
      }
      setTimeout(() => {
        setEventMessage({ type: '', text: '' });
      }, 3000);
    }
  };

  const handleQuestionSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      setQuestionMessage({ type: 'error', text: 'Please log in to submit questions' });
      return;
    }

    if (!newQuestion.trim()) {
      setQuestionMessage({ type: 'error', text: 'Please enter a question' });
      return;
    }

    try {
      await createQuestion(user.people_id, newQuestion);
      setQuestionMessage({ type: 'success', text: 'Question submitted successfully!' });
      
      // Refresh questions
      const res = await getQuestions(user.people_id);
      setQuestions(res.data);
      
      // Reset form
      setNewQuestion('');
      setSelectedEmployee('');

      // Clear message after 3 seconds
      setTimeout(() => {
        setQuestionMessage({ type: '', text: '' });
      }, 3000);
    } catch (error) {
      setQuestionMessage({ type: 'error', text: error.message || 'Failed to submit question' });
      setTimeout(() => {
        setQuestionMessage({ type: '', text: '' });
      }, 3000);
    }
  };

  const handleVolunteerSubmit = async (e) => {
    e.preventDefault();
    
    if (!user) {
      alert("Please login to register as a volunteer");
      return;
    }
    
    try {
      const response = await registerVolunteer(user.people_id, volunteerForm.role);
      
      if (response.data.success) {
        setVolunteerMessage({
          type: 'success',
          text: 'Thank you for registering as a volunteer! A staff member will contact you shortly.'
        });
        
        // Reset the form
        setVolunteerForm({ role: 'Book Shelver' });
        
        // Clear success message after 5 seconds
        setTimeout(() => {
          setVolunteerMessage({ type: '', text: '' });
        }, 5000);
      }
    } catch (error) {
      setVolunteerMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to register as a volunteer. Please try again.'
      });
      setTimeout(() => {
        setVolunteerMessage({ type: '', text: '' });
      }, 5000);
    }
  };

  const handleVolunteerFormChange = (e) => {
    const { name, value } = e.target;
    setVolunteerForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="home-container">
      {/* Navigation Bar */}
      <div className="nav-bar">
        <button 
          className={`nav-button ${activeSection === null ? 'active' : ''}`}
          onClick={() => handleNavClick(null)}
        >
          Home
        </button>
        <button 
          className={`nav-button ${activeSection === 'return' ? 'active' : ''}`}
          onClick={() => handleNavClick('return')}
        >
          Return
        </button>
        <button 
          className={`nav-button ${activeSection === 'donate' ? 'active' : ''}`}
          onClick={() => handleNavClick('donate')}
        >
          Donate
        </button>
        <button 
          className={`nav-button ${activeSection === 'events' ? 'active' : ''}`}
          onClick={() => handleNavClick('events')}
        >
          Events
        </button>
        <button 
          className={`nav-button ${activeSection === 'contact' ? 'active' : ''}`}
          onClick={() => handleNavClick('contact')}
        >
          Contact
        </button>
        <button 
          className={`nav-button ${activeSection === 'volunteer' ? 'active' : ''}`}
          onClick={() => handleNavClick('volunteer')}
        >
          Volunteer
        </button>
      </div>

      {/* Dynamic Sections */}
      <div className="section-container">
        {activeSection === 'borrow' && (
          <div className="section borrow-section">
            <h2>Borrow Items</h2>
            <div className="available-items">
              <h3>Available Items</h3>
              <ul>
                {items.filter(item => item.Status === 'Available').map(item => (
                  <li key={item.ItemID}>
                    <strong>{item.Title}</strong> by {item.Author}
                    <button className="borrow-button">Borrow</button>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {activeSection === 'return' && (
          <div className="section return-section">
            <h2>Return Items</h2>
            {returnMessage.text && (
              <div className={`message ${returnMessage.type}`}>
                {returnMessage.text}
              </div>
            )}
            <div className="borrowed-items" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
              <h3>Your Borrowed Items</h3>
              {console.log('All items:', items)}
              {console.log('Checked out items:', items.filter(item => item.Status === 'CheckedOut' && item.CanReturn))}
              <ul style={{ width: '100%', maxWidth: '800px', margin: '0 auto', padding: '0' }}>
                {items.filter(item => item.Status === 'CheckedOut' && item.CanReturn).map(item => (
                  <li key={item.ItemID} className="item-card">
                    <div className="content-wrapper">
                      <img src="/images/book.png" alt="Book cover" />
                      <h3>{item.Title}</h3>
                    </div>
                    <div className="item-details">
                      <p><strong>Author:</strong> {item.Author}</p>
                      <p><strong>Type:</strong> {item.Type}</p>
                      <p><strong>Due Date:</strong> {item.DueDate || 'Not set'}</p>
                      <button 
                        className="return-button"
                        onClick={() => handleReturn(item.ItemID)}
                      >
                        Return
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
              {items.filter(item => item.Status === 'CheckedOut' && item.CanReturn).length === 0 && (
                <p>You don't have any items checked out.</p>
              )}
            </div>
          </div>
        )}

        {activeSection === 'donate' && (
          <div className="section donate-section">
            <h2>Donate Items</h2>
            {donateMessage.text && (
              <div className={`message ${donateMessage.type}`}>
                {donateMessage.text}
              </div>
            )}
            <form className="donate-form" onSubmit={handleDonateSubmit}>
              <div className="form-group">
                <label>Item Title:</label>
                <input 
                  type="text" 
                  name="title"
                  value={donateForm.title}
                  onChange={handleDonateFormChange}
                  placeholder="Enter item title" 
                  required
                  style={{ fontFamily: 'Times New Roman, Times, serif' }}
                />
              </div>
              <div className="form-group">
                <label>Author:</label>
                <input 
                  type="text" 
                  name="author"
                  value={donateForm.author}
                  onChange={handleDonateFormChange}
                  placeholder="Enter author name" 
                  required
                  style={{ fontFamily: 'Times New Roman, Times, serif' }}
                />
              </div>
              <div className="form-group">
                <label>Publication Year:</label>
                <input 
                  type="number" 
                  name="publication_year"
                  value={donateForm.publication_year}
                  onChange={handleDonateFormChange}
                  placeholder="Enter publication year" 
                  required
                  style={{ fontFamily: 'Times New Roman, Times, serif' }}
                />
              </div>
              <div className="form-group">
                <label>Item Type:</label>
                <select 
                  name="type"
                  value={donateForm.type}
                  onChange={handleDonateFormChange}
                  required
                  style={{ fontFamily: 'Times New Roman, Times, serif' }}
                >
                  <option value="Book">Book</option>
                  <option value="Magazine">Magazine</option>
                  <option value="Scientific Journal">Scientific Journal</option>
                  <option value="CD">CD</option>
                  <option value="Record">Record</option>
                </select>
              </div>
              <div className="form-group">
                <label>URL (Optional - for digital items):</label>
                <input 
                  type="url" 
                  name="url"
                  value={donateForm.url}
                  onChange={handleDonateFormChange}
                  placeholder="Enter digital item URL" 
                  style={{ fontFamily: 'Times New Roman, Times, serif' }}
                />
              </div>
              <button 
                type="submit" 
                className="submit-button" 
                style={{ 
                  backgroundColor: '#4f583d', 
                  color: 'white',
                  fontFamily: 'Times New Roman, Times, serif'
                }}
              >
                Submit Donation
              </button>
            </form>
          </div>
        )}

        {activeSection === 'events' && (
          <div className="section events-section">
            <h2>Library Events</h2>
            {eventMessage.text && (
              <div className={`message ${eventMessage.type}`}>
                {eventMessage.text}
              </div>
            )}
            <div className="events-list">
              {events.map((event) => (
                <div key={event.EventID} className="event-card" style={{ fontFamily: 'Times New Roman, Times, serif' }}>
                  <h3 style={{ color: '#4f583d' }}>{event.EventName}</h3>
                  <p><strong>Type:</strong> {event.Type}</p>
                  <p><strong>Date:</strong> {new Date(event.EventDate).toLocaleString()}</p>
                  <p><strong>Location:</strong> {event.Location}</p>
                  <p><strong>Capacity:</strong> {event.Capacity}</p>
                  <p><strong>Audience:</strong> {event.Audience}</p>
                  {user ? (
                    <button
                      onClick={() => handleEventRegistration(event.EventID)}
                      className={`register-button ${event.IsRegistered ? 'registered' : ''}`}
                      disabled={event.IsRegistered}
                      style={{ 
                        backgroundColor: event.IsRegistered ? '#8fa6ac' : '#4f583d',
                        color: 'white',
                        fontFamily: 'Times New Roman, Times, serif'
                      }}
                    >
                      {event.IsRegistered ? 'Already Registered' : 'Register'}
                    </button>
                  ) : (
                    <button
                      onClick={() => alert('Please log in to register for events')}
                      className="register-button"
                      style={{ 
                        backgroundColor: '#4f583d',
                        color: 'white',
                        fontFamily: 'Times New Roman, Times, serif'
                      }}
                    >
                      Register
                    </button>
                  )}
                </div>
              ))}
              {events.length === 0 && (
                <p>No upcoming events at the moment.</p>
              )}
            </div>
          </div>
        )}

        {activeSection === 'contact' && (
          <div className="section contact-section">
            <h2>Contact Us</h2>
            <div className="contact-info">
              <div className="contact-card" style={{ fontFamily: 'Times New Roman, Times, serif' }}>
                <h3 style={{ color: '#4f583d' }}>📞 Phone</h3>
                <p>(555) 123-4567</p>
              </div>
              <div className="contact-card" style={{ fontFamily: 'Times New Roman, Times, serif' }}>
                <h3 style={{ color: '#4f583d' }}>📧 Email</h3>
                <p>library@example.com</p>
              </div>
              <div className="contact-card" style={{ fontFamily: 'Times New Roman, Times, serif' }}>
                <h3 style={{ color: '#4f583d' }}>📍 Address</h3>
                <p>123 Library Street<br />City, State 12345</p>
              </div>
            </div>

            <div className="questions-section" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
              <h3 style={{ color: '#4f583d', fontFamily: 'Times New Roman, Times, serif' }}>Ask a Question</h3>
              {questionMessage.text && (
                <div className={`message ${questionMessage.type}`}>
                  {questionMessage.text}
                </div>
              )}
              
              {user ? (
                <>
                  <form className="question-form" onSubmit={handleQuestionSubmit} style={{ width: '100%', maxWidth: '600px' }}>
                    <div className="form-group">
                      <label>Select Staff Member:</label>
                      <select 
                        value={selectedEmployee}
                        onChange={(e) => setSelectedEmployee(e.target.value)}
                        style={{ fontFamily: 'Times New Roman, Times, serif' }}
                      >
                        <option value="">Select an employee</option>
                        {employees.map(emp => (
                          <option key={emp.employee_id} value={emp.employee_id}>
                            {emp.name} - {emp.position}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="form-group">
                      <label>Your Question:</label>
                      <textarea
                        value={newQuestion}
                        onChange={(e) => setNewQuestion(e.target.value)}
                        placeholder="Type your question here..."
                        required
                        style={{ fontFamily: 'Times New Roman, Times, serif' }}
                      />
                    </div>
                    <button 
                      type="submit" 
                      className="submit-button"
                      style={{ 
                        backgroundColor: '#4f583d',
                        color: 'white',
                        fontFamily: 'Times New Roman, Times, serif'
                      }}
                    >
                      Submit Question
                    </button>
                  </form>

                  <div className="previous-questions" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
                    <h3 style={{ color: '#4f583d', fontFamily: 'Times New Roman, Times, serif' }}>Your Previous Questions</h3>
                    {questions.length > 0 ? (
                      <ul className="questions-list" style={{ width: '100%', maxWidth: '600px', margin: '0 auto', padding: '0' }}>
                        {questions.map(q => (
                          <li key={q.request_id} className="question-item" style={{ fontFamily: 'Times New Roman, Times, serif' }}>
                            <div className="question">
                              <strong style={{ color: '#4f583d' }}>Q:</strong> {q.question}
                            </div>
                            {q.answer && (
                              <div className="answer">
                                <strong style={{ color: '#4f583d' }}>A:</strong> {q.answer}
                              </div>
                            )}
                            {!q.answer && (
                              <div className="pending">
                                Awaiting response...
                              </div>
                            )}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p>You haven't asked any questions yet.</p>
                    )}
                  </div>
                </>
              ) : (
                <p>Please log in to ask questions and view your previous inquiries.</p>
              )}
            </div>
          </div>
        )}

        {activeSection === 'volunteer' && (
          <div className="section volunteer-section">
            <h2>Volunteer Opportunities</h2>
            <p>Join our library volunteer team and make a difference in your community!</p>
            
            {volunteerMessage.text && (
              <div className={`message ${volunteerMessage.type}`}>
                {volunteerMessage.text}
              </div>
            )}
            
            {user ? (
              <form onSubmit={handleVolunteerSubmit}>
                <div className="form-group">
                  <label>Role:</label>
                  <select 
                    name="role"
                    value={volunteerForm.role}
                    onChange={handleVolunteerFormChange}
                    required
                    style={{ fontFamily: 'Times New Roman, Times, serif' }}
                  >
                    <option value="">Select a role</option>
                    <option value="Book Shelver">Book Shelver</option>
                    <option value="Event Helper">Event Helper</option>
                    <option value="Program Assistant">Program Assistant</option>
                    <option value="Technology Tutor">Technology Tutor</option>
                  </select>
                </div>
                <button 
                  type="submit" 
                  className="submit-button" 
                  style={{ 
                    backgroundColor: '#4f583d', 
                    color: 'white',
                    fontFamily: 'Times New Roman, Times, serif'
                  }}
                >
                  Register as Volunteer
                </button>
              </form>
            ) : (
              <p>Please login to register as a volunteer.</p>
            )}
            
            <div className="volunteers-list">
              <h3>Our Current Volunteers</h3>
              {volunteers.length > 0 ? (
                <ul className="volunteer-cards">
                  {volunteers.map(volunteer => (
                    <li key={volunteer.volunteer_id} className="volunteer-card">
                      <h4 style={{ color: '#4f583d' }}>{volunteer.name}</h4>
                      <p><strong>Role:</strong> {volunteer.role}</p>
                      <p><strong>Contact:</strong> {volunteer.email}</p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No volunteers registered yet. Be the first one!</p>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="main-content">
        {borrowMessage.text && (
          <div className={`message ${borrowMessage.type}`}>
            {borrowMessage.text}
          </div>
        )}
        {searchResults.length > 0 ? (
          <>
            <h2>Search Results for "{searchQuery}"</h2>
            <div className="search-results">
              {searchResults.map((item) => (
                <div key={item.ItemID} className="item-card">
                  <div className="content-wrapper">
                    <img src="/images/book.png" alt="Book cover" />
                    <h3>{item.Title}</h3>
                  </div>
                  <div className="item-details">
                    <p><strong>Author:</strong> {item.Author}</p>
                    <p><strong>Type:</strong> {item.Type}</p>
                    <p><strong>Status:</strong> {item.Status === 'Available' ? '✅' : '❌'}</p>
                    {item.Status === 'CheckedOut' && item.DueDate && (
                      <p><strong>Due Date:</strong> {item.DueDate}</p>
                    )}
                    {item.Status === 'Available' ? (
                      <button 
                        className="borrow-button"
                        onClick={() => handleBorrow(item.ItemID)}
                      >
                        Borrow
                      </button>
                    ) : (
                      <button 
                        className="return-button"
                        onClick={() => handleReturn(item.ItemID)}
                      >
                        Return
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : searchQuery ? (
          <div className="no-results">
            <p>No items found matching your search "{searchQuery}"</p>
          </div>
        ) : (
          <>
            <h2>Library Items</h2>
            <div className="items-grid">
              {items.map((item) => (
                <div key={item.ItemID} className="item-card">
                  <h3>{item.Title}</h3>
                  <p><strong>Author:</strong> {item.Author}</p>
                  <p><strong>Type:</strong> {item.Type}</p>
                  <p><strong>Year:</strong> {item.PublicationYear}</p>
                  <p><strong>Status:</strong> {item.Status}</p>
                  {item.DueDate && (
                    <p><strong>Due Date:</strong> {item.DueDate}</p>
                  )}
                  {user ? (
                    <div className="item-actions">
                      {item.Status === 'Available' && (
                        <button
                          onClick={() => handleBorrow(item.ItemID)}
                          className="borrow-button"
                        >
                          Borrow
                        </button>
                      )}
                      {item.Status === 'CheckedOut' && item.CanReturn && (
                        <button
                          onClick={() => handleReturn(item.ItemID)}
                          className="return-button"
                        >
                          Return
                        </button>
                      )}
                    </div>
                  ) : (
                    <p className="login-prompt">Please log in to borrow items</p>
                  )}
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Home;