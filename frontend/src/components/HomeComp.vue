<template>

    <div class="card rounded-pill text-center overflow-hidden" style="width: 18rem;">
      <img :src="imageUrl" class="card-img-top" alt="...">
      <div class="card-body bg-dark text-white">
        <h5 class="card-title">{{ title }}</h5>
        <p class="card-text">{{ description }}</p>
        <a :href="link" class="btn btn-light px-3 rounded-pill">{{ buttonLabel }}</a>
      </div>
  </div>

</template>
  

  <script>
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
  