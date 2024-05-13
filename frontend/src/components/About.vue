<template>
  <div class="slider-container">
    <div class="card-slider">
      <div v-for="item in items" :key="item.id" class="slider-item">
        <img :src="item.imageUrl" alt="Card image" class="card-image">
        <div class="card-content">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <a :href="item.link" class="btn">{{ item.buttonLabel }}</a>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'CardSlider',
  data() {
    return {
      items: [
        { id: 1, imageUrl: '../assets/evo1.png', title: 'Run Yass', description: 'Use the YASS algorithm to generate graphs', link: '/run-yass', buttonLabel: 'Run Now' },
        { id: 2, imageUrl: '../assets/evo1.png', title: 'Search Gene Sequence', description: 'Search gene sequences using GeneID from www.ensembl.org website', link: '/gene-sequence/:geneId', buttonLabel: 'Run Now' },
        // Add more items as needed
      ]
    };
  },
}
</script>
<style scoped>
.slider-container {
  overflow-x: auto;
  padding: 20px;
}

.card-slider {
  display: flex;
  gap: 20px;
}

.slider-item {
  flex: 0 0 auto;
  width: 300px; /* Fixed width for each card */
  background-color: white;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  border-radius: 10px;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 200px; /* Fixed height for images */
  object-fit: cover;
}

.card-content {
  padding: 15px;
}

.btn {
  background-color: #007bff;
  color: white;
  padding: 10px;
  text-decoration: none;
  border-radius: 5px;
  display: inline-block;
}
</style>
