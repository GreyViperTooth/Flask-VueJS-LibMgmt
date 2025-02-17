import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';


const app = createApp(App);
app.use(router);

app.config.globalProperties.$axios = axios;
app.config.globalProperties.$login = async (email, password) => {
  try {
    const response = await axios.post('http://localhost:5000/login', { email, password });
    localStorage.setItem('user_id', response.data.user_id);
    localStorage.setItem('user_name', response.data.user_name);
    localStorage.setItem('is_admin', response.data.is_admin);
    return response;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

app.config.globalProperties.$logout = async () => {
  try {
    await axios.post('http://localhost:5000/logout');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_name');
    localStorage.removeItem('is_admin');
  } catch (error) {
    console.error('Logout error:', error);
    throw error;
  }
};

app.mount('#app');
