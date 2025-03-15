import React, { ReactNode } from "react";

interface AppWrapperProps {
  children?: ReactNode;
}

const AppWrapper: React.FC<AppWrapperProps> = () => {
  return (
    <div className="app-wrapper">
      <header>
        <h1 className="text-blue-500">AI Hiring Copilot</h1>
      </header>
      <footer>
        <p>AI Hiring Copilot</p>
      </footer>
    </div>
  );
};

export default AppWrapper;
