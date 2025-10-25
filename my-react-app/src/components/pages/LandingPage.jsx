import { useState, useEffect } from 'react';
import Header from "../layout/Header";
import Footer from "../layout/Footer";
import './LandingPage.css';
import SmartSearch from '/src/assets/smart-search.png';
import Management from '/src/assets/management.png';
import Read from '/src/assets/read.png';

function LandingPage({ onLogin, onRegister }) {
  const [activeFeature, setActiveFeature] = useState(0);

  const features = [
    {
      title: "Smart Search",
      description: "Find books quickly with advanced filters and smart suggestions",
      icon: SmartSearch
    },
    {
      title: "Easy Management",
      description: "Track your borrowing history and renew books online anytime",
      icon: Management
    },
    {
      title: "Read Anywhere",
      description: "Access a digital library with thousands of e-books",
      icon: Read
    }
  ];

  const stats = [
    { number: "50,000+", label: "Books" },
    { number: "10,000+", label: "Members" },
    { number: "100,000+", label: "Borrows per year" },
    { number: "24/7", label: "Support" }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % features.length);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="landing-page">
      <Header isAuthenticated={false} onLogin={onLogin} onRegister={onRegister} />
      
      <main className="landing-main">
        {/* Hero Section */}
        <section className="hero-section">
          <div className="hero-content">
            <div className="hero-text">
              <h1 className="hero-title">
                Welcome to
                <span className="highlight"> BookSphere</span>
              </h1>
              <p className="hero-description">
                A modern library management platform that connects you to thousands of titles 
                and delivers the best reading experience
              </p>
              <div className="hero-actions">
                <button className="btn-primary" onClick={onLogin}>
                  Get Started
                </button>
                <button className="btn-secondary">
                  Learn More
                </button>
              </div>
            </div>
            <div className="hero-image">
              <div className="floating-card card-1">
                <div className="book-icon">
                  <img src="https://cdn-icons-png.flaticon.com/512/3500/3500280.png" alt="Literature" />
                </div>
                <p>Literature</p>
              </div>
              <div className="floating-card card-2">
                <div className="book-icon">
                  <img src="https://cdn-icons-png.flaticon.com/512/1046/1046269.png" alt="Science" />
                </div>
                <p>Science</p>
              </div>
              <div className="floating-card card-3">
                <div className="book-icon">
                  <img src="https://cdn-icons-png.flaticon.com/512/10262/10262344.png" alt="Skills" />
                </div>
                <p>Skills</p>
              </div>
              <div className="hero-circle"></div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="features-section">
          <h2 className="section-title">Outstanding Features</h2>
          <p className="section-subtitle">Discover the amazing features of BookSphere</p>
          
          <div className="features-grid">
            {features.map((feature, index) => (
              <div 
                key={index}
                className={`feature-card ${activeFeature === index ? 'active' : ''}`}
                onMouseEnter={() => setActiveFeature(index)}
              >
                <div className="feature-icon">
                  <img src={feature.icon} alt={feature.title} />
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Stats Section */}
        <section className="stats-section">
          <div className="stats-container">
            {stats.map((stat, index) => (
              <div key={index} className="stat-item">
                <div className="stat-number">{stat.number}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
            ))}
          </div>
        </section>

        {/* How it works Section */}
        <section className="how-it-works-section">
          <h2 className="section-title">How It Works</h2>
          <p className="section-subtitle">Just 3 simple steps</p>
          
          <div className="steps-container">
            <div className="step-item">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Create an Account</h3>
                <p>Sign up for free in just a few minutes</p>
              </div>
            </div>
            
            <div className="step-arrow">→</div>
            
            <div className="step-item">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Search for Books</h3>
                <p>Browse through thousands of diverse titles</p>
              </div>
            </div>
            
            <div className="step-arrow">→</div>
            
            <div className="step-item">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Start Reading</h3>
                <p>Borrow books and enjoy your reading journey</p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="cta-section">
          <div className="cta-content">
            <h2>Ready to explore the world of books?</h2>
            <p>Join thousands of other readers on BookSphere today</p>
            <button className="btn-cta" onClick={onLogin}>
              Log in Now
            </button>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}

export default LandingPage;