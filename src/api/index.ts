import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://47.242.151.196:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000, // 5秒超时
});


export default apiClient;