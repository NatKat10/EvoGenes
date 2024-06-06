<template>
  <div class="container1">
    <div class="run-yass">
      <div class="yassComp">
        <div class="components-container">
          <RunYass />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RunYass from "@/components/RunYass.vue";  

export default {
  components: {
    RunYass
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

h1 {
  text-align: center;
  margin-bottom: 20px;
}
</style>
