import React, { useEffect, useState } from 'react';
import { getItems } from '../api';

function Home() {
  const [items, setItems] = useState([]);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Get user data from localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }

    const fetchData = async () => {
      try {
        const res = await getItems();
        setItems(res.data);
      } catch (err) {
        console.error('Error fetching items:', err);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      {user && (
        <div className="welcome-message">
          <h2>Welcome, {user.firstName} {user.lastName}!</h2>
        </div>
      )}
      <h1>Library Items</h1>
      <ul>
        {items.map(item => (
          <li key={item.ItemID}>
            <strong>{item.Title}</strong> by {item.Author} ({item.Type}) - {item.Status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Home;
