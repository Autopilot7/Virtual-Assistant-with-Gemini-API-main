import React, { useState } from "react";
import { Link } from "react-router-dom";

const Transcribe: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [context, setContext] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload an audio file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("context", context);

    try {
      const response = await fetch("http://localhost:5000/transcribe", {
        method: "POST",
        body: formData,
      });
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "transcription.txt";
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", backgroundColor: "#f0f2f5", minHeight: "100vh" }}>
      {/* Navbar */}
      <nav style={{ backgroundColor: "#343a40", display: "flex", justifyContent: "center", padding: "1rem" }}>
        <Link to="/" style={{ color: "#fff", margin: "0 15px", textDecoration: "none" }}>Home</Link>
        <Link to="/dashboard/document_processing" style={{ color: "#fff", margin: "0 15px", textDecoration: "none" }}>Document Processing</Link>
        <Link to="/dashboard/transcribe" style={{ color: "#fff", margin: "0 15px", textDecoration: "none" }}>Transcribe</Link>
      </nav>

      <div style={{ maxWidth: "800px", margin: "2rem auto", padding: "1rem" }}>
        <h1 style={{ textAlign: "center", marginBottom: "1.5rem" }}>Audio Transcription</h1>
        <div style={{
          backgroundColor: "#fff",
          borderRadius: "8px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          padding: "16px"
        }}>
          <div style={{ marginBottom: "10px" }}>
            <label><strong>Select Audio File:</strong></label>
            <input type="file" onChange={handleFileChange} accept="audio/*" style={{ marginLeft: "10px" }} />
          </div>
          <div style={{ marginBottom: "10px" }}>
            <textarea
              placeholder="Optional context..."
              value={context}
              onChange={(e) => setContext(e.target.value)}
              style={{ width: "100%", height: "80px", padding: "10px", borderRadius: "4px" }}
            ></textarea>
          </div>
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
          >
            Upload & Transcribe
          </button>
        </div>
      </div>
    </div>
  );
};

export default Transcribe;