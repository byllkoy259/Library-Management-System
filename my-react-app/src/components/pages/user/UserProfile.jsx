import { useState, useEffect } from 'react';
import keycloak from '../../../keycloak'; // Để lấy thông tin user
import { getCurrentBorrows, getBorrowHistory } from '../../../api';
import './UserProfile.css';
import { Link } from 'react-router-dom';

function UserProfile() {
  const [currentBorrows, setCurrentBorrows] = useState([]);
  const [borrowHistory, setBorrowHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  // Lấy thông tin người dùng trực tiếp từ instance keycloak
  const userInfo = {
    username: keycloak.tokenParsed?.preferred_username,
    name: keycloak.tokenParsed?.name,
    email: keycloak.tokenParsed?.email,
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Gọi API song song để tăng tốc độ
        const [currentData, historyData] = await Promise.all([
          getCurrentBorrows(),
          getBorrowHistory()
        ]);
        setCurrentBorrows(currentData);
        setBorrowHistory(historyData);
      } catch (error) {
        console.error("Failed to fetch user data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const renderBorrowList = (items, isHistory = false) => {
    if (items.length === 0) {
      return <p>{isHistory ? "No borrowing history found." : "You are not currently borrowing any books."}</p>;
    }
    return (
      <ul className="borrow-list">
        {items.map(item => (
          <li key={item.id} className="borrow-item">
            <Link to={`/books/${item.book.id}`}>
              <img src={item.book.cover_image || 'https://via.placeholder.com/60x90'} alt={item.book.title} />
            </Link>
            <div className="item-details">
              <Link to={`/books/${item.book.id}`} className="item-title">{item.book.title}</Link>
              {isHistory ? (
                <span>Returned on: {new Date(item.return_date).toLocaleDateString()}</span>
              ) : (
                <span>Due Date: {new Date(item.due_date).toLocaleDateString()}</span>
              )}
            </div>
            {isHistory && <span className={`status ${item.status}`}>{item.status}</span>}
          </li>
        ))}
      </ul>
    );
  };

  return (
    <main className="profile-page">
      <div className="profile-container">
        <aside className="profile-sidebar">
          <div className="user-info-card">
            <h2 className="card-title">My Profile</h2>
            <p><strong>Username:</strong> {userInfo.username}</p>
            <p><strong>Full Name:</strong> {userInfo.name}</p>
            <p><strong>Email:</strong> {userInfo.email}</p>
            <a 
              href={keycloak.createAccountUrl()} 
              target="_blank" 
              rel="noopener noreferrer"
              className="manage-account-btn"
            >
              Manage Account
            </a>
          </div>
        </aside>

        <section className="profile-main-content">
          <div className="borrow-section">
            <h2 className="section-title">Currently Borrowing</h2>
            {loading ? <p>Loading...</p> : renderBorrowList(currentBorrows)}
          </div>

          <div className="borrow-section">
            <h2 className="section-title">Borrowing History</h2>
            {loading ? <p>Loading...</p> : renderBorrowList(borrowHistory, true)}
          </div>
        </section>
      </div>
    </main>
  );
}

export default UserProfile;