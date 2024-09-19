import React, { useState } from "react";
import LoginForm from "./auth/LoginForm";
import SignupForm from "./auth/SignupForm";
import ChatApp from "./app/ChatApp";

const App = () => {
  const [currentPage, setCurrentPage] = useState("login"); // State to track current page

  const handleLoginSuccess = () => {
    setCurrentPage("chat"); // Navigate to chat page on successful login
  };

  const handleSignupSuccess = () => {
    setCurrentPage("login"); // Redirect to login page after successful signup
  };

  return (
    <div className="app">
      {currentPage === "login" && (
        <div className="page-container">
          <LoginForm onLoginSuccess={handleLoginSuccess} />
          <button onClick={() => setCurrentPage("signup")}>
            Don't have an account? Sign Up
          </button>
        </div>
      )}

      {currentPage === "signup" && (
        <div className="page-container">
          <SignupForm onSignupSuccess={handleSignupSuccess} />
          <button onClick={() => setCurrentPage("login")}>
            Already have an account? Login
          </button>
        </div>
      )}

      {currentPage === "chat" && <ChatApp />}
    </div>
  );
};

export default App;