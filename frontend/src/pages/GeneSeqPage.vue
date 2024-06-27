<template>
  <div class="seq">
    <div class="cont">
      
    </div>
  </div>
</template>

<script>

export default {
  name: 'gene-sequence',
  components: {
  },
}
</script>

<style>
.seq {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100vh;
  background: none;
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
  opacity: 0.3;
  z-index: -1;
}

.cont {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px; /* Add space between items */
}

.grid > * {
  flex: 0 1 calc(33.333% - 20px); /* 3 items per row, minus the gap */
  box-sizing: border-box;
  margin-bottom: 20px;
}
</style>
