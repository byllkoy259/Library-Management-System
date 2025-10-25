import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { getBooks } from "../../../api";
import BookCard from "../../common/BookCard";
import "./BookList.css";

function BookList() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();

  const query = searchParams.get("q") || ""; // Lấy query 'q' từ URL, ví dụ: /books?q=harry+potter

  useEffect(() => {
    const fetchBooks = async () => {
      setLoading(true);
      try {
        const data = await getBooks(query);
        setBooks(data);
      } catch (error) {
        console.error("Failed to fetch books:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchBooks();
  }, [query]); // Chạy lại mỗi khi query thay đổi

  return (
    <main className="book-list-page">
      <div className="container">
        <h1 className="page-title">
          {query ? `Search Results for "${query}"` : "All Books"}
        </h1>
        {loading ? (
          <p>Loading books...</p>
        ) : (
          <div className="books-grid">
            {books.length > 0 ? (
              books.map(book => <BookCard key={book.id} book={book} />)
            ) : (
              <p>No books found.</p>
            )}
          </div>
        )}
      </div>
    </main>
  );
}

export default BookList;