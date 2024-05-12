<template>
    <div class="run-yass">
      <div class="yassComp">
        <h1>Run YASS</h1>
        <RunYass />
      </div>
    </div>
  </template>
  
  <script>
  import RunYass from "@/components/RunYass.vue";  // Ensure this path is correct
  
  export default {
    components: {
      RunYass  // Register the component
    }
  };
  </script>
  
  <style>
  .run-yass {
    position: relative; /* Needed for absolute positioning of the pseudo-element */
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100vh;
    background: none; /* No background image here */
  }
  
  .run-yass::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('../assets/runyass.jpg');
    background-size: cover;
    background-position: center;
    opacity: 0.3; /* Opacity only applies to the background image */
    z-index: -1; /* Ensures the background is behind the content */
  }
  
  .yassComp {
    position: relative; /* Ensure this content is on top of the background */
    z-index: 1;
  }
  </style>
  