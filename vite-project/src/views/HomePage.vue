<template>
    <div class="home-page">
      <div class="content">
        <h1>Welcome to the Sentinel Library</h1>
        <blockquote>
          "A room without books is like a body without a soul." – Cicero
        </blockquote>
        <img src="/root/madII/vite-project/src/assets/library-image.jpg" alt="Library Image" class="library-image" />
        <button class="shop-button" @click="proceed">Proceed to Shop ></button>
      </div>
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'Home',
    setup() {
      const router = useRouter();
  
      function proceed() {
        const user = JSON.parse(localStorage.getItem('user'));
  
        if (user) {
          if (user.is_admin) {
            router.push('/admin-dashboard');
          } else {
            router.push('/books');
          }
        } else {
          router.push('/login');
        }
      }
  
      return { proceed };
    }
  };
  </script>
  
  <style scoped>
  .home-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: linear-gradient(to right, #f0f4f8, #d9e2ec);
    padding: 10px;
  }
  
  .content {
    text-align: center;
    max-width: 800px;
    background: #ffffff;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #f9f9f9;
  }
  
  h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
    color: #333;
    background-color: #e0f7fa;
    padding: 10px;
    border-radius: 8px;
  }
  
  p {
    font-size: 1.2em;
    margin-bottom: 20px;
    color: #666;
    background-color: #e8f5e9;
    padding: 10px;
    border-radius: 8px;
  }
  
  blockquote {
    font-size: 1.1em;
    margin: 10px 0;
    padding: 05px 10px;
    border-left: 4px solid #4CAF50;
    color: #555;
    font-style: italic;
    background-color: #fffde7;
    border-radius: 8px;
  }
  
  .library-image {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 20px 0;
  }
  
  .shop-button {
    padding: 12px 24px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1.1em;
    transition: background-color 0.3s ease;
    display: block;
    margin: 20px auto;
  }
  
  .shop-button:hover {
    background-color: #45a049;
  }
  </style>
  