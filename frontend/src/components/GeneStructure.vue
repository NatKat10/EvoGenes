<template>
  <div class="container">
    <h1>Gene Structure</h1>
    <form @submit.prevent="fetchGeneStructure">
      <label for="geneId">Enter Gene ID:</label>
      <input type="text" id="geneId" v-model="geneId">
      <button type="submit">Search Gene Structure</button>
    </form>

    <!-- Display success message if the gene is found -->
    <div v-if="geneStructureFound" class="success-message">
      Gene structure found successfully!
    </div>

    <!-- Display error message if the gene is not found -->
    <div v-if="geneStructureFound === false" class="error-message">
      Gene ID not found or incorrect
    </div>

    <!-- Display the exonsPositions array -->
    <div v-if="geneStructureFound === true && exonsPositions">
      <h2>Exons Positions:</h2>
      <div> [{{ formatExonsPositions() }}] </div>
    </div>

    <div v-if="geneStructureFound === true && exonsPositions" class="button-image-container">
      <!-- Button to trigger the plot function -->
      <button @click="plotGeneImage" class="plot-button">Plot Gene Image</button>
    </div>

    <!-- Display the gene image -->
    <div v-if="geneStructureFound === true && exonsPositions && imageSrc" class="gene-image-container">
      <img :src="imageSrc" alt="Gene Image">
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
      geneStructureFound: null,
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
      // this.geneStructureFound = false;

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
        if (data) {
          this.geneStructure = data; // Assuming data contains gene structure information
          this.rawApiResponse = JSON.stringify(data, null, 2); // Format JSON for display
          this.geneStructureFound = true; // Set flag to true when gene structure is found
          // Call the method to process exons positions
          this.processExonsPositions();
        } else {
          this.geneStructureFound = false; // Set flag to false if gene structure is not found
        }
      })
      .catch(error => {
        console.error("Error fetching gene structure:", error);
        this.rawApiResponse = `Failed to fetch data: ${error.message}`;
      });
    },

    formatExonsPositions() {
      if (!this.exonsPositions) return '';

      return this.exonsPositions.map(positions => `(${positions.join(',')})`).join(', ');
    }

  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

/* Style for the API response window */
/* .api-response-window {
  margin-top: 20px;
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  padding: 10px;
  overflow: auto;
  max-height: 400px; /* Adjust based on your needs 
} */

.error-message {
  margin-top: 20px;
  color: red;
}

.success-message {
  margin-top: 20px;
  color: green;
}

.success-message::before {
  content: '✓ ';
}

.button-image-container {
  margin-top: 20px;
  display: flex;
  align-items: center;
}

.plot-button {
  margin-bottom: 10px; /* Add margin to the button */
}

.gene-image-container img {
  width: 100%; /* Ensure image fills its container */
}

</style>
