import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./SearchBar.css";

function SearchBar({ onSearch }) {
    const [query, setQuery] = useState("");
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query.trim());
            navigate(`/books?q=${encodeURIComponent(query.trim())}`);
        }
    };

    return (
        <form className="search-bar-container" onSubmit={handleSubmit}>
            <input
                type="text"
                className="search-input"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for books..."
            />
            <button type="submit" className="search-button">Search</button>
        </form>
    );
}

export default SearchBar;