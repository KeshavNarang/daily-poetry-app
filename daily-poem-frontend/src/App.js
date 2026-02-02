import { useEffect, useState } from "react";

function App() {
  const [poemData, setPoemData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/today") // points to your local backend
      .then(res => res.json())
      .then(data => setPoemData(data));
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