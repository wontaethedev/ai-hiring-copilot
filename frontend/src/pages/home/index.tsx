import React, { useEffect, useState } from "react";

import "@/assets/styles/common-styles.scss";
import "@/pages/home/index.scss";

import { ResumeClassifierTypes } from "@/lib/models/product/resume";
import { ListClassifiedResponse, ResumeDetails } from "@/lib/models/resume";
import { getListClassifiedResumes } from "@/lib/api/resume";

const HomePage: React.FC = () => {
  const [veryFitResumes, setVeryFitResumes] = useState<ResumeDetails[]>([]);
  const [fitResumes, setFitResumes] = useState<ResumeDetails[]>([]);
  const [notFitResumes, setNotFitResumes] = useState<ResumeDetails[]>([]);

  const [isResumeDataLoading, setIsResumeDataLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedClassifier, setSelectedClassifier] =
    useState<ResumeClassifierTypes>(ResumeClassifierTypes.OUTSTANDING);

  const selectClassifier = (classifier: ResumeClassifierTypes) => {
    setSelectedClassifier(classifier);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsResumeDataLoading(true);
        const result: ListClassifiedResponse = await getListClassifiedResumes();
        setVeryFitResumes(result.very_fit);
        setFitResumes(result.fit);
        setNotFitResumes(result.not_fit);
      } catch (err) {
        setError("Failed to fetch data");
        console.error("Error fetching data:", err);
      } finally {
        setIsResumeDataLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isResumeDataLoading)
    return (
      <div className="home-page">
        <p>Loading...</p>
      </div>
    );
  if (error)
    return (
      <div className="home-page">
        <p>Error: {error}</p>
      </div>
    );

  return (
    <div className="home-page c-page">
      <div className="resume-classifier">
        <div className="classifier-menu">
          <h1 className="title">HR Copilot</h1>
          <button
            className="classifier"
            onClick={() => selectClassifier(ResumeClassifierTypes.OUTSTANDING)}
          >
            Outstanding
          </button>
          <button
            className="classifier"
            onClick={() => selectClassifier(ResumeClassifierTypes.FIT)}
          >
            Fit
          </button>
          <button
            className="classifier"
            onClick={() => selectClassifier(ResumeClassifierTypes.UNFIT)}
          >
            Unfit
          </button>
        </div>

        <div className="candidate-details-list">
          {
            selectedClassifier == ResumeClassifierTypes.OUTSTANDING
              ? ResumeSection(veryFitResumes)
              : selectedClassifier == ResumeClassifierTypes.FIT
              ? ResumeSection(fitResumes)
              : selectedClassifier == ResumeClassifierTypes.UNFIT
              ? ResumeSection(notFitResumes)
              : ResumeSection(veryFitResumes) // Should not happen
          }
        </div>
      </div>
    </div>
  );
};

const ResumeSection = (resumes: ResumeDetails[]): React.ReactNode => {
  if (resumes.length <= 0) {
    return <p>No candidates</p>;
  }

  return resumes.map((resume) => (
    <div className="candidate-details" key={resume.id}>
      <div className="attribute">ID: {resume.id}</div>
      <div className="attribute">
        Base requirement satisfaction score:{" "}
        {resume.base_requirement_satisfaction_score}
      </div>
      <div className="attribute">
        Exceptional considerations: {resume.exceptional_considerations}
      </div>
      <div className="attribute">Fitness score: {resume.fitness_score}</div>
    </div>
  ));
};

export default HomePage;
