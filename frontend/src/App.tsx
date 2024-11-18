import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import LandingWrapper from "@/pages";
import HomePage from "@/pages/home";
import SettingsPage from "@/pages/settings";

const App: React.FC = () => {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingWrapper />}>
            <Route index element={<HomePage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
