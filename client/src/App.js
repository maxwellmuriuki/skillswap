import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import UserPage from "./pages/userPage";
import HomePage from "./pages/HomePage";
import AddNewUser from "./pages/AddNewUser";  // Renamed from UserAuth
import "./App.css";

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/users" element={<UserPage />} />
        <Route path="/auth" element={<AddNewUser />} /> {/* Renamed route */}
      </Routes>
    </div>
  );
}

export default App;
