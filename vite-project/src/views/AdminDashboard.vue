<template>
  <div class="container mt-5">
    <h1 class="mb-4">Admin Dashboard</h1>


    <!-- Users and Borrowed Books (Collapsible) -->
    <div class="card mb-4">
      <div class="card-header" @click="toggleCollapse('usersWithBooksForm')">
        <h2 class="card-title">Users and Borrowed Books</h2>
      </div>
      <div v-show="visibleForms.usersWithBooksForm">
        <div class="card-body">
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>User Name</th>
                <th>Email</th>
                <th>Borrowed Book</th>
                <th>Borrowed Date</th>
                <th>Revoke Access</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user, index) in usersWithBooks" :key="index">
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.borrowed_book.title }}</td>
                <td>{{ new Date(user.borrowed_date).toLocaleDateString() }}</td>
                <td>
                  <button class="btn btn-danger" @click="revokeAccess(user.id, user.borrowed_book.id)">Revoke</button>
                </td>
              </tr>
            </tbody>
          </table>
                <!-- New table for books stats -->
      <h4>Books Borrowing Stats</h4>
      <table class="books-stats-table">
        <thead>
          <tr>
            <th>Book Title</th>
            <th>Number Borrowed</th>
            <th>Number of Users</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in booksStats" :key="book.title">
            <td>{{ book.title }}</td>
            <td>{{ book.num_borrowed }}</td>
            <td>{{ book.num_users }}</td>
          </tr>
        </tbody>
      </table>
        </div>
      </div>
    </div>
    <!-- Add Category Form (Collapsible) -->
    <div class="card mb-4">
      <div class="card-header" @click="toggleCollapse('addCategoryForm')">
        <h2 class="card-title">Add Category</h2>
      </div>
      <div v-show="visibleForms.addCategoryForm">
        <div class="card-body">
          <form @submit.prevent="addCategory">
            <div class="form-group">
              <label for="categoryName">Category Name:</label>
              <input type="text" id="categoryName" v-model="categoryName" class="form-control" required />
            </div><br>
            <button type="submit" class="btn btn-primary">Add Category</button>
          </form>
        </div>
      </div>
    </div>

        <!-- Categories (Collapsible) -->
        <div class="card mb-4">
      <div class="card-header" @click="toggleCollapse('categoriesForm')">
        <h2 class="card-title">Manage Categories</h2>
      </div>
      <div v-show="visibleForms.categoriesForm">
        <div class="card-body">
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>Category Name</th>
                <th>Edit</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(category, index) in categories" :key="index">
                <td>{{ category.name }}</td>
                <td><button class="btn btn-warning" @click="editCategory(category.id)">Edit</button></td>
                <td><button class="btn btn-danger" @click="deleteCategory(category.id)">Delete</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Books (Collapsible) -->
    <div class="card mb-4">
      <div class="card-header" @click="toggleCollapse('booksForm')">
        <h2 class="card-title">Manage Books</h2>
      </div>
      <div v-show="visibleForms.booksForm">
        <div class="card-body">
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>Book Title</th>
                <th>Author</th>
                <th>Edit</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(book, index) in books" :key="index">
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td><button class="btn btn-warning" @click="editBook(book.id)">Edit</button></td>
                <td><button class="btn btn-danger" @click="deleteBook(book.id)">Delete</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Add Book Form (Collapsible) -->
    <div class="card mb-4">
      <div class="card-header" @click="toggleCollapse('addBookForm')">
        <h2 class="card-title">Add Book</h2>
      </div>
      <div v-show="visibleForms.addBookForm">
        <div class="card-body">
          <form @submit.prevent="addBook">
            <div class="form-group">
              <label for="bookTitle">Book Title:</label>
              <input type="text" id="bookTitle" v-model="book.title" class="form-control" required />
            </div>
            <div class="form-group">
              <label for="bookAuthor">Book Author:</label>
              <input type="text" id="bookAuthor" v-model="book.author" class="form-control" required />
            </div>
            <div class="form-group">
              <label for="bookDescription">Book Description:</label>
              <textarea id="bookDescription" v-model="book.description" class="form-control"></textarea>
            </div>
            <div class="form-group">
              <label for="bookCategory">Book Category:</label>
              <select id="bookCategory" v-model="book.category_id" class="form-control" required>
                <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="bookCover">Book Cover Image:</label>
              <input type="file" id="bookCover" @change="onFileChange('coverImage', $event)" class="form-control" />
            </div>
            <div class="form-group">
              <label for="bookPDF">Book PDF:</label>
              <input type="file" id="bookPDF" @change="onFileChange('pdfFile', $event)" class="form-control" />
            </div><br>
            <button type="submit" class="btn btn-primary">Add Book</button>
          </form>
        </div>
      </div>
    </div>

    <!-- Book List (Collapsible) -->
    <div class="card mb-4">
      <div class="card-header" @click="toggleCollapse('bookListForm')">
        <h2 class="card-title">Store Snapshot:</h2>
      </div>
      <div v-show="visibleForms.bookListForm">
        <div class="card-body">
          <!-- Including the BookList component -->
          <BookList />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import BookList from './BookList.vue';  // Import the BookList component

