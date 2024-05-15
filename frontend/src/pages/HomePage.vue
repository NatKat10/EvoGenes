<template>
    <div class="home-page">
        <!-- <HomeComp /> Make sure this matches the registered component name -->
        <!-- <HomeComp /> -->



        <HomeComp
          :imageUrl="require('../assets/evo1.png')"
          :title="'Run Yass'"
          :description="'Use the YASS algorithm to generate graphs'"
          :link="'/run-yass'" 
          :buttonLabel="'Run Now'"
        />

      

        <HomeComp
          :imageUrl="require('../assets/evo1.png')"
          :title="'Search Gene Sequence'"
          :description="'Seach gene sequences using GeneID from www.ensembl.org website'"
          :link="'/gene-sequence/:geneId'" 
          :buttonLabel="'Search'"
        />
    </div>
  </template>
  
  <script>
  import HomeComp from "@/components/HomeComp.vue";
  export default {
  name: 'HomePage',
  components: {
    HomeComp
  },
  
}
  </script>
  
  <style>
  /* .home-page {
    position: relative; Needed for absolute positioning of the pseudo-element
    width: 100%;
    height: 100vh;
    overflow: hidden; Prevents content from spilling out
  } */
  
  .home-page {
    display: flex; /* Change display to flex */
    flex-direction: row; /* Ensure components are arranged horizontally */
    justify-content: center; /* Center components horizontally */
    align-items: center; /* Center components vertically */
    height: 100vh;
    overflow: hidden;
  }

  /* Add margin between HomeComp components */
  .home-page > * + * {
    margin-left: 50px; /* Adjust this value as needed */
  }


  .home-page::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('../assets/evo2.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.4; /* Opacity applied only to the background */
    z-index: -1; /* Ensures the background is behind the content */
  }
  
  .content-overlay {
    position: relative; /* Ensure this is positioned above the pseudo-element */
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1; /* Higher index to keep content above the background */
  }
  </style>
  
  