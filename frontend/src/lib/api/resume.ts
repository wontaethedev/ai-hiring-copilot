import { AxiosResponse } from "axios";

import { ListClassifiedResponse } from "@/lib/models/resume";
import { apiClient } from "@/lib/helpers/api";

export const getListClassifiedResumes =
  async (): Promise<ListClassifiedResponse> => {
    const response: AxiosResponse<ListClassifiedResponse> = await apiClient.get(
      "/resume/list_classified"
    );

    return response.data;
  };

export const registerResumes = async (
  files: File[]
): Promise<void | string[]> => {
  if (!files.length) {
    return;
  }

  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  const response: AxiosResponse<string[]> = await apiClient.post(
    "/resume/register",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const processResumes = async (): Promise<string[]> => {
  const response: AxiosResponse<string[]> = await apiClient.post(
    "/resume/process"
  );

  return response.data;
};
