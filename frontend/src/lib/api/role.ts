import { AxiosResponse } from "axios";

import { RoleDetails } from "@/lib/models/role";
import { apiClient } from "@/lib/helpers/api";

export const getListAllRoles = async (): Promise<RoleDetails[]> => {
  const response: AxiosResponse<RoleDetails[]> = await apiClient.get(
    "/role/list_all"
  );

  return response.data;
};

export const registerRole = async (
  name: string,
  file: File
): Promise<void | string> => {
  if (!file || !name) {
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);

  const response: AxiosResponse<string> = await apiClient.post(
    "/role/register",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};
