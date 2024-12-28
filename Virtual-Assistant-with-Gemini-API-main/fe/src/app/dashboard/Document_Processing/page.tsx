import React, { useState } from "react";
import { Link } from "react-router-dom";

const DocumentProcessing: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/process_document", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setSummary(data.summary);
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", backgroundColor: "#f0f2f5", minHeight: "100vh" }}>
      {/* Navbar */}
      <nav style={{ backgroundColor: "#343a40", display: "flex", justifyContent: "center", padding: "1rem" }}>
        <Link to="/" style={{ color: "#fff", margin: "0 15px", textDecoration: "none" }}>Home</Link>
        <Link to="/dashboard/transcribe" style={{ color: "#fff", margin: "0 15px", textDecoration: "none" }}>Transcribe</Link>
        <Link to="/dashboard/document_processing" style={{ color: "#fff", margin: "0 15px", textDecoration: "none" }}>Document Processing</Link>
      </nav>

      <div style={{ maxWidth: "800px", margin: "2rem auto", padding: "1rem" }}>
        <h1 style={{ textAlign: "center", marginBottom: "1.5rem" }}>Document Processing</h1>
        <div style={{
          backgroundColor: "#fff",
          borderRadius: "8px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          padding: "16px",
          marginBottom: "20px"
        }}>
          <div style={{ marginBottom: "10px" }}>
            <input type="file" onChange={handleFileChange} style={{ marginRight: "10px" }} />
            <button
              style={{
                padding: "10px 20px",
                borderRadius: "4px",
                backgroundColor: "#007bff",
                color: "#fff",
                border: "none",
                cursor: "pointer",
                transition: "background-color 0.3s ease"
              }}
              onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#0056b3")}
              onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#007bff")}
              onClick={handleUpload}
              disabled={loading}
            >
              {loading ? "Uploading..." : "Upload & Get Summary"}
            </button>
          </div>
          {summary && (
            <p style={{ backgroundColor: "#f9f9f9", padding: "10px", borderRadius: "4px" }}>
              <strong>Summary:</strong> {summary}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentProcessing;