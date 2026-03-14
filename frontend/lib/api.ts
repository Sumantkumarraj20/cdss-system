import axios, { type AxiosRequestHeaders } from "axios";

const baseURL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.trim() || "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL,
  withCredentials: true,
});

export function setAuthToken(token: string | null) {
  if (typeof window === "undefined") return;
  if (token) {
    localStorage.setItem("cdss_token", token);
  } else {
    localStorage.removeItem("cdss_token");
  }
}

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("cdss_token");
    if (token) {
      const headers = (config.headers || {}) as AxiosRequestHeaders;
      (headers as any)["Authorization"] = `Bearer ${token}`;
      config.headers = headers;
    }
  }
  return config;
});
