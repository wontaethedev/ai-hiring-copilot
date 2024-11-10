import React, { useEffect, useState } from "react";

import "@/assets/styles/common-styles.scss";
import "@/pages/home/index.scss";

import { HealthData } from "@/lib/models/home";
import { getHealth } from "@/lib/api/dev";

const HomePage: React.FC = () => {
  const [healthData, setHealthData] = useState<HealthData | null>(null);
  const [isHealthDataLoading, setIsHealthDataLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsHealthDataLoading(true);
        const result = await getHealth();
        setHealthData(result);
      } catch (err) {
        setError("Failed to fetch data");
        console.error("Error fetching data:", err);
      } finally {
        setIsHealthDataLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="home-page c-page">
      {isHealthDataLoading ? (
        <span>Loading...</span>
      ) : error ? (
        <span>{error}</span>
      ) : (
        <>
          <span>{healthData?.healthy ? "Healthy::" : "Not Healthy::"}</span>
          <span>{healthData?.message}</span>
        </>
      )}
    </div>
  );
};

export default HomePage;
