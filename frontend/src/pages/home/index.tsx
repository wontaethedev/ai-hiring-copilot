import React from "react";

import "@/assets/styles/common-styles.scss";

import SideBar from "@/components/side-bar";

const sideBarItems = (): React.ReactNode => (
  <>
    <div className="title">Co-Pilot</div>
    <div className="header">Candidates</div>
    <div className="sidebar-item">Very Fit</div>
    <div className="sidebar-item">Fit</div>
    <div className="sidebar-item">Unfit</div>
  </>
);

const HomePage: React.FC = () => {
  return (
    <div className="home-page c-page">
      <SideBar items={sideBarItems()} />
    </div>
  );
};

export default HomePage;
