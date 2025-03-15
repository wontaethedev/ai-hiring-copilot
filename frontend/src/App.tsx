import React from "react";
import { BrowserRouter, Routes } from "react-router-dom";

const App: React.FC = () => {
  return (
    <>
      <BrowserRouter>
        <Routes>
          {/* <Route path="/" element={<LandingWrapper />}>
            <Route index element={<HomePage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route> */}
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
