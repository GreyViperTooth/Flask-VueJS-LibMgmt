<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h1 class="card-title text-center">User Signup</h1>
            <form @submit.prevent="signup">
              <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" v-model="name" class="form-control" required />
              </div>
              <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="email" class="form-control" required />
              </div>
              <div class="form-group">
                <label for="mobile">Mobile:</label>
                <input type="text" id="mobile" v-model="mobile" class="form-control" required />
              </div>
              <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" class="form-control" required />
              </div><br>
              <button type="submit" class="btn btn-primary btn-block">Signup</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      email: '',
      mobile: '',
      password: ''
    };
  },
  methods: {
    async signup() {
      try {
        const response = await fetch('http://localhost:5000/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            mobile: this.mobile,
            password: this.password
          })
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.$router.push('/login');
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error(error);
      }
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
