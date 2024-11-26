import React from "react";

import "@/components/side-bar/index.scss";

type Sidebaritems = {
  items: React.ReactNode;
};

const SideBar: React.FC<Sidebaritems> = ({ items }) => {
  return <div className="side-bar">{items}</div>;
};

export default SideBar;
