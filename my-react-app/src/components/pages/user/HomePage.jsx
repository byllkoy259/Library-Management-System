import { useEffect, useState } from "react";
import SearchBar from "../../common/SearchBar";
import BookCard from "../../common/BookCard";
import { getBooks } from "../../../api";
import "./HomePage.css";

function HomePage({ userName, onLogout }) {
    const [newBooks, setNewBooks] = useState([]);
    const [popularBooks, setPopularBooks] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchBooks = async () => {
            try {
                setIsLoading(true);
                const allBooks = await getBooks();
                setNewBooks(allBooks.slice(0, 5));
                setPopularBooks(allBooks.slice(5, 10));
                setError(null);       
            } catch (err) {
                setError('Failed to load books. Please try again later.');
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };
        fetchBooks();
    }, []);

    const handleSearch = (query) => {
        console.log("Searching for:", query);
    };

    return (
        <div className="homepage">
            <main className="homepage-main">
                <section className="hero-welcome">
                    <div className="hero-welcome-content">
                        <h1>Hi, {userName}!</h1>
                        <p>What are you looking for today?</p>
                        <SearchBar onSearch={handleSearch} />
                    </div>
                </section>

                <section className="book-section">
                    <h2 className="section-title">New Arrivals</h2>
                    {isLoading && <p>Loading...</p>}
                    {error && <p className="error-message">{error}</p>}
                    <div className="book-list">
                        {newBooks.map(book => (
                            <BookCard key={book.id} book={book} />
                        ))}
                    </div>
                </section>

                <section className="book-section">
                    <h2 className="section-title">Popular Books</h2>
                    {isLoading && <p>Loading...</p>}
                    {error && <p className="error-message">{error}</p>}
                    <div className="book-list">
                        {popularBooks.map(book => (
                            <BookCard key={book.id} book={book} />
                        ))}
                    </div>
                </section>
            </main>
        </div>
    )
}

export default HomePage;