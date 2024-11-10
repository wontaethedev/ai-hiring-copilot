import { AxiosResponse } from "axios";

import { HealthData } from "@/lib/models/home";
import { apiClient } from "@/lib/helpers/api";

export const getHealth = async (): Promise<HealthData> => {
  const response: AxiosResponse<HealthData> = await apiClient.post("/dev/", {
    message: "from frontend",
  });

  return response.data;
};
