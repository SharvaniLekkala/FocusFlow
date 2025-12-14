import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const registerUser = (data) =>
  API.post("/register", data);

export const loginUser = (data) =>
  API.post("/login", data);
export const createSession = (data, token) =>
  API.post("/sessions", data, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const getSessions = (token) =>
  API.get("/sessions", {
    headers: { Authorization: `Bearer ${token}` },
  });

export const getInsights = (token) =>
  API.get("/insights", {
    headers: { Authorization: `Bearer ${token}` },
  });
export const clearTodaySessions = (token) =>
  API.delete("/sessions/today", {
    headers: { Authorization: `Bearer ${token}` },
  });

export const getSummary = (range, token) =>
  API.get(`/summary/${range}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
