import React, { useState, useEffect } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [topic, setTopic] = useState("");
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);

  // Charger l'historique au démarrage
  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/history");
      if (!response.ok) throw new Error("Erreur lors du chargement de l'historique");
      const data = await response.json();
      setHistory(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error("Erreur lors de l'analyse de l'URL.");
      }

      const data = await response.json();
      setSummary(data.summary);
      setTopic(data.topic);
      setTitle(data.title || "");
      setUrl("");
      
      // Recharger l'historique après analyse
      fetchHistory();
    } catch (err) {
      setError(err.message);
      setSummary("");
      setTopic("");
      setTitle("");
    } finally {
      setLoading(false);
    }
  };

  const handleHistoryClick = (item) => {
    setSelectedItem(item);
    setSummary(item.summary);
    setTopic(item.topic);
    setTitle(item.title || "");
  };

  // Delete item from history
  const handleDeleteItem = async (e, itemId) => {
    e.stopPropagation(); // Éviter que le clic sur la poubelle déclenche handleHistoryClick
    
    try {
      const response = await fetch(`http://127.0.0.1:5000/delete/${itemId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la suppression");
      }

      // Si l'élément supprimé était sélectionné, le désélectionner
      if (selectedItem?.id === itemId) {
        setSelectedItem(null);
        setSummary("");
        setTopic("");
        setTitle("");
      }

      // Recharger l'historique
      fetchHistory();
    } catch (err) {
      console.error(err);
      alert("Erreur lors de la suppression : " + err.message);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial" }}>
      {/* Panneau gauche - Historique */}
      <div style={{
        width: "300px",
        borderRight: "1px solid #ccc",
        padding: "20px",
        overflowY: "auto",
        backgroundColor: "#f9f9f9"
      }}>
        <h2>Historique</h2>
        {history.length === 0 ? (
          <p style={{ color: "#999" }}>Aucune analyse</p>
        ) : (
          <ul style={{ listStyle: "none", padding: 0 }}>
            {history.map((item) => (
              <li
                key={item.id}
                onClick={() => handleHistoryClick(item)}
                style={{
                  padding: "10px",
                  marginBottom: "10px",
                  backgroundColor: selectedItem?.id === item.id ? "#e0e0e0" : "#fff",
                  border: "1px solid #ddd",
                  borderRadius: "5px",
                  cursor: "pointer",
                  transition: "background-color 0.3s",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start"
                }}
              >
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: "bold", fontSize: "12px", color: "#333", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                    {item.title || "Sans titre"}
                  </div>
                  <div style={{ fontSize: "11px", color: "#666", marginTop: "5px" }}>
                    📌 {item.topic || "N/A"}
                  </div>
                  <div style={{ fontSize: "10px", color: "#999", marginTop: "3px" }}>
                    {new Date(item.created_at).toLocaleDateString()}
                  </div>
                </div>
                {/* Icône poubelle */}
                <button
                  onClick={(e) => handleDeleteItem(e, item.id)}
                  style={{
                    background: "none",
                    border: "none",
                    cursor: "pointer",
                    fontSize: "18px",
                    padding: "5px",
                    marginLeft: "10px",
                    color: "#999",
                    transition: "color 0.3s"
                  }}
                  onMouseEnter={(e) => e.target.style.color = "#d32f2f"}
                  onMouseLeave={(e) => e.target.style.color = "#999"}
                  title="Supprimer"
                >
                  🗑️
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Panneau droit - Saisie et résultats */}
      <div style={{ flex: 1, padding: "20px", overflowY: "auto" }}>
        <h1>Analyseur d'URL</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Saisissez une URL (ex: https://exemple.com)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            style={{ padding: "8px", width: "400px", marginRight: "10px" }}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? "Analyse en cours..." : "Analyser"}
          </button>
        </form>

        {error && <p style={{ color: "red" }}>{error}</p>}

        {title && (
          <div style={{ marginTop: "20px" }}>
            <h2>Titre :</h2>
            <h3 style={{ margin: "6px 0" }}>{title}</h3>
         </div>
       )}


        {summary && (
          <div style={{ marginTop: "20px" }}>
            <h2>Résumé :</h2>
            <p style={{ whiteSpace: "pre-wrap", backgroundColor: "#f0f0f0", padding: "10px", borderRadius: "5px" }}>
              {summary}
            </p>
          </div>
        )}

        {topic && (
          <div style={{ marginTop: "20px" }}>
            <h2>Topic principal :</h2>
            <p style={{ fontWeight: "bold", fontSize: "18px" }}>{topic}</p>
          </div>
        )}

        {selectedItem && (
          <div style={{ marginTop: "20px", padding: "10px", backgroundColor: "#fffacd", borderRadius: "5px" }}>
            <h3>URL sélectionnée :</h3>
            <a href={selectedItem.url} target="_blank" rel="noopener noreferrer" style={{ color: "#0066cc" }}>
              {selectedItem.url}
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;