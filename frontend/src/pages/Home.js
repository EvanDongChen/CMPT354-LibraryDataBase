import React, { useEffect, useState } from 'react';
import { getItems, searchItems } from '../api';
import { useLocation } from 'react-router-dom';

function Home() {
  const [items, setItems] = useState([]);
  const [user, setUser] = useState(null);
  const [activeSection, setActiveSection] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
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
        const res = await getItems();
        setItems(res.data);
      } catch (err) {
        console.error('Error fetching items:', err);
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
  }, [location.state]); // Update when location state changes

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      return; // Do nothing if search is empty
    }

    try {
      const res = await searchItems(searchQuery);
      setSearchResults(res.data);
    } catch (err) {
      console.error('Error searching items:', err);
    }
  };

  const handleShowAll = () => {
    setSearchResults([]);
    setSearchQuery('');
  };

  const handleNavClick = (section) => {
    setActiveSection(activeSection === section ? null : section);
  };

  return (
    <div className="home-container">
      {/* Navigation Bar */}
      <div className="nav-bar">
        <button 
          className={`nav-button ${activeSection === 'borrow' ? 'active' : ''}`}
          onClick={() => handleNavClick('borrow')}
        >
          📚 Borrow
        </button>
        <button 
          className={`nav-button ${activeSection === 'return' ? 'active' : ''}`}
          onClick={() => handleNavClick('return')}
        >
          ↩️ Return
        </button>
        <button 
          className={`nav-button ${activeSection === 'donate' ? 'active' : ''}`}
          onClick={() => handleNavClick('donate')}
        >
          🎁 Donate
        </button>
        <button 
          className={`nav-button ${activeSection === 'events' ? 'active' : ''}`}
          onClick={() => handleNavClick('events')}
        >
          📅 Events
        </button>
        <button 
          className={`nav-button ${activeSection === 'contact' ? 'active' : ''}`}
          onClick={() => handleNavClick('contact')}
        >
          📞 Contact
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
            <div className="borrowed-items">
              <h3>Your Borrowed Items</h3>
              <ul>
                {items.filter(item => item.Status === 'Borrowed').map(item => (
                  <li key={item.ItemID}>
                    <strong>{item.Title}</strong> by {item.Author}
                    <button className="return-button">Return</button>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {activeSection === 'donate' && (
          <div className="section donate-section">
            <h2>Donate Items</h2>
            <form className="donate-form">
              <div className="form-group">
                <label>Item Title:</label>
                <input type="text" placeholder="Enter item title" />
              </div>
              <div className="form-group">
                <label>Author:</label>
                <input type="text" placeholder="Enter author name" />
              </div>
              <div className="form-group">
                <label>Type:</label>
                <select>
                  <option value="book">Book</option>
                  <option value="digital">Digital Item</option>
                  <option value="magazine">Magazine</option>
                </select>
              </div>
              <button type="submit" className="submit-button">Submit Donation</button>
            </form>
          </div>
        )}

        {activeSection === 'events' && (
          <div className="section events-section">
            <h2>Library Events</h2>
            <div className="events-list">
              <div className="event-card">
                <h3>Book Club Meeting</h3>
                <p>Date: March 30, 2024</p>
                <p>Time: 2:00 PM</p>
                <button className="register-button">Register</button>
              </div>
              <div className="event-card">
                <h3>Author Reading</h3>
                <p>Date: April 5, 2024</p>
                <p>Time: 3:00 PM</p>
                <button className="register-button">Register</button>
              </div>
            </div>
          </div>
        )}

        {activeSection === 'contact' && (
          <div className="section contact-section">
            <h2>Contact Us</h2>
            <div className="contact-info">
              <div className="contact-card">
                <h3>📞 Phone</h3>
                <p>(555) 123-4567</p>
              </div>
              <div className="contact-card">
                <h3>📧 Email</h3>
                <p>library@example.com</p>
              </div>
              <div className="contact-card">
                <h3>📍 Address</h3>
                <p>123 Library Street<br />City, State 12345</p>
              </div>
            </div>
            <form className="contact-form">
              <div className="form-group">
                <label>Name:</label>
                <input type="text" placeholder="Your name" />
              </div>
              <div className="form-group">
                <label>Email:</label>
                <input type="email" placeholder="Your email" />
              </div>
              <div className="form-group">
                <label>Message:</label>
                <textarea placeholder="Your message"></textarea>
              </div>
              <button type="submit" className="submit-button">Send Message</button>
            </form>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="main-content">
        {searchResults.length > 0 ? (
          <>
            <h2>Search Results for "{searchQuery}"</h2>
            {searchResults.map((item) => (
              <div key={item.ItemID} className="item-card">
                <h3>{item.Title}</h3>
                <p>Author: {item.Author}</p>
                <p>Type: {item.Type}</p>
                <p>Status: {item.Status}</p>
                <p>Publication Year: {item.PublicationYear}</p>
              </div>
            ))}
          </>
        ) : searchQuery ? (
          <div className="no-results">
            <p>No items found matching your search "{searchQuery}"</p>
          </div>
        ) : (
          <>
            <h2>Library Items</h2>
            {items.map((item) => (
              <div key={item.ItemID} className="item-card">
                <h3>{item.Title}</h3>
                <p>Author: {item.Author}</p>
                <p>Type: {item.Type}</p>
                <p>Status: {item.Status}</p>
                <p>Publication Year: {item.PublicationYear}</p>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}

export default Home;