export default {
  data() {
    return {
      categoryName: '',
      book: {
        title: '',
        author: '',
        description: '',
        booksStats: [],
        category_id: ''
      },
      categories: [],
      coverImage: null, // Store the file object
      pdfFile: null,    // Store the PDF file object
      visibleForms: {
        addCategoryForm: false,
        addBookForm: false,
        bookListForm: false,
        usersWithBooksForm: false // Add entry for users with books
      },
      usersWithBooks: []  // Define usersWithBooks in data
    };
  },
  created() {
    this.fetchCategories();
    this.fetchUsersWithBooks();  // Fetch users with borrowed books when the component is created
    this.fetchBooksStats();  // Fetch book stats when the component is created
  },
  components: {
    BookList  // Register the BookList component
  },
  methods: {
    fetchCategories() {
      axios.get('http://localhost:5000/categories')
        .then(response => {
          this.categories = response.data;
        })
        .catch(error => {
          console.error("Error fetching categories:", error);
        });
    },
    addCategory() {
      axios.post('http://localhost:5000/categories', { name: this.categoryName })
        .then(response => {
          alert(response.data.message);
          this.categoryName = '';
          this.fetchCategories(); // Refresh the categories list
        })
        .catch(error => {
          console.error("Error adding category:", error);
        });
    },
    onFileChange(type, event) {
      const file = event.target.files[0];
      if (type === 'coverImage') {
        this.coverImage = file;
      } else if (type === 'pdfFile') {
        this.pdfFile = file;
      }
    },
    addBook() {
      const formData = new FormData();
      formData.append('title', this.book.title);
      formData.append('author', this.book.author);
      formData.append('description', this.book.description);
      formData.append('category_id', this.book.category_id);
      
      // Append cover image and PDF file if they exist
      if (this.coverImage) {
        formData.append('cover_image', this.coverImage);
      }
      if (this.pdfFile) {
        formData.append('pdf_file', this.pdfFile);
      }

      axios.post('http://localhost:5000/books', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        alert(response.data.message);
        this.book.title = '';
        this.book.author = '';
        this.book.description = '';
        this.book.category_id = '';
        this.coverImage = null;
        this.pdfFile = null;
      })
      .catch(error => {
        console.error("Error adding book:", error);
      });
    },
    toggleCollapse(formId) {
      // Toggle visibility while ensuring that only the card header is clickable
      this.visibleForms[formId] = !this.visibleForms[formId];
    },
    fetchUsersWithBooks() {
      axios.get('http://localhost:5000/users-with-books')
        .then(response => {
          console.log(response.data);  // Debug log
          this.usersWithBooks = response.data;
        })
        .catch(error => {
          console.error("Error fetching users with books:", error);
        });
    },
    revokeAccess(userId, bookId) {
      axios.post('http://localhost:5000/revoke-access', {
        user_id: userId,
        book_id: bookId
      })
      .then(response => {
        alert(response.data.message);
        console.log(response.data);  // Debug log
        this.fetchUsersWithBooks(); // Refresh the list after revoking
      })
      .catch(error => {
        console.error("Error revoking access:", error);
      });
    },
    async fetchBooksStats() {
      try {
        const response = await axios.get('http://localhost:5000/books_stats');
        this.booksStats = response.data;
      } catch (error) {
        console.error('Error fetching books stats:', error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
}
.card {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.card-header {
  cursor: pointer;
  background-color: #f8f9fa;
}
.card-title {
  font-size: 1.25rem;
}
.card {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
  background-color: #f9f9f9;
}

h4 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 1.25rem;
  color: #333;
}

.books-stats-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.books-stats-table th,
.books-stats-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.books-stats-table th {
  background-color: #f4f4f4;
  color: #333;
  font-weight: bold;
}

.books-stats-table tr:hover {
  background-color: #f1f1f1;
}

.books-stats-table td {
  color: #555;
}
</style>
