import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleQuery = async () => {
    const res = await fetch('http://localhost:8000/query/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div>
      <h1>Enterprise RAG Bot</h1>
      <textarea 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask the bot..."
      />
      <button onClick={handleQuery}>Send</button>
      <div>
        <h3>Response:</h3>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default App;
