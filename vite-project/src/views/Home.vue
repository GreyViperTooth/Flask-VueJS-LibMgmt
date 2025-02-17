<template>
    <div>
      <h1>Library Management System</h1>
      <h2>Books</h2>
      <ul>
        <li v-for="book in books" :key="book.id">
          <router-link :to="{ path: `/books/${book.id}` }">{{ book.title }}</router-link>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        books: [/* Book data from API or hardcoded */]
      };
    },
    created() {
      // Fetch books data from API or set hardcoded data
    }
  };
  </script>
  