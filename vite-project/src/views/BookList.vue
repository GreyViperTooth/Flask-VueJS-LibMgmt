<template>
  <div class="container mt-5">
    <h1 class="mb-4">Book List</h1>
    <input type="text" v-model="searchQuery" placeholder="Search for books or categories..." class="form-control mb-4" />
    
    <div v-for="category in filteredBooks" :key="category.category" class="category-section">
      <h2>{{ category.category }}</h2>
      <div class="books-container">
        <div v-for="book in category.books" :key="book.id" class="book-item">
          <router-link :to="'/books/' + book.id">
            <div class="book-cover-wrapper">
              <img :src="book.cover_image ? book.cover_image : require('@/assets/placeholder.jpeg')" alt="Book Cover" class="book-cover">
            </div>
            <div class="book-info">
              <h3>{{ book.title }}</h3>
              <p>{{ book.author }}</p>
            </div>
          </router-link>
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
      books: [],
      searchQuery: "" // Add a data property for search query
    };
  },
  created() {
    this.fetchBooks();
  },
  computed: {
    filteredBooks() {
      // Filter categories and books based on the search query
      const query = this.searchQuery.toLowerCase();
      return this.books
        .map(category => {
          const filteredBooks = category.books.filter(book =>
            book.title.toLowerCase().includes(query) ||
            book.author.toLowerCase().includes(query)
          );
          if (category.category.toLowerCase().includes(query) || filteredBooks.length > 0) {
            return {
              category: category.category,
              books: filteredBooks
            };
          }
          return null;
        })
        .filter(category => category !== null); // Remove empty categories
    }
  },
  methods: {
    fetchBooks() {
      const apiUrl = process.env.NODE_ENV === 'production' ? 'https://your-production-url.com/books' : 'http://localhost:5000/books';
      
      axios.get(apiUrl)
        .then(response => {
          this.books = response.data;
        })
        .catch(error => {
          console.error("Error fetching books:", error);
        });
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.category-section {
  margin-bottom: 40px;
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
}

.category-section h2 {
  margin-bottom: 20px;
  border-bottom: 2px solid #ddd;
  padding-bottom: 5px;
}

.books-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.book-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 8px;
  width: calc(25% - 20px);
  box-sizing: border-box;
}

.book-cover-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 200px;
  overflow: hidden;
  margin-bottom: 10px;
}

.book-cover {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.book-info {
  text-align: center;
}

input.form-control {
  margin-bottom: 20px;
}
</style>
