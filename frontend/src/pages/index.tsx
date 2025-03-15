import React, { ReactNode } from "react";

import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/in-house/sidebar/app-sidebar";

interface AppWrapperProps {
  children?: ReactNode;
}

const AppWrapper: React.FC<AppWrapperProps> = () => {
  return (
    <SidebarProvider>
      <AppSidebar />
      <div className="app-content">
        <SidebarTrigger />
        <h1 className="text-blue-500">AI Hiring Copilot</h1>
      </div>
    </SidebarProvider>
  );
};

export default AppWrapper;
