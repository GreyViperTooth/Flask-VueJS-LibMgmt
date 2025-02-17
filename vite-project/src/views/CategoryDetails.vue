<template>
  <div>
    <h1>Category Details</h1>
    <div v-if="category">
      <h2>{{ category.name }}</h2>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import CategoryService from '../services/CategoryService';

export default {
  name: 'CategoryDetails',
  data() {
    return {
      category: null
    };
  },
  created() {
    const categoryId = this.$route.params.id;
    CategoryService.getCategory(categoryId)
      .then(response => {
        this.category = response.data;
      })
      .catch(error => {
        console.error("Error fetching category details:", error);
      });
  }
};
</script>

<style scoped>
/* Add your styles here if needed */
</style>

  