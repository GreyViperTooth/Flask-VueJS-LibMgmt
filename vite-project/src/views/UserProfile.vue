<template>
  <div class="profile-container">
    <h1>User Profile</h1>
    <div class="profile-info">
      <img :src="profile.photo" alt="Profile Photo" class="profile-photo" v-if="profile.photo" />
      <div class="profile-details">
        <div class="detail-item">
          <strong>Name:</strong> <span>{{ profile.name }}</span>
        </div>
        <div class="detail-item">
          <strong>Email:</strong> <span>{{ profile.email }}</span>
        </div>
        <div class="detail-item">
          <strong>Mobile:</strong> <span>{{ profile.mobile }}</span>
        </div>
      </div>
    </div>

    <!-- Error/Success Message Display -->
    <div v-if="message" class="message-box" :class="{'error-message': isError, 'success-message': !isError}">
      {{ message }}
    </div>

    <!-- Borrowed Books Section -->
    <div class="card mb-4">
      <div class="card-header" @click="toggleCollapse('borrowedBooks')">
        <h2 class="card-title">Borrowed Books</h2>
      </div>
      <div v-show="visibleSections.borrowedBooks" class="card-body">
        <template v-if="borrowedBooks.length === 0">
          <p class="empty-message">Oh so empty :)</p>
        </template>
        <template v-else>
          <ul>
            <li v-for="book in borrowedBooks" :key="book.id" class="book-item">
              <img :src="book.cover_image" alt="Book Cover" class="book-cover" />
              <div class="book-details">
                <strong>{{ book.title }}</strong> by {{ book.author }}
                <div class="book-info">
                  <p>Borrowed Date: {{ book.borrowed_date }}</p>
                  <p>Due Date: {{ book.due_date }}</p>
                  <button @click="returnBook(book.id)" class="return-button">Return Book</button>
                </div>
              </div>
            </li>
          </ul>
        </template>
      </div>
    </div>

    <!-- Returned Books Section -->
    <div class="card mb-4">
      <div class="card-header" @click="toggleCollapse('returnedBooks')">
        <h2 class="card-title">Returned Books</h2>
      </div>
      <div v-show="visibleSections.returnedBooks" class="card-body">
        <template v-if="returnedBooks.length === 0">
          <p class="empty-message">Oh so empty :)</p>
        </template>
        <template v-else>
          <ul>
            <li v-for="book in returnedBooks" :key="book.id" class="book-item">
              <img :src="book.cover_image" alt="Book Cover" class="book-cover" />
              <div class="book-details">
                <strong>{{ book.title }}</strong> by {{ book.author }}
                <div class="book-info">
                  <p>Borrowed Date: {{ book.borrowed_date }}</p>
                  <p>Returned Date: {{ book.returned_date }}</p>
                </div>
              </div>
            </li>
          </ul>
        </template>
      </div>
    </div>

    <!-- Notifications Section -->
    <div class="card mb-4">
      <div class="card-header" @click="toggleCollapse('notifications')">
        <h2 class="card-title">Notifications</h2>
      </div>
      <div v-show="visibleSections.notifications" class="card-body">
        <template v-if="notifications.length === 0">
          <p class="empty-message">No notifications at the moment.</p>
        </template>
        <template v-else>
          <ul>
            <li v-for="notification in notifications" :key="notification.id" class="notification-item">
              <strong>{{ notification.message }}</strong>
              <p>{{ notification.timestamp }}</p>
            </li>
          </ul>
        </template>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      profile: {
        photo: '',
        name: '',
        email: '',
        mobile: '',
        bio: ''
      },
      borrowedBooks: [],
      returnedBooks: [],
      notifications: [],
      visibleSections: {
        borrowedBooks: false,
        returnedBooks: false,
        notifications: false
      },
      message: '',        // For displaying success or error messages
      isError: false      // For differentiating error messages from success
    };
  },
  created() {
    this.loadProfile();
    this.loadBorrowedBooks();
    this.loadReturnedBooks();
    this.loadNotifications();
  },
  methods: {
    loadProfile() {
      const user = JSON.parse(localStorage.getItem('user'));
      if (user) {
        axios.get(`/api/profile/${user.id}`)
          .then(response => {
            this.profile = response.data;
          })
          .catch(error => {
            console.error('Error loading profile:', error);
          });
      }
    },
    loadBorrowedBooks() {
      const user = JSON.parse(localStorage.getItem('user'));
      if (user) {
        axios.get(`/api/borrowed-books/${user.id}`)
          .then(response => {
            this.borrowedBooks = response.data;
          })
          .catch(error => {
            console.error('Error loading borrowed books:', error);
          });
      }
    },
    loadReturnedBooks() {
      const user = JSON.parse(localStorage.getItem('user'));
      if (user) {
        axios.get(`/api/returned-books/${user.id}`)
          .then(response => {
            this.returnedBooks = response.data;
          })
          .catch(error => {
            console.error('Error loading returned books:', error);
          });
      }
    },
    loadNotifications() {
      const user = JSON.parse(localStorage.getItem('user'));
      if (user) {
        axios.get(`/api/notifications/${user.id}`)
          .then(response => {
            this.notifications = response.data;
          })
          .catch(error => {
            console.error('Error loading notifications:', error);
          });
      }
    },
    returnBook(bookId) {
      const userId = JSON.parse(localStorage.getItem('user')).id;
      axios.post('http://localhost:5000/return', {
        user_id: userId,
        book_id: bookId,
        return_date: new Date().toISOString()
      })
      .then(response => {
        this.borrowedBooks = this.borrowedBooks.filter(book => book.id !== bookId);
        this.message = 'Book returned successfully!';
        this.isError = false;
      })
      .catch(error => {
        console.error('Error returning book:', error);
        this.message = 'Error returning the book.';
        this.isError = true;
      });
    },
    toggleCollapse(section) {
      this.visibleSections[section] = !this.visibleSections[section];
    }
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-info {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-photo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-right: 20px;
}

.profile-details {
  flex: 1;
}

.detail-item {
  margin-bottom: 10px;
}

.card {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.card-header {
  cursor: pointer;
  background-color: #f7f7f7;
  padding: 10px;
}

.card-body {
  padding: 20px;
}

.book-item, .notification-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.book-cover {
  width: 50px;
  height: 75px;
  margin-right: 20px;
}

.book-details, .notification-details {
  flex: 1;
}

.book-info, .notification-info {
  margin-top: 10px;
}

.return-button {
  padding: 5px 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.return-button:hover {
  background-color: #c82333;
}

.empty-message {
  text-align: center;
  color: #888;
  font-style: italic;
}

.message-box {
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 5px;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
}
</style>
