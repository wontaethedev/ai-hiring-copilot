import React, { useEffect, useState, useCallback, useRef } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import "@/assets/styles/common-styles.scss";
import "@/pages/home/index.scss";

import { ResumeDetails } from "@/lib/models/resume";
import {
  ResumeStatusTypes,
  ResumeClassifierTypes,
  ResumeCategoryTypes,
} from "@/lib/models/product/resume";
import { RoleDetails } from "@/lib/models/role";
import { getListAllRoles } from "@/lib/api/role";
import {
  getListByFiltersResumes,
  ResumeFilters,
  registerResumes,
  processResumes,
  updateResumeStatus,
} from "@/lib/api/resume";

import SideBar from "@/components/side-bar";

type ResumeCategory =
  | {
      type: ResumeCategoryTypes;
      value: ResumeClassifierTypes;
    }
  | {
      type: ResumeCategoryTypes;
      value: ResumeStatusTypes;
    };

const HomePage: React.FC = () => {
  const [roles, setRoles] = useState<RoleDetails[]>([]);
  const [role, setRole] = useState<RoleDetails | null>(null);
  const [isRolesLoading, setIsRolesLoading] = useState<boolean>(true);
  const [isRoleOptionsVisible, setIsRoleOptionsVisible] =
    useState<boolean>(false);

  const [resumes, setResumes] = useState<ResumeDetails[]>([]);
  const [isResumesLoading, setIsResumesLoading] = useState<boolean>(true);
  const [selectedResumeCategory, setSelectedResumeCategory] =
    useState<ResumeCategory>({
      type: ResumeCategoryTypes.CLASSIFIER,
      value: ResumeClassifierTypes.VERY_FIT,
    });
  const [processedResumeIds, setProcessedResumeIds] = useState<string[]>([]);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const [error, setError] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const toggleRoleOptions = () => {
    setIsRoleOptionsVisible(!isRoleOptionsVisible);
  };

  // TODO: Refactor
  const fetchRole = async () => {
    setError(null);

    try {
      setIsRolesLoading(true);
      const result: RoleDetails[] = await getListAllRoles();
      setRoles(result);
      // Assign first role as default
      // TODO: Add "default role/last selected role as default" functionality
      setRole(result[0]);
    } catch (err) {
      setError("Failed to fetch roles");
      console.error("Error fetching roles:", err);
    } finally {
      setIsRolesLoading(false);
    }
  };

  const fetchResumes = useCallback(async () => {
    setError(null);

    if (!role) {
      setIsResumesLoading(false);
      return;
    }

    const filters: ResumeFilters = {
      role_id: role.id,
    };

    if (selectedResumeCategory.type === ResumeCategoryTypes.CLASSIFIER) {
      filters.status = ResumeStatusTypes.COMPLETE;
      filters.classifier =
        selectedResumeCategory.value as ResumeClassifierTypes;
    } else {
      filters.status = selectedResumeCategory.value as ResumeStatusTypes;
    }

    try {
      setIsResumesLoading(true);
      const result: ResumeDetails[] = await getListByFiltersResumes(filters);
      setResumes(result);
    } catch (err) {
      setError("Failed to fetch resumes");
      console.error("Error fetching resumes:", err);
    } finally {
      setIsResumesLoading(false);
    }
  }, [role, selectedResumeCategory.type, selectedResumeCategory.value]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFiles(Array.from(e.target.files));
    }
  };

  const handleUpload = async () => {
    setError(null);

    if (!role) {
      setError("Please create a role");
      return;
    }

    try {
      const result: string[] | void = await registerResumes(
        role.id,
        selectedFiles
      );
      console.log("Registering success", result);
    } catch (err) {
      setError("Failed to upload files");
      console.error("Error fetching data:", err);
    } finally {
      setSelectedFiles([]);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleProcess = async () => {
    setProcessedResumeIds([]);
    setError(null);

    try {
      const result: string[] = await processResumes();
      console.log("Processing success", result);
      setProcessedResumeIds(result);
      await fetchResumes();
    } catch (err) {
      setError("Failed to process resumes");
      console.error("Error processing data:", err);
    }
  };

  const handleUpdateResumeStatus = async (
    id: string,
    status: ResumeStatusTypes
  ) => {
    setError(null);

    try {
      const result: boolean = await updateResumeStatus(id, status);
      console.log("Update status success", result);
      await fetchResumes();
    } catch (err) {
      setError("Failed to update resume status");
      console.error("Error processing data:", err);
    }
  };

  useEffect(() => {
    fetchRole();
  }, []);

  useEffect(() => {
    fetchResumes();
  }, [role, fetchResumes]);

  const sideBarItems = (): React.ReactNode => (
    <>
      <div className="title">Co-Pilot</div>
      <div className="header">Candidates</div>
      <div
        className="sidebar-item"
        onClick={() =>
          setSelectedResumeCategory({
            type: ResumeCategoryTypes.CLASSIFIER,
            value: ResumeClassifierTypes.VERY_FIT,
          })
        }
      >
        Very Fit
      </div>
      <div
        className="sidebar-item"
        onClick={() =>
          setSelectedResumeCategory({
            type: ResumeCategoryTypes.CLASSIFIER,
            value: ResumeClassifierTypes.FIT,
          })
        }
      >
        Fit
      </div>
      <div
        className="sidebar-item"
        onClick={() =>
          setSelectedResumeCategory({
            type: ResumeCategoryTypes.CLASSIFIER,
            value: ResumeClassifierTypes.UNFIT,
          })
        }
      >
        Unfit
      </div>
      <div className="header">Assessed</div>
      <div
        className="sidebar-item"
        onClick={() =>
          setSelectedResumeCategory({
            type: ResumeCategoryTypes.STATUS,
            value: ResumeStatusTypes.ASSESSED_FIT,
          })
        }
      >
        Fit
      </div>
      <div
        className="sidebar-item"
        onClick={() =>
          setSelectedResumeCategory({
            type: ResumeCategoryTypes.STATUS,
            value: ResumeStatusTypes.ASSESSED_HOLD,
          })
        }
      >
        Hold
      </div>
      <div
        className="sidebar-item"
        onClick={() =>
          setSelectedResumeCategory({
            type: ResumeCategoryTypes.STATUS,
            value: ResumeStatusTypes.ASSESSED_UNFIT,
          })
        }
      >
        Unfit
      </div>
    </>
  );

  const errorContent = (): React.ReactNode => (
    <>
      <p className="error-msg">Error: {error}</p>
    </>
  );

  const content = (): React.ReactNode => (
    <>
      {resumes.length > 0 ? (
        resumes.map((resume) => {
          return (
            <div key={resume.id} className="resume-container">
              <div className="left-items">
                <div className="attribute">ID: {resume.id}</div>
                <div className="attribute">
                  Base Requirement Satisfaction Score:{" "}
                  {resume.base_requirement_satisfaction_score}
                </div>
                <div className="attribute">
                  Exceptional Considerations:{" "}
                  {resume.exceptional_considerations}
                </div>
                <div className="attribute">
                  Fitness Score: {resume.fitness_score}
                </div>
              </div>
              <div className="right-items">
                <button>
                  <FontAwesomeIcon
                    className="classify-icon"
                    icon={["fas", "thumbs-up"]}
                    onClick={() =>
                      handleUpdateResumeStatus(
                        resume.id,
                        ResumeStatusTypes.ASSESSED_FIT
                      )
                    }
                  />
                </button>
                <button>
                  <FontAwesomeIcon
                    className="classify-icon"
                    icon={["fas", "hand"]}
                    onClick={() =>
                      handleUpdateResumeStatus(
                        resume.id,
                        ResumeStatusTypes.ASSESSED_HOLD
                      )
                    }
                  />
                </button>
                <button>
                  <FontAwesomeIcon
                    className="classify-icon"
                    icon={["fas", "thumbs-down"]}
                    onClick={() =>
                      handleUpdateResumeStatus(
                        resume.id,
                        ResumeStatusTypes.ASSESSED_UNFIT
                      )
                    }
                  />
                </button>
              </div>
            </div>
          );
        })
      ) : (
        <p className="system-msg">There are no resumes</p>
      )}
    </>
  );

  return (
    <div className="home-page c-page">
      <SideBar items={sideBarItems()} />

      {/* Content */}
      <div className="c-content">
        <div className="role-selector">
          <div className="current-role" onClick={() => toggleRoleOptions()}>
            {role?.name || "Select a role"}{" "}
            <FontAwesomeIcon
              className="toggle-options-icon"
              icon={
                isRoleOptionsVisible
                  ? ["fas", "chevron-up"]
                  : ["fas", "chevron-down"]
              }
            />
          </div>
          <div
            className={`options-container ${
              isRoleOptionsVisible ? "visible" : ""
            }`}
          >
            {roles.length > 0 &&
              roles.map((role) => {
                return (
                  <div
                    key={role.id}
                    className="option"
                    onClick={() => setRole(role)}
                  >
                    {role.name}
                  </div>
                );
              })}
          </div>
        </div>
        <div className="border" />
        {/* Upload resumes */}
        <div className="upload-resumes-container">
          <div className="left-items">
            {/* File uploader - TODO: Move to component */}
            <div className="file-uploader">
              <input
                id="file-input"
                multiple
                ref={fileInputRef}
                type="file"
                onChange={handleFileChange}
              />
              <label htmlFor="file-input">
                <div className="c-button">Choose Files</div>
              </label>
            </div>
            <div className="file-preview">
              {selectedFiles.length > 0 && `${selectedFiles.length} Files`}
            </div>
          </div>

          <div className="right-items">
            {/* Create button - TODO: Move to component */}
            <button className="c-button" onClick={() => handleUpload()}>
              Upload Resumes
            </button>
          </div>
        </div>
        {/* Process resumes */}
        <div className="process-resumes-container">
          <button className="c-button" onClick={() => handleProcess()}>
            Process uploaded resumes
          </button>
          <div className="processed-resumes-preview">
            {`${processedResumeIds.length} Files Processed`}
          </div>
        </div>
        <div className="border" />
        {isResumesLoading || isRolesLoading
          ? loadingContent()
          : error
          ? errorContent()
          : content()}
      </div>
    </div>
  );
};

const loadingContent = (): React.ReactNode => (
  <>
    <p className="system-msg">Loading...</p>
  </>
);

export default HomePage;
