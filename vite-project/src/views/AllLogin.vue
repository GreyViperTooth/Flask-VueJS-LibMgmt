<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center">Login</h2>
            <form @submit.prevent="login">
              <div class="form-group">
                <label for="email">Email:</label>
                <input
                  type="email"
                  id="email"
                  v-model="credentials.email"
                  class="form-control"
                  required
                />
              </div>
              <div class="form-group">
                <label for="password">Password:</label>
                <input
                  type="password"
                  id="password"
                  v-model="credentials.password"
                  class="form-control"
                  required
                />
              </div><br>
              <button type="submit" class="btn btn-primary btn-block">Login</button>
              <!-- Display error message if any -->
              <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      credentials: {
        email: '',
        password: ''
      },
      errorMessage: ''  // Property to hold the error message
    };
  },
  methods: {
    login() {
      axios.post('http://localhost:5000/login', this.credentials)
        .then(response => {
          localStorage.setItem('user', JSON.stringify(response.data.user));
          // Redirect based on admin status
          if (response.data.user.is_admin) {
            this.$router.push('/admin-dashboard');
          } else {
            this.$router.push('/books');
          }
        })
        .catch(error => {
          // Handle specific error messages
          if (error.response && error.response.status === 401) {
            this.errorMessage = 'Invalid email or password. Please try again.';
          } else {
            this.errorMessage = 'An error occurred. Please try again later.';
          }
        });
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
.card {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
