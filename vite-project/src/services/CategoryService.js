import axios from 'axios';

const API_URL = 'http://localhost:5000/api/categories';

export default {
  getCategories() {
    return axios.get(API_URL);
  },
  getCategory(id) {
    return axios.get(`${API_URL}/${id}`);
  }
};
