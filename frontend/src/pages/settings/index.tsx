import React, { useEffect, useState, useRef } from "react";

import "@/assets/styles/common-styles.scss";
import "@/pages/settings/index.scss";

import SideBar from "@/components/side-bar";

import { getListAllRoles, registerRole } from "@/lib/api/role";
import { RoleDetails } from "@/lib/models/role";

const SettingsPage: React.FC = () => {
  const [roles, setRoles] = useState<RoleDetails[]>([]);
  const [isRoleLoading, setIsRoleLoading] = useState<boolean>(true);

  const [newRoleName, setNewRoleName] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [error, setError] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleNewRoleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNewRoleName(e.target.value); // Update the state as the user types
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  // TODO: Refactor
  const fetchRole = async () => {
    try {
      setIsRoleLoading(true);
      const result: RoleDetails[] = await getListAllRoles();
      setRoles(result);
    } catch (err) {
      setError("Failed to fetch data");
      console.error("Error fetching data:", err);
    } finally {
      setIsRoleLoading(false);
    }
  };

  const createNewRole = async () => {
    if (!selectedFile) {
      return;
    }

    try {
      const result: string | void = await registerRole(
        newRoleName,
        selectedFile
      );
      console.log("Create new role success", result);
    } catch (err) {
      // TODO: Replace with notification
      console.error("Error: ", err);
    } finally {
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
      await fetchRole();
    }
  };

  useEffect(() => {
    fetchRole();
  }, []);

  // TODO: Refactor
  const errorContent = (): React.ReactNode => (
    <>
      <p>Error: {error}</p>
    </>
  );

  // TODO: Refactor
  const content = (): React.ReactNode => (
    <>
      {roles.length > 0 ? (
        roles.map((role) => {
          return (
            <div key={role.id} className="role-container">
              <p>{role.name}</p>
            </div>
          );
        })
      ) : (
        <p className="system-msg">Please create a role</p>
      )}
    </>
  );

  return (
    <div className="settings-page c-page">
      <SideBar items={sideBarItems()} />

      {/* Content */}
      <div className="c-content">
        {/* Create role */}
        <div className="create-role-container">
          <div className="left-items">
            {/* File uploader - TODO: Move to component */}
            <div className="file-uploader">
              <input
                id="file-input"
                ref={fileInputRef}
                type="file"
                onChange={handleFileChange}
              />
              <label htmlFor="file-input">
                <div className="c-button">Choose a File</div>
              </label>
            </div>
            <div className="file-preview">
              {selectedFile && selectedFile.name}
            </div>

            {/* Name input */}
            <div className="text-field-container">
              <label htmlFor="text-input" className="text-label">
                Name:
              </label>
              <input
                id="text-input"
                type="text"
                value={newRoleName}
                onChange={handleNewRoleNameChange}
                className="text-input"
                placeholder="Enter your role name"
              />
            </div>
          </div>

          <div className="right-items">
            {/* Create button - TODO: Move to component */}
            <button className="c-button" onClick={() => createNewRole()}>
              Create
            </button>
          </div>
        </div>

        {/* Role list */}
        <div className="roles-table">
          {isRoleLoading
            ? loadingContent()
            : error
            ? errorContent()
            : content()}
        </div>
      </div>
    </div>
  );
};

const loadingContent = (): React.ReactNode => (
  <>
    <p className="system-msg">Loading...</p>
  </>
);

const sideBarItems = (): React.ReactNode => (
  <>
    <div className="title">Settings</div>
    <div className="header">Roles</div>
  </>
);

export default SettingsPage;
