<template>
  <div class="container">
    <h1>Find Gene Structure</h1>
    <form @submit.prevent="fetchGeneStructure" class="input-container">
      <div class="input-button-wrapper">
        <input class="textarea" type="text" v-model="geneId" placeholder="Enter Gene ID Here...">
        <button type="submit" class="search-button">➔</button>
      </div>
    </form>

    <!-- Display success message if the gene is found -->
    <div v-if="geneStructureFound" class="success-message">
      Gene structure found successfully!
    </div>

    <!-- Display error message if the gene is not found -->
    <div v-if="geneStructureFound === false" class="error-message">
      Gene ID not found or incorrect
    </div>

    <!-- Display the exonsPositions array in a resizable, scrollable text box -->
    <div v-if="geneStructureFound === true && exonsPositions" class="scrollable-textbox">
      <h2>Exons Positions:</h2>
      <div> [{{ formatExonsPositions() }}] </div>
    </div>

    <div v-if="geneStructureFound === true && exonsPositions" class="button-image-container">
      <!-- Button to trigger the plot function -->
      <button @click="plotGeneImage" class="plot-button">Plot Gene Image</button>

    </div>


    <div v-if="geneStructureFound === true && exonsPositions && dashAppUrl" class="gene-image-container">
      <iframe :src="dashAppUrl" class="figure-iframe" width="800" height="400"></iframe>
    </div>

    <!-- Dropdown to select Parent -->
    <div v-if="geneStructureFound === true && exonsPositions" class="dropdown-container">
      <label for="parent-select">Select Parent:</label>
      <select id="parent-select" v-model="selectedParent" @change="updateGeneVisualization">
        <option v-for="(positions, parent) in exonsPositions" :key="parent" :value="parent">{{ parent }}</option>
      </select>
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
      // figureHtml: null,
      dashAppUrl: null,
      selectedParent: null

    };
  },

  methods: {
    
    processExonsPositions() {
      if (this.geneStructure) {
        const exonsByParent = {};

        this.geneStructure.forEach(gene => {
          const { Parent, start, end } = gene;

          if (!exonsByParent[Parent]) {
            exonsByParent[Parent] = [];
          }

          exonsByParent[Parent].push([start, end]);
        });

        this.exonsPositions = exonsByParent;

        if (Object.keys(this.exonsPositions).length > 0) {
          this.selectedParent = Object.keys(this.exonsPositions)[0];
        }

        console.log('Exons Positions:', this.exonsPositions);
      }
    },

    plotGeneImage() {
      if (!this.selectedParent) return;

      const selectedExonPositions = this.exonsPositions[this.selectedParent];

      fetch('http://localhost:5000/dash/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exonsPositions: selectedExonPositions }),
        mode: 'cors',
      })
        .then(response => response.json())
        .then(() => {
          this.dashAppUrl = `http://localhost:5000/dash/plot?positions=${encodeURIComponent(JSON.stringify(selectedExonPositions))}`;
        })
        .catch(error => {
          console.error('Error fetching gene image:', error);
        });
    },

    fetchGeneStructure() {
      console.log('Gene ID:', this.geneId);

      const requestData = { gene_id: this.geneId };

      fetch('http://localhost:5000/generate/gene-structure', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData),
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
          this.geneStructure = data;
          this.rawApiResponse = JSON.stringify(data, null, 2);
          this.geneStructureFound = true;
          this.processExonsPositions();
        } else {
          this.geneStructureFound = false;
        }
      })
      .catch(error => {
        console.error("Error fetching gene structure:", error);
        this.rawApiResponse = `Failed to fetch data: ${error.message}`;
      });
    },

    updateGeneVisualization() {
      this.plotGeneImage();
    },

    formatExonsPositions() {
      if (!this.exonsPositions) return '';

      return Object.entries(this.exonsPositions).map(([parent, positionsArray]) => {
        return `${parent}: [${positionsArray.map(positions => `(${positions.join(',')})`).join(', ')}]`;
      }).join('\n');
    },
    

  },
};
</script>

<style scoped>
.container {
  width: 90%;
  max-width: 900px;
  margin: 5vh auto;
  padding: 3vw;
  border: 0.3vw solid #ebebeb;
  background-color: rgba(244, 244, 244, 0.6);
  border-radius: 2vw;
  box-shadow: 0.5vw 0.5vw 1vw rgba(144, 143, 143, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box; /* Ensures padding and border are included in the element's total width and height */
}

h1 {
  margin-bottom: 40px; /* Increase space below the title */
  text-align: center; /* Center-align the title */
}

.input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%; /* Ensure the input container takes full width */
}

.input-button-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%; /* Ensure the wrapper takes full width */
}

.textarea {
  background-color: #fff4ee;
  color: #256937;
  padding: 0.5em; /* Reduced padding for thinner height */
  border-radius: 1vw;
  border: 0.2vw solid transparent;
  outline: none;
  font-family: "Heebo", sans-serif;
  font-size: 1vw; /* Reduced font size for thinner height */
  line-height: 1.2; /* Adjusted line-height for thinner height */
  width: 100%; /* Ensure the textarea takes full width */
  transition: all 0.2s;
  box-shadow: 0.5vw 0.3vw 0.5vw rgba(144, 143, 143, 0.5);
  box-sizing: border-box; /* Ensures padding and border are included in the element's total width and height */
}

.textarea:hover {
  background-color: #ffd3aa;
}

.textarea:focus {
  color: #333;
  background-color: #fff;
  border-color: #333;
}

.search-button {
  position: absolute;
  right: 0.7vw;
  background-color: #166844;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 2.4vw;
  height: 2.3vw;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-button:hover {
  background-color: #22a66d;
}

.error-message, .success-message {
  margin-top: 20px;
  width: 100%; /* Ensure message width doesn't exceed container */
  text-align: center; /* Center align the text */
}

.success-message {
  color: green;
}

.error-message {
  color: red;
}

.success-message::before {
  content: '✓ ';
}

.button-image-container {
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: center; /* Center the button horizontally */
}

.plot-button {
  margin-bottom: 10px; /* Add margin to the button */
}

.gene-image-container {
  display: flex;
  align-items: center;
  justify-content: center; /* Center the image horizontally */
  margin-top: 20px; /* Add top margin */
  width: 100%;
}

.gene-image-container img {
  width: 100%; /* Ensure image fills its container */
  max-width: 100%; /* Ensure image does not exceed its container */
}

/* Scrollable text box for exonsPositions */
.scrollable-textbox {
  max-height: 200px;
  min-height: 100px; /* Ensures at least 5 lines of text are visible by default */
  overflow-y: auto;
  width: 100%;
  border: 1px solid #ddd;
  padding: 10px;
  background-color: #f9f9f9;
  margin-top: 20px;
  border-radius: 5px;
  resize: both; /* Allows the text box to be resizable */
  box-sizing: border-box; /* Ensures padding and border are included in the element's total width and height */
}

.figure-iframe {
  width: 100%;
  height: 100px; /* Allow the height to adjust based on the aspect ratio */
  border: none;
  overflow: hidden;
  flex-grow: 1;
}

.figure-container {
  flex-grow: 1; /* Allow the figure container to grow and match the size of its parent */
}

</style>
