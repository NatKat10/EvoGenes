<template>
  <div class="container1">
    <div class="run-yass">
      <div class="yassComp">

        <header class="header2">
            <svg class="gene-title" viewBox="0 0 1000 100">
              <text x="50%" y="50%" text-anchor="middle" dy=".35em" class="gene-text">Run Evo Genes</text>
            </svg>
          </header>

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
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 100vh;
  background: none;
  overflow-y: auto;
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
  opacity: 0.3;
  z-index: -1;
}

.yassComp {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.components-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 20px;
}

.header2 {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.gene-title {
  width: 1200px;
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
  align-items: stretch;
  width: 100%;
  gap: 20px; /* Add space between components */
}

.components-container > div {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 500px; /* Adjust as needed for a larger size */
}
  
</style>
