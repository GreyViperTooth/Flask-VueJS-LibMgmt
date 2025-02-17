import axios from 'axios';

const API_URL = 'http://localhost:5000';

class BookService {
  getBooks() {
    return axios.get(`${API_URL}/books`).then(response => response.data);
  }
}

export default new BookService();
