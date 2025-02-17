import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Update with your Flask server URL

class AuthService {
  login(username, password) {
    return axios.post(`${API_URL}/login`, { username, password });
  }
  signup(username, password) {
    return axios.post(`${API_URL}/signup`, { username, password });
  }
  adminSignup(username, password, securityAnswer) {
    return axios.post(`${API_URL}/admin-signup`, { username, password, securityAnswer });
  }
}

export default new AuthService();
