import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { logout, searchItems } from '../api';

const Navigation = ({ user, onLogout }) => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    
    try {
      const response = await searchItems(searchQuery);
      navigate('/home', { 
        state: { 
          searchQuery, 
          searchResults: response.data,
          isSearching: true 
        } 
      });
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  const handleShowAll = () => {
    setSearchQuery('');
    navigate('/home', { 
      state: { 
        searchQuery: '', 
        searchResults: [],
        isSearching: false 
      } 
    });
  };

  const handleLogout = async () => {
    try {
      await logout();
      onLogout();
      navigate('/login', { replace: true });
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <>
      <div className="logout-bar">
        {user ? (
          <div className="user-section">
            <span className="welcome-text">Welcome, {user.firstName} {user.lastName}!</span>
            <div className="logout-container">
              <button onClick={handleLogout} className="logout-button">
                Logout
              </button>
            </div>
          </div>
        ) : (
          <div className="auth-links">
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/signup" className="nav-link">Sign Up</Link>
          </div>
        )}
      </div>

      {user && (
        <nav className="main-nav">
          <div className="nav-left">
            <img src="/images/library-logo-ver2.png" alt="Library Logo" className="nav-logo" />
          </div>
          <div className="search-container">
            <form onSubmit={handleSearch} className="search-form">
              <input 
                type="text" 
                placeholder="Search library items..." 
                className="search-input"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <button type="submit" className="search-button">Search</button>
              <button type="button" onClick={handleShowAll} className="show-all-button">Show All</button>
            </form>
          </div>
        </nav>
      )}
    </>
  );
};

export default Navigation; 