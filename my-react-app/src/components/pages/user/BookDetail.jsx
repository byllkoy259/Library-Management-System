import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getBookById } from '../../../api';
import './BookDetail.css';

const DEFAULT_COVER = 'https://via.placeholder.com/300x440.png?text=No+Cover';

function BookDetail() {
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { bookId } = useParams(); // Lấy ID sách từ URL, ví dụ: /books/123

  useEffect(() => {
    const fetchBookDetails = async () => {
      setLoading(true);
      setError('');
      try {
        const data = await getBookById(bookId);
        setBook(data);
      } catch (err) {
        setError('Could not fetch book details. The book may not exist or an error occurred.');
        console.error("Failed to fetch book:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchBookDetails();
  }, [bookId]);

  if (loading) {
    return <div className="book-detail-container"><p>Loading book details...</p></div>;
  }

  if (error) {
    return <div className="book-detail-container"><p className="error-message">{error}</p></div>;
  }

  if (!book) {
    return null;
  }

  return (
    <main className="book-detail-page">
      <div className="book-detail-container">
        <div className="book-cover-container">
          <img 
            src={book.cover_image || DEFAULT_COVER} 
            alt={`Cover of ${book.title}`} 
            className="book-cover-image"
          />
        </div>
        <div className="book-info-container">
          <h1 className="book-title">{book.title}</h1>
          <p className="book-author">
            by <a href="#">{book.author_name || 'Unknown Author'}</a>
          </p>
          <div className="book-meta">
            <span className="meta-item"><strong>Category:</strong> {book.category_name || 'N/A'}</span>
            <span className="meta-item"><strong>Published:</strong> {book.publication_year || 'N/A'}</span>
          </div>
          <p className="book-description">
            {book.description || 'No description available.'}
          </p>
          <div className="book-actions">
            <button className="btn-borrow">Borrow Book</button>
            <button className="btn-wishlist">Add to Wishlist</button>
          </div>
        </div>
      </div>
    </main>
  );
}

export default BookDetail;