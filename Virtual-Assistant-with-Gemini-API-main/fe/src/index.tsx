import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App"; // App chính
import TranscribePage from "./app/dashboard/Transcribe/page"; // Trang Transcribe
import TroChuyenPage from "./app/dashboard/Document_Processing/page"; // Trang Trò Chuyện

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        {/* Route chính */}
        <Route path="/" element={<App />} /> 

        {/* Routes trong dashboard */}
        <Route path="/dashboard/transcribe" element={<TranscribePage />} /> 
        <Route path="/dashboard/document_processing" element={<TroChuyenPage />} /> 
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
