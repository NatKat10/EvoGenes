<template>
  <div class="seq">
    <div class="cont">
      <div class="grid">
        <PopularGenesComp
          :imageUrl="require('../assets/logoo.jpg')"
          :title="'Popular Human Genes 1'"
          :description="'See the most popular genes for human use'"
          :buttonLabel="'HUMAN'"
          :modalTitle="'Details for Popular Human Genes 1'"
          :tableData="[
            { id: 1, col1: 'Gene A1', col2: 'Sequence A1' },
            { id: 2, col1: 'Gene A2', col2: 'Sequence A2' }
          ]"
        />
        <PopularGenesComp
          :imageUrl="require('../assets/logoo.jpg')"
          :title="'Popular Human Genes 2'"
          :description="'See the most popular genes for human use'"
          :buttonLabel="'HUMAN'"
          :modalTitle="'Details for Popular Human Genes 2'"
          :tableData="[
            { id: 1, col1: 'Gene B1', col2: 'Sequence B1' },
            { id: 2, col1: 'Gene B2', col2: 'Sequence B2' }
          ]"
        />
        <PopularGenesComp
          :imageUrl="require('../assets/logoo.jpg')"
          :title="'Popular Human Genes 3'"
          :description="'See the most popular genes for human use'"
          :buttonLabel="'HUMAN'"
          :modalTitle="'Details for Popular Human Genes 3'"
          :tableData="[
            { id: 1, col1: 'Gene C1', col2: 'Sequence C1' },
            { id: 2, col1: 'Gene C2', col2: 'Sequence C2' }
          ]"
        />
        <PopularGenesComp
          :imageUrl="require('../assets/logoo.jpg')"
          :title="'Popular Human Genes 4'"
          :description="'See the most popular genes for human use'"
          :buttonLabel="'HUMAN'"
          :modalTitle="'Details for Popular Human Genes 4'"
          :tableData="[
            { id: 1, col1: 'Gene D1', col2: 'Sequence D1' },
            { id: 2, col1: 'Gene D2', col2: 'Sequence D2' }
          ]"
        />
        <PopularGenesComp
          :imageUrl="require('../assets/logoo.jpg')"
          :title="'Popular Human Genes 5'"
          :description="'See the most popular genes for human use'"
          :buttonLabel="'HUMAN'"
          :modalTitle="'Details for Popular Human Genes 5'"
          :tableData="[
            { id: 1, col1: 'Gene E1', col2: 'Sequence E1' },
            { id: 2, col1: 'Gene E2', col2: 'Sequence E2' }
          ]"
        />
        <PopularGenesComp
          :imageUrl="require('../assets/logoo.jpg')"
          :title="'Popular Human Genes 6'"
          :description="'See the most popular genes for human use'"
          :buttonLabel="'HUMAN'"
          :modalTitle="'Details for Popular Human Genes 6'"
          :tableData="[
            { id: 1, col1: 'Gene F1', col2: 'Sequence F1' },
            { id: 2, col1: 'Gene F2', col2: 'Sequence F2' }
          ]"
        />
      </div>
    </div>
  </div>
</template>

<script>
import PopularGenesComp from "@/components/PopularGenesComp.vue";

export default {
  name: 'gene-sequence',
  components: {
    PopularGenesComp
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
