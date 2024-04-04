<template>
  <div>
    <h1>Gene Structure</h1>
    <form @submit.prevent="fetchGeneStructure">
      <label for="geneId">Enter Gene ID:</label>
      <input type="text" id="geneId" v-model="geneId">
      <button type="submit">Get Gene Structure</button>
    </form>

    <!-- Section to display processed gene structure
    <div v-if="geneStructure">
      <h2>Processed Gene Structure</h2>
      <div v-for="gene in geneStructure" :key="gene.gene_id">
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
    </div> -->

    <!-- Section to display the raw API response in a window-like container -->
    <div v-if="rawApiResponse" class="api-response-window">
      <h2>Raw API Response</h2>
      <pre>{{ rawApiResponse }}</pre>
    </div>

    <div v-if="exonsPositions">
      <!-- Button to trigger the plot function -->
      <button @click="plotGeneImage">Plot Gene Image</button>

      <!-- Display the gene image -->
      
      <img v-if="imageSrc" :src="imageSrc" alt="Gene Image">
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
      exonsPositions: null,
      imageSrc: null,
    };
  },
  methods: {
    processExonsPositions() {
      if (this.geneStructure) {
        // Extract "start" and "end" fields from each gene and create exonsPositions array
        this.exonsPositions = this.geneStructure.map(gene => {
          return [gene.start, gene.end];
        });

        // Log the result to the console
        console.log('Exons Positions:', this.exonsPositions);
      }
    },

    plotGeneImage() {
      // Make an HTTP request to the Flask endpoint
      fetch('http://localhost:5000/generate/gene-image', {
        method: 'POST',  // You may need to adjust the method based on your Flask route
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exonsPositions: this.exonsPositions }),
        mode: 'cors',
      })
      .then(response => response.blob())
      .then(blob => {
        // Create a Blob URL and set it as the image source
        const imageUrl = URL.createObjectURL(blob);
        this.imageSrc = imageUrl;
        console.log('Image URL:', imageUrl);
      })
      .catch(error => {
        console.error('Error fetching gene image:', error);
      });
    },

    fetchGeneStructure() {
      // Log the geneId before making the request
      console.log('Gene ID:', this.geneId);

      const requestData = { gene_id: this.geneId };

      fetch('http://localhost:5000/generate/gene-structure', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData),
        // credentials: 'include',
        mode: 'cors',
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
        
        // Call the method to process exons positions
        this.processExonsPositions();
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
