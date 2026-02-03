import { useEffect, useState } from "react";

function App() {
  const [poemData, setPoemData] = useState(null);

  useEffect(() => {
  // If running on localhost:3000, fetch local backend
  // Otherwise, fetch from the same host the frontend is served on (Railway)
    const API_BASE =
      window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
        ? "http://127.0.0.1:8000"
        : "";  // empty string means "same host"

    fetch(`${API_BASE}/api/poem`)
      .then(res => res.json())
      .then(data => setPoemData(data))
      .catch(err => console.error("Error fetching poem:", err));
  }, []);

  if (!poemData) return <div>Loading...</div>;

  const { poem, date } = poemData;

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto", fontFamily: "serif" }}>
      <h2>{date}</h2>
      <h1>{poem.title}</h1>
      <h3>— {poem.author}</h3>
      {poem.stanzas.map((stanza, i) => (
        <p key={i} style={{ marginBottom: "1.5em", whiteSpace: "pre-line" }}>
          {stanza.join("\n")}
        </p>
      ))}
    </div>
  );
}

export default App;
