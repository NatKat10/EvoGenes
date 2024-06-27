<template>
  <div class="container">
    <h1>"Evo-Genes" Web Instructions</h1>
    <p>
      LOLOLO
    </p>
    
  </div>
</template>

<script>
export default {
  name: 'GeneVisualization'
}
</script>

<style scoped>
.container {
  width: 90%;
  max-width: 900px;
  margin: 5vh auto;
  padding: 3vw;
  border: 0.3vw solid #ebebeb;
  background-color: rgba(244, 244, 244, 0.6);
  border-radius: 2vw;
  box-shadow: 0.5vw 0.5vw 1vw rgba(144, 143, 143, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box; /* Ensures padding and border are included in the element's total width and height */
}

h1 {
  margin-bottom: 40px; /* Increase space below the title */
  text-align: center; /* Center-align the title */
  font-size: 23px;
}

p {
  margin-bottom: 20px; /* Adds space between paragraphs */
  text-align: justify; /* Justifies text for a cleaner look */
  font-size: 18px; /* Sets the font size for the paragraphs */
  line-height: 1.6; /* Adjusts line spacing for better readability */
}
</style>
