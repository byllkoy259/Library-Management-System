import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import libraryIcon from '../../assets/library-icon.png';

function Header({ isAuthenticated, userName, onLogin, onRegister, onLogout }) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <header className={`header ${isScrolled ? 'scrolled' : ''}`}>
      <div className="header-container">
        <div className="header-logo">
          <img src={libraryIcon} alt="Library Logo" />
          <Link to="/" style={{ textDecoration: 'none' }}>
              <h1>BookSphere</h1>
          </Link>
        </div>

        <button 
          className={`mobile-menu-toggle ${isMobileMenuOpen ? 'active' : ''}`}
          onClick={toggleMobileMenu}
          aria-label="Toggle menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <nav className={`header-nav ${isMobileMenuOpen ? 'mobile-open' : ''}`}>
          <Link to="/" className="nav-link">HOME</Link>
          <Link to="/books" className="nav-link">SEARCH</Link> 
          <Link to="/about" className="nav-link">ABOUT</Link>
          <Link to="/contact" className="nav-link">CONTACT</Link>
        </nav>

        <div className={`header-actions ${isMobileMenuOpen ? 'mobile-open' : ''}`}>
          {isAuthenticated ? (
            <div className="user-menu">
              <button 
                className="user-menu-button" 
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              >
                What's up, {userName}!
              </button>
              {isDropdownOpen && (
                <div className="dropdown-menu">
                  <Link to="/profile" onClick={() => setIsDropdownOpen(false)}>My Profile</Link>
                  <button className="btn-logout" onClick={() => {onLogout(); setIsDropdownOpen(false)}}>LOGOUT</button>
                </div>
              )}
            </div>
          ) : (
            <>
              <button className="btn-login" onClick={onLogin}>LOGIN</button>
              <button className="btn-register" onClick={onRegister}>REGISTER</button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;