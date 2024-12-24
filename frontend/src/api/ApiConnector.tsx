import axios from "axios";

export const BASE_URL = "http://t123abcdefg.mooo.com:80";
const refreshToken = sessionStorage.getItem("refreshToken");

const { protocol, hostname } = window.location;
const apiProtocol = protocol === "https:" ? "https:" : "http:";
const wsProtocol = protocol === "https:" ? "wss:" : "ws:";

// Dynamically set base URLs for Spring and Django APIs
export const BASE_URL_SPRING = `${apiProtocol}//${hostname}:3000/springboot`;
export const BASE_URL_DJANGO = `${apiProtocol}//${hostname}:3000/django`;

// Dynamically set WebSocket URLs
export const WS_DJANGO_URL = `${wsProtocol}//${hostname}:3000/django`;
export const WS_SPRING_URL = `${wsProtocol}//${hostname}:3000/springboot`;

const api2 = axios.create({
  baseURL: `${BASE_URL_SPRING}`,
  headers: {
    "Content-Type": "application/json",
  },
});

export function loginUser(email: string, password: string) {
  return api2
    .post(`/api/v1/auth/login`, { email, password })
    .then((res) => res.data);
}

export function signupUser(
  email: string,
  password: string,
  firstName: string,
  lastName: string,
) {
  return api2
    .post(`/api/v1/auth/signup`, { email, password, firstName, lastName })
    .then((res) => res.data);
}

function refreshTokenRequest() {
  return api2
    .post(`/api/v1/auth/refresh`, { token: refreshToken })
    .then((response) => {
      sessionStorage.setItem("jwt", response.data.token);
      return response.data.token;
    });
}

/**
 * Create an instance of the API using the Axios library.
 *
 * @param {string} baseURL - The base URL of the API.
 * @param {string} path - (optional) The additional path of the API.
 * @returns {object} - An instance of the API.
 */
export function createAPI(baseURL: string, path?: string) {
  let url = path ? baseURL + path : baseURL;

  const api = axios.create({
    baseURL: url,
    headers: {
      "Content-Type": "application/json",
    },
  });

  api.interceptors.request.use((config) => {
    const token = sessionStorage.getItem("jwt");
    config.headers.Authorization = token ? `Bearer ${token}` : "";
    return config;
  });

  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;

      if (error.response.status === 403 && !originalRequest._retry) {
        originalRequest._retry = true;
        const newAccessToken = await refreshTokenRequest();
        axios.defaults.headers.common["Authorization"] =
          `Bearer ${newAccessToken}`;
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return axios(originalRequest);
      } else if (error.response.status === 404) {
        console.log(error.response.data);
      } else if (error.response.status === 400) {
        console.log(error.response.data);
      }

      return Promise.reject(error);
    },
  );
  return api;
}

export const springAPI = createAPI(BASE_URL_SPRING);
export const djangoAPI = createAPI(BASE_URL_DJANGO, "/api/v1");
