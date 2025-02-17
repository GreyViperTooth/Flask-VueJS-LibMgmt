import { createRouter, createWebHistory } from 'vue-router';
import BookList from './views/BookList.vue';
import BookDetails from './views/BookDetails.vue';
import AdminDashboard from './views/AdminDashboard.vue';
import UserSignup from './views/UserSignup.vue';
import AdminSignup from './views/AdminSignup.vue';
import AllLogin from './views/AllLogin.vue';
import UserProfile from './views/UserProfile.vue';
import Home from './views/HomePage.vue';

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/books', component: BookList },
  { path: '/books/:id', component: BookDetails, name: 'BookDetails', props: true },
  { path: '/admin-dashboard', component: AdminDashboard, meta: { requiresAuth: true, isAdmin: true } },
  { path: '/signup', component: UserSignup },
  { path: '/admin-signup', component: AdminSignup },
  { path: '/login', component: AllLogin },
  { path: '/profile', component: UserProfile, meta: { requiresAuth: true } },
  { path: '/profile/:id', component: UserProfile, meta: { requiresAuth: true }, props: true },
  { path: '/home', component: Home }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user'));
  const isAuthenticated = !!user;

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ path: '/login' });
    } else {
      // If the route is the admin dashboard, ensure the user is an admin
      if (to.matched.some(record => record.meta.isAdmin) && !user.is_admin) {
        next({ path: '/books' }); // Non-admin users should not access admin routes
      } else {
        next(); // Let the user go to the route
      }
    }
  } else {
    next();
  }
});

export default router;
