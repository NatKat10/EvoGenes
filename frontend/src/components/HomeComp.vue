<template>
 
  <div class="home-comp px-4">
    <h1> HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII</h1>
      <b-carousel-slide v-for="item in items" :key="item.id">
        <template #default>
          <div class="card mx-auto" style="width: 18rem;">
            <img :src="item.image" class="card-img-top" alt="Profile of {{ item.name }}">
            <div class="card-body">
              <h5 class="card-title">{{ item.name }}</h5>
              <p class="card-text">{{ item.description }}</p>
              <a href="#" class="btn btn-primary">View More</a>
            </div>
          </div>
        </template>
      </b-carousel-slide>
  </div>
    
  </template>
  

  <!-- image: require('@/assets/profile1.jpg') -->
  <script>
    export default {
    name: 'HomeComp',
    mounted() {
        console.log('HomeComp mounted');
    }
    }
  
  </script>
  
  <style scoped>
  
  
  
  </style>
  