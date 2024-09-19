import React, { useState } from "react";
import LoginForm from "./auth/LoginForm";
import SignupForm from "./auth/SignupForm";
import ChatApp from "./app/ChatApp";
import "./App.css";

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
          <h1 className="app-name">DocuGPT</h1>
          <img src="/squarespace-icon.png" alt="Logo" className="logo-image" />
          <LoginForm onLoginSuccess={handleLoginSuccess} />
          <button onClick={() => setCurrentPage("signup")} className="switch-button">
            Don't have an account? Sign Up
          </button>
        </div>
      )}

      {currentPage === "signup" && (
        <div className="page-container">
          <h1 className="app-name">DocuGPT</h1>
          <img src="/squarespace-icon.png" alt="Logo" className="logo-image" />
          <SignupForm onSignupSuccess={handleSignupSuccess}/>
          <button onClick={() => setCurrentPage("login")}  className="switch-button" >
            Already have an account? Login
          </button>
        </div>
      )}

      {currentPage === "chat" && <ChatApp />}
    </div>
  );
};

export default App;