import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate, Link } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import SignUp from './components/SignUp';
import { logout, searchItems } from './api';
import './App.css';
import Navigation from './components/Navigation';

// Protected Route component
const ProtectedRoute = ({ children, user }) => {
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check for existing user data in localStorage on component mount
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <BrowserRouter>
      <div className="app-container">
        <header>
          <Navigation user={user} onLogout={handleLogout} />
        </header>
        <main>
          <Routes>
            <Route 
              path="/" 
              element={
                user ? (
                  <Navigate to="/home" replace />
                ) : (
                  <Navigate to="/login" replace />
                )
              } 
            />
            <Route 
              path="/login" 
              element={
                user ? (
                  <Navigate to="/home" replace />
                ) : (
                  <Login onLogin={handleLogin} />
                )
              } 
            />
            <Route 
              path="/signup" 
              element={
                user ? (
                  <Navigate to="/home" replace />
                ) : (
                  <SignUp onClose={() => window.history.back()} />
                )
              } 
            />
            <Route 
              path="/home" 
              element={
                <ProtectedRoute user={user}>
                  <Home />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </main>
        <footer className="footer">
          Made for CMPT354 SPRING 2025,<br />
          Evan Chen and Emmy Fong
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;