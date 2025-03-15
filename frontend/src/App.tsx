import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import AppWrapper from "@/pages";

const App: React.FC = () => {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppWrapper />}></Route>
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
