import { useEffect, useState } from "react";

function App() {
  const [poemData, setPoemData] = useState(null);

  useEffect(() => {
    // Use deployed URL if not localhost
    const API_BASE =
      window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
        ? "http://127.0.0.1:8000"
        : "https://daily-poetry-app-production.up.railway.app";

    fetch(`${API_BASE}/today`)
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