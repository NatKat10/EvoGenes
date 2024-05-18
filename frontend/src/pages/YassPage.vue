<template>
  <div class="container1">
    <div class="run-yass">
    <div class="yassComp">
      <div class="components-container">
        <GeneStructure />
        <RunYass />
      </div>
    </div>
  </div>

  </div>
  
</template>

<script>
import RunYass from "@/components/RunYass.vue";  
import GeneStructure from "@/components/GeneStructure.vue";

export default {
  components: {
    RunYass,
    GeneStructure  
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
  min-height: 100vh; /* Ensure the container takes at least the full viewport height */
  background: none; /* No background image here */
  overflow-y: auto; /* Allow vertical scrolling */
}

.run-yass::before {
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
  padding: 20px; /* Add padding for better spacing */
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
