<template>
  <div class="container">
    <!-- Shows a loading spinner when the process is running -->
    <LoaderOverlay :visible="loading" :progress="progress" />
    <!-- Sequence text inputs -->
    <div class="ensemble-section" :class="{ disabled: disableOtherSections && activeSection !== 'ensemble'}">
      <h3>Enter Ensembl Gene ID:</h3>
      <div class="file-group">
        <div class="file-label-input">
          <label for="file1" class="upload-label">Enter Gene ID for Gene 1:</label>
          <textarea class="textarea" v-model="GeneID1" placeholder="Enter Gene ID 1 here" @input="handleInput('ensemble')"></textarea>
        </div>
        <div class="file-label-input">
          <label for="file2" class="upload-label">Enter Gene ID for Gene 2:</label>
          <textarea class="textarea" v-model="GeneID2" placeholder="Enter Gene ID 2 here" @input="handleInput('ensemble')"></textarea>
        </div>
      </div>
    </div>

    <div class="btn">
      <button @click="runEvoGenes">
        <span></span>
        Run Evo Genes
        <span></span>
      </button>
    </div>

    <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>

    <div class="visualization-container" v-if="visualizations">
      <div class="graph-container">
        <div class="dotplot-container">
          <div ref="dotplot" class="figure-plot"></div>
          <div class="info-icon" @click="showModal = true">?</div>
        </div>
        <div class="gene-structure-container">
          <div ref="geneStructure1" class="gene-structure"></div>
          <div ref="geneStructure2" class="gene-structure"></div>

          <div class="parent-select-container">
            <label for="parent-select1">Select Parent for Gene 1:   </label>
            <select id="parent-select1" v-model="selectedParent1" @change="updateGeneStructure('geneStructure1', selectedParent1)" class="styled-select">
              <option v-for="parent in Object.keys(visualizations.exon_intervals1)" :key="parent" :value="parent">{{ parent }}</option>
            </select>
          </div>
          
          <div class="parent-select-container">
            <label for="parent-select2">Select Parent for Gene 2:   </label>
            <select id="parent-select2" v-model="selectedParent2" @change="updateGeneStructure('geneStructure2', selectedParent2)" class="styled-select">
              <option v-for="parent in Object.keys(visualizations.exon_intervals2)" :key="parent" :value="parent">{{ parent }}</option>
            </select>
          </div>
        </div>
      </div>

      <div class="manual-zoom-container">
        <h4>Manual Zoom</h4>
        <div class="zoom-inputs">
          <div>
            <label>X-axis: </label>
            <input v-model.number="manualZoom.x1" type="number" placeholder="Start">
            <input v-model.number="manualZoom.x2" type="number" placeholder="End">
          </div>
          <div>
            <label>Y-axis: </label>
            <input v-model.number="manualZoom.y1" type="number" placeholder="Start">
            <input v-model.number="manualZoom.y2" type="number" placeholder="End">
          </div>
        </div>
        <button @click="applyManualZoom">Apply Zoom</button>
      </div>

      <!-- Export button as image -->
      <div class="export-button" v-if="visualizations">
        <img src="@/assets/camera.png" alt="Export" @click="captureScreenshot" style="cursor: pointer;"/>
      </div>
    </div>
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content">
        <h3>YASS Alignment Summary:</h3>
        <pre>{{ yassOutput }}</pre>
        <button @click="showModal = false">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import html2canvas from 'html2canvas';

import LoaderOverlay from './LoaderOverlay.vue';
// This import is used to get the server domain for making API requests
import { server_domain } from '@/server_domain';

