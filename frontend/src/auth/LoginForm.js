import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginForm.css"
import Cookies from "js-cookie";

const API_ENDPOINT = "http://127.0.0.1:8000";

function LoginForm({ onLoginSuccess }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate(); // Hook to handle navigation

    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        const loginPayload = {
            username,
            password,
        };

        try {
            const response = await fetch(`${API_ENDPOINT}/auth/login`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(loginPayload),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            Cookies.set("token", data.access_token, {expires: 7}); // Store JWT token in cookies
            onLoginSuccess(); // Call the login success handler
            navigate('/chat'); // Redirect to ChatApp page after login
        } catch (error) {
            console.error("Error logging in:", error);
            setError("Invalid credentials, please try again.");
        } finally {
            setIsLoading(false); // Stop loading
        }
    }

    return (
        <div className="login-form">
            {error && <div className="error-message">{error}</div>}
            <form onSubmit={handleLogin}>
                <div>
                    <input type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        placeholder="Username"
                    />
                </div>
                <div>
                    <input type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        placeholder="Password"
                    />
                </div>
                <button type="submit" disabled={isLoading}>
                    {isLoading ? "Logging in..." : "Login"}
                </button>
            </form>
        </div>
    );
}

export default LoginForm;