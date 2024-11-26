import React from "react";
import { Link } from "react-router-dom";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import "@/components/nav-bar/index.scss";

const NavBar: React.FC = () => {
  return (
    <div className="nav-bar">
      <div className="menu-item">
        <Link to="/" className="icon">
          <FontAwesomeIcon icon={["fas", "list-check"]} />
        </Link>
      </div>
      <div className="menu-item">
        <Link to="/settings" className="icon">
          <FontAwesomeIcon icon={["fas", "gear"]} />
        </Link>
      </div>
    </div>
  );
};

export default NavBar;
