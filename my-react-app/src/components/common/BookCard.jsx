import { Link } from 'react-router-dom';
import "./BookCard.css";

const DEFAULT_COVER = "https://via.placeholder.com/150x220?text=No+Cover";

function BookCard({ book }) {
    return (
        <Link to={`/books/${book.id}`} className="book-card">
            <div className="book-card">
                <div className="book-card-image-container">
                    <img
                        src={book.cover_image || DEFAULT_COVER}
                        alt={`Cover of ${book.title}`}
                        className="book-card-image"
                    />
                </div>
                <div className="book-card-content">
                    <h3 className="book-card-title">{book.title}</h3>
                    <p className="book-card-author">{book.author_name || "Unknown Author"}</p>
                </div>
            </div>
        </Link>
    );
}

export default BookCard;