import React from "react";
import { Routes, Route } from "react-router-dom";
import IntroPage from "./IntroPage";
import App from "./App";

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<IntroPage />} />
      <Route path="/main" element={<App />} />
    </Routes>
  );
}
