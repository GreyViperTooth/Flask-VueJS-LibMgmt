<template>
  <div class="container">
    <div class="details-card">
      <img :src="book.cover_image" alt="Book Cover" v-if="book.cover_image" class="book-image">
      <div class="book-info">
        <h1>{{ book.title }}</h1>
        <p class="author">{{ book.author }}</p>
        <p class="description">{{ book.description }}</p>
        
        <!-- Button to open the PDF in a new tab -->
        <a v-if="hasBorrowed" :href="book.pdf_file" target="_blank" class="pdf-button">
          Open PDF in new tab
        </a>
        <br><br>
        <!-- Display PDF in card if user chooses to view it here -->
        <button v-if="hasBorrowed && !showPdf" @click="showPdf = true" class="view-pdf-button">
          View PDF
        </button>
        <br>
        <button v-if="showPdf && hasBorrowed" @click="showPdf = false" class="hide-pdf-button">
          Hide PDF
        </button>
        <!-- Conditionally render the PDF viewer -->
        <iframe v-if="showPdf && book.pdf_file" :src="book.pdf_file" class="pdf-viewer"></iframe>
        <button v-if="!hasBorrowed" @click="borrowBook" class="borrow-button">Borrow Book</button>
        <button v-if="hasBorrowed" @click="returnBook" class="return-button">Return Book</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['id'],
  data() {
    return {
      book: {},
      hasBorrowed: false,
      showPdf: false  // Track whether the PDF should be displayed
    };
  },
  created() {
    this.fetchBookDetails();
    this.checkIfBorrowed();
  },
  methods: {
    fetchBookDetails() {
      axios.get(`http://localhost:5000/books/${this.id}`)
        .then(response => {
          this.book = response.data;
        })
        .catch(error => {
          console.error('Error fetching book details:', error);
        });
    },
    borrowBook() {
      const userId = JSON.parse(localStorage.getItem('user')).id;
      
      // Check the number of books the user has already borrowed
      axios.get(`http://localhost:5000/borrowed-books/${userId}`)
        .then(response => {
          const borrowedBooksCount = response.data.length;

          if (borrowedBooksCount >= 5) {
            // Show alert if the user has already borrowed 5 books
            alert('You cannot borrow more than 5 books at a time.');
          } else {
            // Proceed to borrow the book
            axios.post('http://localhost:5000/borrow', {
              user_id: userId,
              book_id: this.book.id,
              borrowed_date: new Date().toISOString()
            })
            .then(response => {
              this.hasBorrowed = true;
              alert('Book borrowed successfully!');
            })
            .catch(error => {
              console.error('Error borrowing book:', error);
            });
          }
        })
        .catch(error => {
          console.error('Error checking borrowed books count:', error);
        });
    },
    returnBook() {
      const userId = JSON.parse(localStorage.getItem('user')).id;
      axios.post('http://localhost:5000/return', {
        user_id: userId,
        book_id: this.book.id,
        return_date: new Date().toISOString()
      })
      .then(response => {
        this.hasBorrowed = false;
        alert('Book returned successfully!');
      })
      .catch(error => {
        console.error('Error returning book:', error);
      });
    },
    checkIfBorrowed() {
      const userId = JSON.parse(localStorage.getItem('user')).id;
      axios.get(`http://localhost:5000/borrowed-books/${userId}`)
        .then(response => {
          this.hasBorrowed = response.data.some(book => book.id === this.id);
        })
        .catch(error => {
          console.error('Error checking borrowed books:', error);
        });
    }
  }
};
</script>


<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.details-card {
  display: flex;
  align-items: center;
  max-width: 800px;
  width: 100%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  gap: 20px;
}

.book-image {
  max-width: 300px;
  max-height: 400px;
  object-fit: cover;
  border-radius: 8px;
}

.book-info {
  flex: 1;
}

.book-info h1 {
  font-size: 2em;
  margin: 0;
}

.author {
  font-size: 1.2em;
  color: #555;
  margin: 10px 0;
}

.description {
  margin: 20px 0;
}

.pdf-button, .view-pdf-button, .hide-pdf-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
}

.pdf-button:hover, .view-pdf-button:hover, .hide-pdf-button:hover {
  background-color: #0056b3;
}

.pdf-viewer {
  width: 100%;
  height: 500px;
  border: none;
  margin-top: 10px;
}

.borrow-button, .return-button {
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.borrow-button:hover, .return-button:hover {
  background-color: #218838;
}
</style>
