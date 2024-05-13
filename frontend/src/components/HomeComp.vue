<template>
  <!-- <div class="container"> 
    <div class="card rounded-pill text-center overflow-hidden" style="width: 18rem;">
      <img src="../assets/evo1.png" class="card-img-top" alt="...">
      <div class="card-body bg-dark text-white">
        <h5 class="card-title">Run Yass</h5>
        <p class="card-text">Something about the yass.</p>
        <p class="mt-3">$129.00</p>
        <a href="#" class="btn btn-light px-3 rounded-pill">Run Now</a>
      </div>
    </div>
  </div> -->

  <div class="container"> 
    <div class="card rounded-pill text-center overflow-hidden" style="width: 18rem;">
      <img :src="imageUrl" class="card-img-top" alt="...">
      <div class="card-body bg-dark text-white">
        <h5 class="card-title">{{ title }}</h5>
        <p class="card-text">{{ description }}</p>
        <a :href="link" class="btn btn-light px-3 rounded-pill">{{ buttonLabel }}</a>
      </div>
    </div>
  </div>

</template>
  

  <!-- image: require('@/assets/profile1.jpg') -->
  <script>
    // export default {
    // name: 'HomeComp',
    export default {
      name: 'HomeComp',
      props: {
        imageUrl: {
          type: String,
          required: true
        },
        title: {
          type: String,
          required: true
        },
        description: {
          type: String,
          required: true
        },
        link: {
          type: String,
          required: true
        },
        buttonLabel: {
          type: String,
          required: true
        }
      },

      mounted() {
          // console.log('HomeComp mounted');
      }
    }
  
  </script>
  
  <style scoped>
 
  </style>
  