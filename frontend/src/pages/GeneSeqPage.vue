<template>
    <div class="seq">
        <div class="cont">
            <h1>HEHEHEHEHEHEHEHEHE TOTOTO</h1>

            <GeneSequenceDisplay/>

        </div>
      
    </div>
  </template>
  
  <script>
  import GeneSequenceDisplay from "@/components/GeneSequenceDisplay.vue";
  export default {
  name: 'gene-sequence',
  components: {
    GeneSequenceDisplay
  },
  
}
  </script>
  
  <style>
  .seq {
    position: relative; /* Needed for absolute positioning of the pseudo-element */
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100vh;
    background: none; /* No background image here */
  }
  
  .seq::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('../assets/evo5.jpg');
    background-size: cover;
    background-position: center;
    opacity: 0.3; /* Opacity only applies to the background image */
    z-index: -1; /* Ensures the background is behind the content */
  }
  
  
  </style>
  
  