export default {
  name: 'RunEvoGenes',
  components: {
    LoaderOverlay
  },
  data() {
    return {
      errorMessage: '',
      sequence1: '',
      sequence2: '',
      GeneID1: '',
      GeneID2: '',
      file1: null,
      file2: null,
      visualizations: null,
      selectedParent1: null,
      selectedParent2: null,
      activeSection: null,
      loading: false,
      progress: 0,
      dashDotplotUrl: null,
      yassOutput: '',
      showModal: false,
      comparison_id: null,
      manualZoom: {
        x1: null,
        x2: null,
        y1: null,
        y2: null
      },
    };
  },
  mounted() {
    this.comparison_id = this.$route.params.comparison_id || (this.visualizations && this.visualizations.comparison_id);
  },
  computed: {
    disableOtherSections() {
      return this.sequence1 || this.sequence2 || this.file1 || this.file2 || this.GeneID1 || this.GeneID2;
    },
  },
  methods: {
    handleInput(section) {
      this.activeSection = section;
    },
    clearInputs() {
      this.file1 = null;
      this.file2 = null;
      this.sequence1 = '';
      this.sequence2 = '';
      this.GeneID1 = '';
      this.GeneID2 = '';
      this.errorMessage = '';
      const fileInput1 = this.$refs.file1;
      const fileInput2 = this.$refs.file2;
      if (fileInput1) fileInput1.value = '';
      if (fileInput2) fileInput2.value = '';
    },
    handleFileChange(refName) {
      const file = this.$refs[refName].files[0];
      this[refName] = file;
      this.handleInput('upload');
    },
    async runEvoGenes() {
    console.log('Run Evo Genes method called');
    const formData = new FormData();
    if (this.file1 && this.file2) {
      formData.append('fasta1', this.file1);
      formData.append('fasta2', this.file2);
    } else if (this.sequence1 && this.sequence2) {
      formData.append('sequence1', this.sequence1);
      formData.append('sequence2', this.sequence2);
    } else if (this.GeneID1 && this.GeneID2) {
      formData.append('GeneID1', this.GeneID1);
      formData.append('GeneID2', this.GeneID2);
    } else {
      this.errorMessage = "Please provide two sequences or two FASTA files or two Ensembl Gene IDs.";
      return;
    }

    this.loading = true;
    this.progress = 0;

    try {
      const response = await this.fetchWithProgress(`${server_domain}/run-evo-genes`, {
        method: 'POST',
        body: formData
      }, (loaded, total) => {
        this.progress = Math.floor((loaded / total) * 100);
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log("Response Data: ", data);  // Log data received from the backend
      this.visualizations = {
        dotplot_data: data.dotplot_data,
        gene_structure1_html: data.gene_structure1_html,
        gene_structure2_html: data.gene_structure2_html,
        exon_intervals1: data.exon_intervals1,
        exon_intervals2: data.exon_intervals2,
        comparison_id: data.comparison_id
      };
      this.comparison_id = data.comparison_id;
      this.yassOutput = data.yass_output;
      this.selectedParent1 = Object.keys(data.exon_intervals1)[0];
      this.selectedParent2 = Object.keys(data.exon_intervals2)[0];
      this.$nextTick(() => {
        this.insertGeneStructureHTML(this.$refs.geneStructure1, this.visualizations.gene_structure1_html);
        this.insertGeneStructureHTML(this.$refs.geneStructure2, this.visualizations.gene_structure2_html);
      });

      this.clearInputs();
    } catch (error) {
      console.error('Error running Evo Genes:', error);
      this.errorMessage = "Incorrect Input";
    } finally {
      this.clearInputs();
      this.updateDotplot();
      this.loading = false;
      this.progress = 100;
      }
    },
    async fetchWithProgress(url, options, onProgress) {
      const response = await fetch(url, options);
      const reader = response.body.getReader();
      const contentLength = +response.headers.get('Content-Length');

      let receivedLength = 0;
      let chunks = [];

      let done = false;

      while (!done) {
        const { done: readerDone, value } = await reader.read();
        done = readerDone;

        if (value) {
          chunks.push(value);
          receivedLength += value.length;
          onProgress(receivedLength, contentLength);
        }
      }

      let chunksAll = new Uint8Array(receivedLength);
      let position = 0;
      for (let chunk of chunks) {
        chunksAll.set(chunk, position);
        position += chunk.length;
      }

      return new Response(chunksAll, {
        headers: { 'Content-Type': response.headers.get('Content-Type') }
      });
    },
    updateGeneStructure(containerRef, selectedParent) {
      const exonIntervals = this.visualizations[containerRef === 'geneStructure1' ? 'exon_intervals1' : 'exon_intervals2'][selectedParent];
      fetch(`${server_domain}/dash/update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exonsPositions: exonIntervals }),
        mode: 'cors',
      })
        .then(response => response.json())
        .then(() => {
          const plotUrl = `${server_domain}/dash/plot?positions=${encodeURIComponent(JSON.stringify(exonIntervals))}`;
          fetch(plotUrl)
            .then(response => response.text())
            .then(html => {
              this.insertGeneStructureHTML(this.$refs[containerRef], html);
            });
        })
        .catch(error => {
          console.error('Error updating gene structure:', error);
        });
    },
    insertGeneStructureHTML(container, html) {
      container.innerHTML = html;
      const scripts = container.getElementsByTagName('script');
      for (const script of scripts) {
        const newScript = document.createElement('script');
        newScript.text = script.text;
        script.replaceWith(newScript);
      }
    },
    updateDotplot() {
    if (!this.visualizations || !this.visualizations.dotplot_data) return;
    console.log('Updating dotplot with data:', this.visualizations.dotplot_data);  // Log dotplot data
    fetch(`${server_domain}/dash/dotplot/plot`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dotplot_data: this.visualizations.dotplot_data }),
      mode: 'cors',
    })
      .then(response => response.text())
      .then(html => {
        this.insertDotplotHTML(this.$refs.dotplot, html);
      })
      .catch(error => {
        console.error('Error updating dotplot:', error);
        });
    },
    fetchRelayoutData() {
      // Ensure fetchRelayoutData is only called when necessary data is available
      if (!this.comparison_id) {
        console.error('comparison_id is not set');
        return;
      }
      fetch(`${server_domain}/dash/relayout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: 'fetch_relayout', comparison_id: this.comparison_id })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
          throw new TypeError("Received non-JSON response");
        }
        return response.json();
      })
      .then(data => {
        console.log('Relayout data:', data);
      })
      .catch(error => {
        console.error('Error fetching relayout data:', error);
      });
    },
    insertDotplotHTML(container, html) {
    console.log('Inserting dotplot HTML:', html);  // Log HTML to check content
    container.innerHTML = html;

    // Execute any scripts within the newly inserted HTML
    const scripts = container.getElementsByTagName('script');
    for (const script of scripts) {
      const newScript = document.createElement('script');
      newScript.type = 'text/javascript';
      if (script.src) {
        newScript.src = script.src;
      } else {
        newScript.textContent = script.textContent;
      }
      script.parentNode.replaceChild(newScript, script);
    }

    this.addZoomEventListener(container); // Add this line
    },
    addZoomEventListener(container) {
        const dotplot = container.querySelector('.plotly-graph-div');
        if (dotplot) {
            dotplot.on('plotly_relayout', (eventData) => {
                const comparison_id = this.comparison_id;
                const exon_intervals1 = this.visualizations.exon_intervals1;
                const exon_intervals2 = this.visualizations.exon_intervals2;

                if (eventData['xaxis.range[0]'] && eventData['xaxis.range[1]']) {
                    const x0 = eventData['xaxis.range[0]'];
                    const x1 = eventData['xaxis.range[1]'];
                    const y0 = eventData['yaxis.range[0]'];
                    const y1 = eventData['yaxis.range[1]'];
                    console.log(`Zoomed to x: [${x0}, ${x1}], y: [${y0}, ${y1}]`);
                    console.log(`Sending relayout data: x0=${x0}, x1=${x1}, y0=${y0}, y1=${y1}, comparison_id=${comparison_id}`);
                    this.sendRelayoutData(x0, x1, y0, y1, exon_intervals1, exon_intervals2, comparison_id);
                } else {
                    // Axes have been reset, send the original coordinates
                    const originalX0 = this.visualizations.dotplot_data.min_x;
                    const originalX1 = this.visualizations.dotplot_data.max_x;
                    const originalY0 = this.visualizations.dotplot_data.max_y;
                    const originalY1 = this.visualizations.dotplot_data.min_y;
                    console.log('Resetting axes to original coordinates');
                    this.sendRelayoutData(originalX0, originalX1, originalY0, originalY1, exon_intervals1, exon_intervals2, comparison_id);
        }
      });
      }
    },

    sendRelayoutData(x0, x1, y0, y1, exon_intervals1, exon_intervals2, comparison_id, is_manual_zoom = false) {
      const dotplot_data = this.visualizations.dotplot_data;
      const requestBody = { 
        x0, x1, y0, y1, 
        exon_intervals1, 
        exon_intervals2, 
        comparison_id,
        is_manual_zoom,
        directions: dotplot_data.directions,
        min_x: dotplot_data.min_x,
        max_x: dotplot_data.max_x,
        min_y: dotplot_data.min_y,
        max_y: dotplot_data.max_y,
        x_label: dotplot_data.x_label,
        y_label: dotplot_data.y_label
      };
      console.log('Sending relayout data:', JSON.stringify(requestBody, null, 2));
      
      fetch(`${server_domain}/dash/relayout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Received response:', data);
        // Update the gene structure plots and dotplot with the response data
        this.insertGeneStructureHTML(this.$refs.geneStructure1, data.gene_structure1_html);
        this.insertGeneStructureHTML(this.$refs.geneStructure2, data.gene_structure2_html);
        this.insertDotplotHTML(this.$refs.dotplot, data.dotplot_html);
        console.log('Relayout data applied successfully');
      })
      .catch(error => {
        console.error('Error sending relayout data:', error);
      });
    },

    captureScreenshot() {
      const combinedVisualization = document.querySelector('.visualization-container');
      const exportButton = document.querySelector('.export-button');
      if (combinedVisualization) {
        console.log('Combined visualization element found');

        // Hide the export button
        exportButton.style.display = 'none';

        html2canvas(combinedVisualization).then(canvas => {
          // Show the export button again
          exportButton.style.display = '';

          const link = document.createElement('a');
          link.download = 'combined_visualization.png';
          link.href = canvas.toDataURL('image/png');
          link.click();
        });
      } else {
        console.error('Combined visualization element not found');
      }
    },
    // applyManualZoom() {
    //   if (this.manualZoom.x1 !== null && this.manualZoom.x2 !== null &&
    //       this.manualZoom.y1 !== null && this.manualZoom.y2 !== null) {
    //     const { x1, x2, y1, y2 } = this.manualZoom;
    //     this.sendRelayoutData(
    //       x1, x2, y2, y1,
    //       this.visualizations.exon_intervals1,
    //       this.visualizations.exon_intervals2,
    //       this.comparison_id,
    //       true, // is_manual_zoom
    //       this.visualizations.dotplot_data // Include original dotplot data
    //     );
    //   } else {
    //     console.error('Please fill in all zoom coordinates');
    //   }
    // },
applyManualZoom() {
  this.loading = true;
  this.progress = 0;
  
  try {
    if (!this.visualizations || !this.visualizations.dotplot_data) {
      throw new Error('Dotplot data is missing');
    }

    // Ensure the manual zoom coordinates are present
    if (this.manualZoom && this.manualZoom.x1 !== null && this.manualZoom.x2 !== null &&
        this.manualZoom.y1 !== null && this.manualZoom.y2 !== null) {
      
      const { x1, x2, y1, y2 } = this.manualZoom;
      const comparison_id = this.comparison_id;
      const exon_intervals1 = this.visualizations.exon_intervals1;
      const exon_intervals2 = this.visualizations.exon_intervals2;
      
      fetch(`${server_domain}/dash/dotplot/plot_update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          dotplot_data: this.visualizations.dotplot_data,
          x1: x1,
          x2: x2,
          y1: y1,
          y2: y2
        }),
        mode: 'cors',
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      .then(html => {
        this.insertDotplotHTML(this.$refs.dotplot, html);
        this.sendRelayoutData(x1, x2, y1, y2, exon_intervals1, exon_intervals2, comparison_id);
      })
      .catch(error => {
        console.error('Error updating dotplot:', error);
      });
    } else {
      throw new Error('Please fill in all zoom coordinates');
    }
  } catch (error) {
    console.error('Error in applyManualZoom:', error.message);
  } finally {
    this.loading = false;
    this.progress = 100;
  }
}

  }
};
</script>
<style scoped>
.error-message {
  color: red;
  margin-top: 10px;
}
.sequence-section.disabled,
.upload-section.disabled,
.ensemble-section.disabled {
  pointer-events: none;
  opacity: 0.5;
}

