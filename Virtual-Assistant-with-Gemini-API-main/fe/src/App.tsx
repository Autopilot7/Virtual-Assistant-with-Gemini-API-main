import React, { useState } from "react";
import { Link } from "react-router-dom";
import { ReactMic } from 'react-mic';

const App: React.FC = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<{ user: string; bot: string }[]>([]);
  const [record, setRecord] = useState(false);
  const [blobURL, setBlobURL] = useState<string | null>(null);

  const handleSendMessage = async () => {
    if (message.trim() === "") return;

    console.log("Sending message:", message); // Logging

    const newChat = { user: message, bot: "" };
    setChatHistory(prevHistory => [...prevHistory, newChat]);

    try {
      const response = await fetch("http://localhost:5000/chatbot", { // Đảm bảo URL đúng với backend
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      console.log("Received response:", data); // Logging response

      if (response.ok) {
        setChatHistory(prevHistory => {
          const updatedHistory = [...prevHistory];
          updatedHistory[updatedHistory.length - 1].bot = data.response;
          return updatedHistory;
        });

        // Text-to-Speech
        const utterance = new SpeechSynthesisUtterance(data.response);
        window.speechSynthesis.speak(utterance);
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.error("Error sending message:", error);
    } finally {
      setMessage("");
    }
  };

  const startRecording = () => {
    setRecord(true);
  };

  const stopRecording = () => {
    setRecord(false);
  };

  const onStop = (recordedBlob: { blob: Blob; blobURL: string }) => {
    console.log('Recorded Blob:', recordedBlob); // Debug logging
    setBlobURL(recordedBlob.blobURL);
    sendAudio(recordedBlob.blob);
  };

  const sendAudio = async (audioBlob: Blob) => {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav');

    try {
      const response = await fetch("http://localhost:5000/record", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      console.log("Received audio response:", data); // Logging response

      if (response.ok) {
        setChatHistory(data.history);

        // Text-to-Speech
        const utterance = new SpeechSynthesisUtterance(data.response);
        window.speechSynthesis.speak(utterance);
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.error("Error processing audio:", error);
    }
  };

  return (
    <div style={{
      fontFamily: "Roboto, Arial, sans-serif",
      backgroundColor: "#f0f2f5",
      minHeight: "100vh"
    }}>
      {/* Navbar */}
      <nav style={{
        backgroundColor: "#343a40",
        display: "flex",
        justifyContent: "center",
        padding: "1rem"
      }}>
        <Link to="/" style={{ color: "#fff", margin: "0 15px", textDecoration: "none" }}>Home</Link>
        <Link to="/dashboard/document_processing" style={{ color: "#fff", margin: "0 15px", textDecoration: "none" }}>Document Processing</Link>
        <Link to="/dashboard/transcribe" style={{ color: "#fff", margin: "0 15px", textDecoration: "none" }}>Transcribe</Link>
      </nav>

      <div style={{ maxWidth: "800px", margin: "2rem auto", padding: "1rem" }}>
        <h1 style={{ textAlign: "center", marginBottom: "1.5rem" }}>Chatbot</h1>
        <div style={{
          backgroundColor: "#ffffff",
          borderRadius: "8px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          padding: "16px",
          marginBottom: "20px",
          maxHeight: "400px",
          overflowY: "auto"
        }}>
          {chatHistory.map((chat, index) => (
            <div key={index} style={{ marginBottom: "10px" }}>
              <p><strong>Bạn:</strong> {chat.user}</p>
              <p><strong>Bot:</strong> {chat.bot}</p>
              <hr />
            </div>
          ))}
        </div>
        <div style={{ display: "flex", marginBottom: "20px" }}>
          <input
            style={{
              flex: 1,
              padding: "10px",
              marginRight: "10px",
              borderRadius: "4px",
              border: "1px solid #ccc"
            }}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Nhập nội dung..."
          />
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
            onClick={handleSendMessage}
          >
            Gửi
          </button>
        </div>

        {/* Voice Chat Section */}
        <div style={{ textAlign: "center" }}>
          <h2>Chat bằng Lời nói</h2>
          <ReactMic
            record={record}
            className="sound-wave"
            onStop={onStop}
            mimeType="audio/wav; codecs=1" // Enforce PCM encoding
            strokeColor="#007bff"
            backgroundColor="#f0f2f5"
          />
          <div style={{ marginTop: "10px" }}>
            {!record ? (
              <button
                onClick={startRecording}
                style={{
                  padding: "10px 20px",
                  borderRadius: "4px",
                  backgroundColor: "#28a745",
                  color: "#fff",
                  border: "none",
                  cursor: "pointer",
                  transition: "background-color 0.3s ease",
                  marginRight: "10px"
                }}
                onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#218838")}
                onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#28a745")}
              >
                Bắt đầu Ghi âm
              </button>
            ) : (
              <button
                onClick={stopRecording}
                style={{
                  padding: "10px 20px",
                  borderRadius: "4px",
                  backgroundColor: "#dc3545",
                  color: "#fff",
                  border: "none",
                  cursor: "pointer",
                  transition: "background-color 0.3s ease",
                  marginRight: "10px"
                }}
                onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#c82333")}
                onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#dc3545")}
              >
                Dừng Ghi âm
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;