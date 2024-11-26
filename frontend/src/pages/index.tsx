import React from "react";
import { Outlet } from "react-router-dom";

import "@/assets/styles/common-styles.scss";
import "@/pages/index.scss";

import NavBar from "@/components/nav-bar";

const LandingWrapper: React.FC = () => {
  return (
    <div className="landing-wrapper">
      <NavBar />
      <Outlet />
    </div>
  );
};

export default LandingWrapper;
