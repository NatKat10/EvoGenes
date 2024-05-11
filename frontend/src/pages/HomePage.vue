<template>
    <div class="home-page">
        <HomeComp /> <!-- Make sure this matches the registered component name -->
    </div>
  </template>
  
  <script>
  import HomeComp from "@/components/HomeComp.vue";
  export default {
  name: 'HomePage',
  components: {
    HomeComp
  },
  mounted() {
    console.log('HomePage mounted');
  }
}
  </script>
  
  <style>
  .home-page {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100vh;
    background-image: url('../assets/Evo_genes_backg.jpg'); 
    background-size: cover;  
    background-position: center;
  }
  </style>
  