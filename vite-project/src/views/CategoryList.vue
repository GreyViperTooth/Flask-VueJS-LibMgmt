<template>
  <div>
    <h1>Category List</h1>
    <ul>
      <li v-for="category in categories" :key="category.id">
        <router-link :to="{ name: 'CategoryDetails', params: { id: category.id } }">{{ category.name }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import CategoryService from '../services/CategoryService';

export default {
  name: 'CategoryList',
  data() {
    return {
      categories: []
    };
  },
  created() {
    CategoryService.getCategories()
      .then(response => {
        this.categories = response.data;
      })
      .catch(error => {
        console.error("Error fetching categories:", error);
      });
  }
};
</script>

<style scoped>
/* Add your styles here if needed */
</style>

  