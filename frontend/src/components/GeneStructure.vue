<template>
  <div>
    <h1>Gene Structure</h1>
    <form @submit.prevent="fetchGeneStructure">
      <label for="geneId">Enter Gene ID:</label>
      <input type="text" id="geneId" v-model="geneId">
      <button type="submit">Get Gene Structure</button>
    </form>

    <!-- Section to display processed gene structure -->
    <div v-if="geneStructure">
      <h2>Processed Gene Structure</h2>
      <div v-for="(gene, index) in geneStructure" :key="index">
        <h3>Gene ID: {{ gene.gene_id }}</h3>
        <div v-for="(exon, exonIndex) in gene.exons" :key="exonIndex">
          <div>Exon ID: {{ exon.id }}</div>
          <div>Start: {{ exon.start }}</div>
          <div>End: {{ exon.end }}</div>
        </div>
        <div v-if="gene.introns && gene.introns.length > 0">
          <h4>Introns:</h4>
          <div v-for="(intron, intronIndex) in gene.introns" :key="intronIndex">
            <div>Intron ID: {{ intron.id }}</div>
            <div>Start: {{ intron.start }}</div>
            <div>End: {{ intron.end }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section to display the raw API response in a window-like container -->
    <div v-if="rawApiResponse" class="api-response-window">
      <h2>Raw API Response</h2>
      <pre>{{ rawApiResponse }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      geneId: '',
      geneStructure: null, // This will hold the processed gene structure data
      rawApiResponse: '', // This will hold the raw API response as a string
    };
  },
  methods: {
    fetchGeneStructure() {
  // Log the geneId before making the request
  console.log('Gene ID:', this.geneId);

  const requestData = { gene_id: this.geneId };

  fetch('http://localhost:5000/generate/gene-structure', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(requestData),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok: ' + response.statusText);
    }
    return response.json();
  })
  .then(data => {
    this.geneStructure = data; // Assuming data contains gene structure information
    this.rawApiResponse = JSON.stringify(data, null, 2); // Format JSON for display
  })
  .catch(error => {
    console.error("Error fetching gene structure:", error);
    this.rawApiResponse = `Failed to fetch data: ${error.message}`;
  });
},

  },
};
</script>

<style>
/* Style for the API response window */
.api-response-window {
  margin-top: 20px;
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  padding: 10px;
  overflow: auto;
  max-height: 400px; /* Adjust based on your needs */
}
</style>
