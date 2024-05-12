<template>
  <!-- <div>
    <h1>Gene Sequence Display</h1>
    <div>
      <input v-model="geneId" placeholder="Enter Gene ID" />
      <button @click="searchGene">Search</button>
      <textarea v-model="gene_seq_content" rows="10" cols="50" readonly></textarea>
    </div>
  </div> -->

  <div class="container">
    <h1>Gene Sequence Display</h1>
    <div class="input-container">
      <input v-model="geneId" placeholder="Enter Gene ID" />
      <button @click="searchGene">Search</button>
    </div>
    <textarea v-model="gene_seq_content" rows="10" cols="50" readonly></textarea>
  </div>

</template>

<script>
export default {
  data() {
    return {
      geneId: '',
      gene_seq_content: '',
    };
  },
  methods: {
    async searchGene() {
      if (!this.geneId) {
        alert('Please enter a Gene ID');
        return;
      }

      await this.fetchGeneSequence();
    },
    async fetchGeneSequence() {
      try {
        // Make a request to fetch the gene sequence in JSON format
        const response = await fetch(`http://rest.ensembl.org/sequence/id/${this.geneId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch gene sequence: ${response.statusText}`);
        }

        const data = await response.json();
        // this.gene_seq_content = JSON.stringify(data, null, 2); // Display JSON content
        this.gene_seq_content = data.seq; // Display JSON content
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
};
</script>

<style>
/* Add your styles here */
</style>
