import './footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section footer-about">
            <h3>BookSphere</h3>
            <p>Modern library management platform, bringing you the best reading experience.</p>
          </div>

          <div className="footer-section footer-links">
            <h4>Quick Link</h4>
            <ul>
              <li><a href="#home">Home</a></li>
              <li><a href="#search">Search</a></li>
              <li><a href="#about">About</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div>

          <div className="footer-section footer-links">
            <h4>Support</h4>
            <ul>
              <li><a href="#faq">FAQ</a></li>
              <li><a href="#guide">Guide</a></li>
              <li><a href="#privacy">Privacy Policy</a></li>
              <li><a href="#terms">Terms of Use</a></li>
            </ul>
          </div>

          <div className="footer-section footer-contact">
            <h4>Contact</h4>
            <ul>
              <li>contact@booksphere.vn</li>
              <li>(+84) 123 456 789</li>
              <li>Hanoi, Vietnam</li>
            </ul>
            <div className="footer-social">
              <a href="#facebook">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Facebook_Logo_%282019%29.png/500px-Facebook_Logo_%282019%29.png" alt="Facebook" />
              </a>
              <a href="#x">
                <img src="https://www.freeiconspng.com/uploads/new-x-twitter-logo-png-photo-1.png" alt="X-logo" />
              </a>
              <a href="#instagram">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png" alt="Instagram-logo" />
              </a>
              <a href="#youtube">
                <img src="https://hstatic.net/0/0/global/design/haravan/h_index/images/yt-mau.svg" alt="Youtube" />
              </a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p className="footer-copyright">
            © {currentYear} BookSphere. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;