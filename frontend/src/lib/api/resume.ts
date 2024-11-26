import { AxiosResponse } from "axios";

import { ResumeDetails } from "@/lib/models/resume";
import {
  ResumeStatusTypes,
  ResumeClassifierTypes,
} from "@/lib/models/product/resume";
import { apiClient } from "@/lib/helpers/api";

export type ResumeFilters = {
  role_id: string;
  status?: ResumeStatusTypes;
  classifier?: ResumeClassifierTypes;
};

export const getListByFiltersResumes = async (
  filters: ResumeFilters
): Promise<ResumeDetails[]> => {
  const response: AxiosResponse<ResumeDetails[]> = await apiClient.get(
    "/resume/list_by_filters",
    { params: filters }
  );

  return response.data;
};

export const registerResumes = async (
  role_id: string,
  files: File[]
): Promise<void | string[]> => {
  if (!files.length) {
    return;
  }

  const formData = new FormData();
  formData.append("role_id", role_id);
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

export const updateResumeStatus = async (
  role_id: string,
  status: ResumeStatusTypes
): Promise<boolean> => {
  const formData = new FormData();
  formData.append("id", role_id);
  formData.append("status", status);

  const response: AxiosResponse<boolean> = await apiClient.post(
    "/resume/update_status",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};
