import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const API_ENDPOINT = "http://127.0.0.1:8000"; // Your backend

function SignupForm({ onSignupSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate(); // Hook to handle navigation

  const handleSignup = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      setIsLoading(false);
      return;
    }

    const signupPayload = {
      username,
      password,
    };

    try {
      const response = await fetch(`${API_ENDPOINT}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(signupPayload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("User signed up:", data);
      onSignupSuccess(); // Call the signup success handler
      navigate('/'); // Redirect to LoginPage after signing up
    } catch (error) {
      console.error("Error signing up:", error);
      setError("Signup failed, please try again.");
    } finally {
      setIsLoading(false); // Stop loading
    }
  };

  return (
    <div className="signup-form">
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSignup}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Confirm Password:</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Signing up..." : "Sign Up"}
        </button>
      </form>
    </div>
  );
}

export default SignupForm;