<template>
    <div class="container1">
      <div class="run-yass">
        <div class="yassComp">

          <header class="header1">
            <svg class="gene-title" viewBox="0 0 1000 100">
              <text x="50%" y="50%" text-anchor="middle" dy=".35em" class="gene-text">HELP</text>
            </svg>
          </header>
          
          <div class="components-container">
            <AboutComp />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import AboutComp from "@/components/AboutComp.vue";
  
  export default {
    components: {
      AboutComp
    }
  };
  </script>
  
  <style scoped>
  .run-yass {
    position: relative; /* Needed for absolute positioning of the pseudo-element */
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 100vh; /* Ensure the container takes at least the full viewport height */
    background: none; /* No background image here */
    overflow-y: auto; /* Allow vertical scrolling */
    padding: 1vw;
  }
  
  .run-yass::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('../assets/evo4.jpg');
    background-size: cover;
    background-position: center;
    opacity: 0.3; /* Opacity only applies to the background image */
    z-index: -1; /* Ensures the background is behind the content */
  }
  
  /* hi */
  .yassComp {
    position: relative; /* Ensure this content is on top of the background */
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 1200px; /* Ensure the container does not exceed this width */
    margin: 0 auto; /* Center the container horizontally */
    padding: 10px; /* Add padding for better spacing */
  }
  
  .header1 {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .gene-title {
    width: 1000px;
    height: 100px;
  }
  
  .gene-text {
    font-size: 80px;
    fill: #ffffff; /* Adjust color as needed */
    font-family: 'Courier New', Courier, monospace;
    font-weight: 700; /* Increased font weight for thicker text */
    animation: geneMove 7s infinite alternate;
    stroke: #000;
    stroke-width: 4px;
  }
  
  @keyframes geneMove {
    0% { letter-spacing: 5px; }
    50% { letter-spacing: 20px; }
    100% { letter-spacing: 5px; }
  }
  
  .components-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    gap: 20px; /* Add space between components */
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px; /* Add some space below the heading */
  }
  </style>
  