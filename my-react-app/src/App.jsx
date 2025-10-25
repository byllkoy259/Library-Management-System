import { useEffect, useState } from "react";
import { Routes, Route } from "react-router-dom";
import keycloak from "./keycloak";
import LandingPage from "./components/pages/LandingPage";
import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";
import HomePage from "./components/pages/user/HomePage";
import BookList from "./components/pages/user/BookList";
import BookDetail from "./components/pages/user/BookDetail";
import UserProfile from "./components/pages/user/UserProfile";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userName, setUserName] = useState("");
  const [isKeycloakInitialized, setIsKeycloakInitialized] = useState(false);

  useEffect(() => {
    keycloak
      .init({ onLoad: "check-sso" })
      .then((authenticated) => {
        setIsAuthenticated(authenticated);
        if (authenticated) {
          setUserName(keycloak.tokenParsed?.preferred_username || "User");
        }
      })
      .catch((error) => {
        console.error("Keycloak init failed:", error);
      })
      .finally(() => {
        setIsKeycloakInitialized(true);
      });
  }, []);

  const handleRegister = () => {
    keycloak.register({});
  };

  const handleLogin = () => {
    keycloak.login({});
  };

  const handleLogout = () => {
    keycloak.logout({});
  };

  if (!isKeycloakInitialized) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <LandingPage onLogin={handleLogin} onRegister={handleRegister} />;
  }

  return (
    <div className="app">
      <Header isAuthenticated={isAuthenticated} userName={userName} onLogout={handleLogout} />
      <Routes>
        <Route path="/" element={<HomePage userName={userName} />} />
        <Route path="/books" element={<BookList />} />
        <Route path="/books/:id" element={<BookDetail />} />
        <Route path="/profile" element={<UserProfile />} />
      </Routes>
      <Footer />
    </div>
  );
}

export default App;