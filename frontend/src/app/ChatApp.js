import React, { useState } from "react";
import { useEffect } from "react";
import "./ChatApp.css";

const API_ENDPOINT = "http://127.0.0.1:8000"; // Your local backend

function ChatApp() {
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState([]);
  const [file, setFile] = useState(null);
  const [groupId, setGroupId] = useState(null); // Store group_id for the session
  const [pdfUrl, setPdfUrl] = useState(null); // State to store the PDF URL
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [menuItems, setMenuItems] = useState([]);

  const getUserDocument = async () => {
    setIsLoading(true); // Start loading

    // Get the token from localStorage
    const token = localStorage.getItem('token');

    try {
      const response = await fetch(
        `${API_ENDPOINT}/upload/?token=${token}`, // Token passed as a query parameter
        { method: "GET" }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("User documents fetched", data);

      // Extract the group_id and document name from the response
      const items = data.map((item) => ({ name: item.doc_name, group_id: item.group_id }));
      setMenuItems(items);
    } catch (error) {
      console.error("Error fetching user documents:", error);
      setError("There is a temporary issue with the server. Please try again later.");
    } finally {
      setIsLoading(false); // Stop loading
    }
  };

  useEffect(() => {
    getUserDocument();
  }, []);

  const uploadDocument = async () => {
    if (!file) return;
    setIsLoading(true); // Start loading
  
    const formData = new FormData();
    formData.append("file", file);
  
    // Get the token from localStorage
    const token = localStorage.getItem('token');
  
    try {
      const response = await fetch(
        `${API_ENDPOINT}/upload/?token=${token}`, // Token passed as a query parameter
        { 
          method: "POST", 
          body: formData 
        }
      );
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const result = await response.json();
      console.log("Document uploaded", result);
      const newGroupId = result.group_id;  // Extract the group_id
      setGroupId(newGroupId); // Update state with the new group_id
      setConversation([]);
      setPdfUrl(URL.createObjectURL(file)); // Create a URL for the uploaded file and set it
  
      // Use the newGroupId directly after it's fetched
      window.history.pushState({}, '', `/group_id/${newGroupId}`);

      const documentName = file.name;
      setMenuItems((items) => [...items, { name: documentName, group_id: newGroupId }]);
    } catch (error) {
      console.error("Error uploading document:", error);
      setError("There is a temporary issue with the server. Please try again later.");
    } finally {
      setIsLoading(false); // Stop loading
    }
  };  

  const sendMessage = async () => {
    if (message.trim() === "" || !groupId) return;
    setIsLoading(true); // Start loading

    try {
      const response = await fetch(
        `${API_ENDPOINT}/rag/?group_id=${groupId}`, // RAG route from backend
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify( message ), // match the backend's expected payload
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const outputText = data.response || "No response text found";

      setConversation((convo) => [
        { text: outputText, from: "bot" },
        { text: message, from: "user" },
        ...convo,
      ]);

      setMessage("");
    } catch (error) {
      console.error("Error sending message:", error);
      setError("There is a temporary issue with the server. Please try again later."); // Set the error message
    } finally {
      setIsLoading(false); // Stop loading
    }
  };

  const handleMessageChange = (event) => {
    setMessage(event.target.value);
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      sendMessage();
    }
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSessionChange = async (selectedGroupId) => {
    setIsLoading(true); // Start loading
    setGroupId(selectedGroupId); // Update the groupId to the selected one
  
    try {
      const response = await fetch(
        `${API_ENDPOINT}/rag/?group_id=${selectedGroupId}`, // Fetch conversation for the selected document
        {
          method: "GET",
        }
      );
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      
      // Update conversation with the fetched messages
      setConversation(data.conversation); // Assuming data.conversation contains the chat history
  
      // Update the URL without reloading the page
      window.history.pushState({}, '', `/chat/${selectedGroupId}`);
    } catch (error) {
      console.error("Error fetching document conversation:", error);
      setError("There is a temporary issue with the server. Please try again later.");
    } finally {
      setIsLoading(false); // Stop loading
    }
  };  

  // New function to reset the chat
  const resetChat = () => {
    setMessage("");
    setConversation([]);
    setFile(null);
    setGroupId(null);
    setPdfUrl(null);
    setError(null);
    window.history.pushState({}, '', '/chat/'); // Reset the URL
  };

  return (
    <>
      {error && <div className="error-message">{error}</div>}

      {isLoading && (
        <div className="overlay">
          <div className="spinner"></div>
        </div>
      )}

      <div className={`app-container ${isLoading ? 'faded' : ''}`}>
        <div class="left-bar">
          <div class="chat-menu">
            <div class="new-chat-item" onClick={resetChat}>
              <span>New Chat</span>
            </div>
            {menuItems.slice().reverse().map((item, index) => (
              <div key={index} className="menu-item" onClick={() => handleSessionChange(item.group_id)}>
                <span>{item.name}</span> {/* Display the document name */}
              </div>
            ))}
          </div>
        </div>
        <div className="pdf-preview">
          {pdfUrl && (
            <iframe
              src={pdfUrl}
              title="PDF Preview"
              className="pdf-iframe"
            ></iframe>
          )}
        </div>
        <div className="chat-container">
          <div className="input-area">
            <label htmlFor="file-upload" className="icon-button choose-file"></label>
            <input
              id="file-upload"
              type="file"
              accept="application/pdf"
              style={{ display: 'none' }} // Hide the input field
              onChange={handleFileChange}
            />
            <button onClick={uploadDocument} className="icon-button upload-file"></button>
          </div>
          <div className="messages-area">
            {conversation.map((c, index) => (
              <div
                key={index}
                className={`message ${c.from === "user" ? "user-message" : "bot-message"}`}
              >
                {c.text}
              </div>
            ))}
          </div>
          <div className="input-area">
            <input
              className="input-box"
              type="text"
              value={message}
              onChange={handleMessageChange}
              onKeyPress={handleKeyPress}
              placeholder="Type a message..."
            />
            <button className="send-button" onClick={sendMessage}>
              Send
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

export default ChatApp;
