import axios, { AxiosInstance } from "axios";

// Should be moved to a config/env file
const API_BASE_URL: string = "http://localhost:8000";

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});
