<template>
  <div class="container">
    <h1>"Evo-Genes" help</h1>
    <div class="instruction-list">
      <div class="instruction-item" v-for="(item, index) in instructions" :key="index">
        <div class="icon" v-if="item.image">
          <img :src="item.image" :alt="item.title" class="button-image">
        </div>
        <div class="icon" v-else>
          <i :class="item.icon"></i>
        </div>
        <div class="description">
          <h2>{{ item.title }}</h2>
          <p>{{ item.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GeneVisualization',
  data() {
    return {
      instructions: [
        {
          image: require('../assets/camera.png'), // Update the path as needed
          title: 'Camera',
          description: 'Allows you to capture a screenshot of the visualization and save it as an image file.'
        },
        {
          icon: 'fa fa-info-circle',
          title: 'Help',
          description: 'Offers additional help and support resources for using the "Evo-Genes" web application.'
        },
        {
          icon: 'fa fa-question-circle',
          title: 'Question Mark',
          description: 'Opens a text file with additional information about the YASS alignment summary.'
        }
      ]
    };
  }
};
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
  box-shadow: 0.5vw 0.5vw 1vw rgba(144, 143, 143, 0.5); /* Corrected CSS syntax */
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

.instruction-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.instruction-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.icon {
  margin-right: 20px;
  font-size: 24px; /* Adjust the size as needed for icons */
}

.button-image {
  width: 50px; /* Adjust the size as needed */
  height: auto;
}

.description {
  flex: 1;
}

.description h2 {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
}

.description p {
  margin: 5px 0 0 0;
  font-size: 18px; /* Sets the font size for the paragraphs */
  line-height: 1.6; /* Adjusts line spacing for better readability */
}
</style>
