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
