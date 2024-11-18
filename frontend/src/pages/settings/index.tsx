import React from "react";

import "@/assets/styles/common-styles.scss";

import SideBar from "@/components/side-bar";

const sideBarItems = (): React.ReactNode => (
  <>
    <div className="title">Settings</div>
    <div className="header">Roles</div>
  </>
);

const SettingsPage: React.FC = () => {
  return (
    <div className="settings-page c-page">
      <SideBar items={sideBarItems()} />
    </div>
  );
};

export default SettingsPage;
