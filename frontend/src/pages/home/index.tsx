import React, { useEffect, useState, useCallback } from "react";

import "@/assets/styles/common-styles.scss";

import { ResumeDetails } from "@/lib/models/resume";
import {
  ResumeStatusTypes,
  ResumeClassifierTypes,
} from "@/lib/models/product/resume";
import { RoleDetails } from "@/lib/models/role";
import { getListAllRoles } from "@/lib/api/role";
import { getListByFiltersResumes, ResumeFilters } from "@/lib/api/resume";

import SideBar from "@/components/side-bar";

const HomePage: React.FC = () => {
  const [role, setRole] = useState<RoleDetails | null>(null);
  const [isRoleLoading, setIsRoleLoading] = useState<boolean>(true);

  const [resumes, setResumes] = useState<ResumeDetails[]>([]);
  const [isResumesLoading, setIsResumesLoading] = useState<boolean>(true);

  const [error, setError] = useState<string | null>(null);

  const [selectedClassifier, setSelectedClassifier] =
    useState<ResumeClassifierTypes>(ResumeClassifierTypes.VERY_FIT);

  // TODO: Refactor
  const fetchRole = async () => {
    try {
      setIsRoleLoading(true);
      const result: RoleDetails[] = await getListAllRoles();
      // Assign first role as default
      // TODO: Add "default role/last selected role as default" functionality
      setRole(result[0]);
    } catch (err) {
      setError("Failed to fetch roles");
      console.error("Error fetching roles:", err);
    } finally {
      setIsRoleLoading(false);
    }
  };

  // Fetch resumes whenever role or classifier changes
  const fetchResumes = useCallback(
    async (status?: ResumeStatusTypes) => {
      if (!role) {
        return;
      }

      const filters: ResumeFilters = {
        role_id: role.id,
        status: status,
        classifier: selectedClassifier,
      };

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
    },
    [role, selectedClassifier] // Dependencies
  );

  useEffect(() => {
    fetchRole();
  }, []);

  useEffect(() => {
    if (role) {
      fetchResumes();
    }
  }, [role, fetchResumes]);

  const sideBarItems = (): React.ReactNode => (
    <>
      <div className="title">Co-Pilot</div>
      <div className="header">Candidates</div>
      <div
        className="sidebar-item"
        onClick={() => setSelectedClassifier(ResumeClassifierTypes.VERY_FIT)}
      >
        Very Fit
      </div>
      <div
        className="sidebar-item"
        onClick={() => setSelectedClassifier(ResumeClassifierTypes.FIT)}
      >
        Fit
      </div>
      <div
        className="sidebar-item"
        onClick={() => setSelectedClassifier(ResumeClassifierTypes.UNFIT)}
      >
        Unfit
      </div>
    </>
  );

  const errorContent = (): React.ReactNode => (
    <>
      <p>Error: {error}</p>
    </>
  );

  const content = (): React.ReactNode => (
    <>
      {resumes.length > 0 ? (
        resumes.map((resume) => {
          return (
            <div key={resume.id} className="resume-container">
              <div className="attribute">{resume.id}</div>
              <div className="attribute">
                {resume.base_requirement_satisfaction_score}
              </div>
              <div className="attribute">
                {resume.exceptional_considerations}
              </div>
              <div className="attribute">{resume.fitness_score}</div>
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
        {isResumesLoading || isRoleLoading
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
