import React, { useEffect, useState } from 'react';
import { getItems, searchItems, borrowItem, returnItem } from '../api';
import { useLocation } from 'react-router-dom';

function Home() {
  const [items, setItems] = useState([]);
  const [user, setUser] = useState(null);
  const [activeSection, setActiveSection] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [borrowMessage, setBorrowMessage] = useState({ type: '', text: '' });
  const [returnMessage, setReturnMessage] = useState({ type: '', text: '' });
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
            <div className="borrowed-items">
              <h3>Your Borrowed Items</h3>
              {console.log('All items:', items)}
              {console.log('Checked out items:', items.filter(item => item.Status === 'CheckedOut'))}
              <ul>
                {items.filter(item => item.Status === 'CheckedOut').map(item => (
                  <li key={item.ItemID}>
                    <strong>{item.Title}</strong> by {item.Author}
                    <p>Due Date: {item.DueDate}</p>
                    <button 
                      className="return-button"
                      onClick={() => handleReturn(item.ItemID)}
                    >
                      Return
                    </button>
                  </li>
                ))}
              </ul>
              {items.filter(item => item.Status === 'CheckedOut').length === 0 && (
                <p>You don't have any items checked out.</p>
              )}
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
                    <button 
                      className="borrow-button"
                      onClick={() => handleBorrow(item.ItemID)}
                    >
                      Borrow
                    </button>
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
                  <div className="content-wrapper">
                    <img src="/images/book.png" alt="Book cover" />
                    <h3>{item.Title}</h3>
                  </div>
                  <div className="item-details">
                    <p><strong>Author:</strong> {item.Author}</p>
                    <p><strong>Type:</strong> {item.Type}</p>
                    <p><strong>Status:</strong> {item.Status === 'Available' ? '✅' : '❌'}</p>
                    <button 
                      className="borrow-button"
                      onClick={() => handleBorrow(item.ItemID)}
                    >
                      Borrow
                    </button>
                  </div>
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