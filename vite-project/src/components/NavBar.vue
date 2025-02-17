<template>
  <nav>
    <div class="nav-container">
      <router-link to="/" class="nav-logo">Sentinel Library</router-link>
      <div class="nav-links">
        <!-- New Home Link -->
        <router-link v-if="user" to="/books" class="nav-item">Home</router-link>
        
        <!-- Existing Links -->
        <!-- <router-link v-if="!user" to="/admin-signup" class="nav-item">Admin Signup</router-link> -->
        <router-link v-if="!user" to="/signup" class="nav-item">User Signup</router-link>
        <router-link v-if="!user" to="/login" class="nav-item">Login</router-link>
        <router-link v-if="user" to="/profile" class="nav-item">Profile</router-link>
        <button v-if="user" @click="logout" class="nav-item logout-button">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      user: JSON.parse(localStorage.getItem('user')) || null
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('user');
      this.$router.push('/login');
    }
  },
  watch: {
    '$route'(to, from) {
      this.user = JSON.parse(localStorage.getItem('user')) || null;
    }
  }
};
</script>

<style scoped>
nav {
  background-color: #333;
  color: #fff;
  padding: 10px;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-logo {
  font-size: 1.5em;
  color: #fff;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 10px;
}

.nav-item {
  color: #fff;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 5px;
}

.nav-item:hover {
  background-color: #555;
}

.logout-button {
  background-color: #e74c3c;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

.logout-button:hover {
  background-color: #c0392b;
}
</style>
