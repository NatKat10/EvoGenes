<template>
  <div class="home-page">
    <header class="header">
      <svg class="gene-title" viewBox="0 0 1000 100">
        <text x="31%" y="50%" text-anchor="middle" dy=".35em" class="gene-text">EVO</text>
        <image x="45%" y="30%" width="54" height="54" xlink:href="../assets/circle_logo.png" alt="Logo" />
        <text x="70%" y="50%" text-anchor="middle" dy=".35em" class="gene-text">GENES</text>
      </svg>
    </header>

    <div class="content-overlay">
      <!-- HomeComp components -->
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
  </div>
</template>

<script>
import HomeComp from "@/components/HomeComp.vue";
export default {
  name: 'HomePage',
  components: {
    HomeComp
  }
}
</script>

<style>
.home-page {
  display: flex;
  flex-direction: column; /* Ensure components are arranged vertically */
  align-items: center;
  height: 100vh;
  overflow: hidden;
}

/* Header styles */
.header {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1; /* Lower z-index to ensure it is behind the menu */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 0;
}

/* Menu styles (assuming you have a menu class) */
.menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 200px; /* Adjust based on your menu width */
  height: 100%;
  background: #333; /* Sample background color */
  z-index: 10; /* Higher z-index to ensure it is above the header */
}

/* SVG Gene Title */
.gene-title {
  width: 1000px;
  height: 100px;
}

.gene-text {
  font-size: 80px;
  fill: #4caf50; /* Adjust color as needed */
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700; /* Increased font weight for thicker text */
  stroke: #000;
  stroke-width: 4px;
  animation: geneMove 7s infinite alternate;
}

/* Animation */
@keyframes geneMove {
  0% { letter-spacing: 5px; }
  50% { letter-spacing: 20px; }
  100% { letter-spacing: 5px; }
}

.gene-text {
  animation: geneMove 5s infinite alternate;
}

/* Content overlay for the rest of the page */
.content-overlay {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-top: 100px; /* Space for the header */
}

/* Add margin between HomeComp components */
.content-overlay > * + * {
  margin-left: 50px; /* Adjust this value as needed */
}

/* Background settings */
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
  opacity: 0.4;
  z-index: -1;
}
</style>
