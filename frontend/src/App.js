import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate, Link } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import Test from './pages/Test';
import { logout, searchItems } from './api';
import './App.css';

// Protected Route component
const ProtectedRoute = ({ children }) => {
  const user = localStorage.getItem('user');
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

// Navigation component
function Navigation() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

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
      localStorage.removeItem('user');
      navigate('/login', { replace: true });
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <>
      <div className="logout-bar">
        {user ? (
          <div className="logout-container">
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        ) : (
          <Link to="/login" className="nav-link">
            Login
          </Link>
        )}
      </div>
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
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <header>
          <Navigation />
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<Login />} />
            <Route 
              path="/home" 
              element={
                <ProtectedRoute>
                  <Home />
                </ProtectedRoute>
              } 
            />
            <Route path="/test" element={<Test />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;