.sequence-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.container {
  width: 100%;
  max-width: 1200px; /* Increased maximum width */
  margin: 2vh auto;
  padding: 1vw;
  border: 0.3vw solid #ebebeb;
  background-color: rgba(244, 244, 244, 0.6); /* Slightly transparent background */
  border-radius: 2vw;
  box-shadow: 0.5vw 0.5vw 1vw rgba(144, 143, 143, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  margin-bottom: 2vw; /* Increase space below the title */
  font-size: 2.5vw; /* Responsive font size */
}
h3 {
  margin-bottom: 2vw; /* Increase space below the title */
  font-size: 2vw; /* Responsive font size */
  text-align: center;
}

.txt1, .txt2 {
  display: flex;
  justify-content: center; /* Center horizontally */
  width: 100%;
}

.txt2 {
  margin-top: 2vw; /* Add space between the two text boxes */
}

.textarea {
  background-color: #c3c3c3;
  color: #205119;
  padding: 1em; /* Reduced padding for thinner height */
  border-radius: 1vw;
  border: 0.2vw solid transparent;
  outline: none;
  font-family: "Heebo", sans-serif;
  font-size: 1vw; /* Reduced font size for thinner height */
  line-height: 1.2; /* Adjusted line-height for thinner height */
  width: 100%;
  transition: all 0.2s;
  box-shadow: 0.5vw 0.3vw 0.5vw rgba(184, 184, 184, 0.5);
}

.textarea:hover {
  background-color: #5a7f5ee9;
  color: #ffffff;

  
}

.textarea:focus {
  color: #333;
  background-color: #fff;
  border-color: #333;
}

.upload-section {
  text-align: center;
  margin: 2vw 0;
}

.file-group {
  display: flex;
  justify-content: space-evenly; /* Distribute space evenly */
  align-items: center; /* Align items vertically in the center */
  flex-wrap: wrap; /* Allow items to wrap on smaller screens */
  gap: 2vw; /* Gap between the file inputs */
}

.file-label-input {
  display: flex;
  flex-direction: column; /* Stack label and input vertically */
  align-items: center; /* Center-align the contents */
  width: 45%; /* Responsive width */
}

.upload-label {
  margin-bottom: 0.5vw; /* Space between label and input */
  font-size: 1vw; /* Responsive font size */
}

.upload-box {
  font-size: 1vw;
  background: #ebebeb;
  border-radius: 50px;
  box-shadow: 0.3vw 0.3vw 0.5vw rgb(110, 110, 110);
  width: 100%;
  outline: none;
  padding: 0.5vw 1vw;
}

.upload-box:hover {
  background-color: #ccc;
}

.upload-box:last-child {
  margin-right: 0; /* Removes margin from the last upload button */
}

::-webkit-file-upload-button {
  color: #f4f4f4;
  background: #166844;
  padding: 20px;
  border: none;
  border-radius: 50px;
  box-shadow: 1px 0px 1px 1px rgb(83, 83, 83);
  outline: none;
}

::-webkit-file-upload-button:hover {
  background: #22a66d;
}

.btn {
  display: flex;
  justify-content: center; /* Centers the button horizontally */
  width: 100%; /* Ensure the flex container spans the full width */
  margin-top: 2vw; /* Add margin for spacing */
}

button {
  font: inherit;
  padding: 1vw 2vw;
  background: #166844;
  border: 0.1em solid hsl(186, 54%, 19%);
  border-radius: 100vw;
  cursor: pointer;
  transition: background-color 250ms;
  position: relative;
  isolation: isolate;
  overflow: hidden;
  color: #fff;
}

button:hover,
button:focus-visible {
  background: #22a66d;
}

button > span {
  position: absolute;
  z-index: -1;
  width: 33.333%;
  height: 100%;
  background: transparent;
  opacity: 0.5;
}

button > :first-child {
  left: 0;
  top: 0;
}

button > :last-child {
  right: 0;
  top: 0;
}

button::before {
  content: "";
  position: absolute;
  z-index: -1;
  background: hsl(200 60% 20%);
  width: 10%;
  aspect-ratio: 1;
  border-radius: 50%;
  inset: 0;
  margin: auto;
  opacity: 0;
  transition: transform 1000ms 200ms, opacity 200ms;
}

button:active::before {
  transform: scale(20);
  opacity: 1;
  transition: transform 1000ms, opacity 500ms;
}

button:has(:first-child:active)::before {
  margin-left: 0;
}

button:has(:last-child:active)::before {
  margin-right: 0;
}

button:has(:first-child:active)::before,
button:has(:last-child:active)::before {
  transition: transform 500ms, opacity 250ms;
}

.image-container {
  margin-top: 8vh;
  width: 100%;
}

.image {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
}

@media (max-width: 768px) {
  .container {
    padding: 2vw 1vw;
  }

  h1 {
    font-size: 2vw;
  }

  .textarea {
    font-size: 1.5vw;
    padding: 0.5em;
  }

  .upload-label {
    font-size: 1.5vw;
  }

  .upload-box {
    padding: 0.5vw;
  }

  .btn button {
    padding: 1vw 1.5vw;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 2vw 0.5vw;
  }

  h1 {
    font-size: 1.5vw;
  }

  .textarea {
    font-size: 1.2vw;
    padding: 0.3em;
  }

  .upload-label {
    font-size: 1.2vw;
  }

  .upload-box {
    padding: 0.3vw;
  }

  .btn button {
    padding: 0.5vw 1vw;
  }
}

.visualization-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.graph-container {
  width: 100%;
  display: flex;
  flex-direction: column; /* Ensure the child elements stack vertically */
  align-items: center; /* Center items horizontally */
  position: relative;

}

.dotplot-container {
  flex: 1;
  position: relative;
}

.gene-structure-container {
  /* flex: 1; */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.figure-iframe {
  width: 100%;
  height: 870px;
  border: none;
}

.parent-select-container {
  margin-bottom: 10px;
}

.gene-structure {
  width: 100%;
  height: 90px;
  /* border: 1px solid #ccc; */
  margin-bottom: 20px;
}



.styled-select {
  width: 100%;
  padding: 0.5em;
  font-size: 1.2em;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.styled-select:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.styled-select option {
  padding: 0.5em;
  font-size: 1.2em;
}



.info-icon {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 20px;
  height: 20px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 80%;
  max-height: 80%;
  overflow: auto;
}

	
.yass-output {
  margin-top: 20px;
  width: 100%;
  background: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}


.export-button {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.export-button img {
  width: 50px; /* Adjust the size as needed */
  height: auto;
}
</style>
