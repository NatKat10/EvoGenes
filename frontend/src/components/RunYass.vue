<template>
  <div class="container"> <!-- This is the single root element -->
    <!-- Shows a loading spinner when the process is running -->
    <LoaderOverlay :visible="loading" :progress="progress" />
    <!-- Sequence text inputs -->
    <div class="ensemble-section" :class="{ disabled: disableOtherSections && activeSection !== 'ensemble' }">
      <h3>Compare the sequence of two genes:</h3>
      <div class="file-group">
        <div class="file-label-input">
          <label for="file1" class="upload-label">Gene Ensembl ID :</label>
          <textarea class="textarea" v-model="GeneID1" placeholder="Gene Ensembl ID"
            @input="handleInput('ensemble')"></textarea>
        </div>
        <div class="file-label-input">
          <label for="file2" class="upload-label">Gene Ensembl ID :</label>
          <textarea class="textarea" v-model="GeneID2" placeholder="Gene Ensembl ID"
            @input="handleInput('ensemble')"></textarea>
        </div>
      </div>
    </div>

    <div class="sampling-fraction">
      <label for="sampling-fraction-select">Select sampling fraction: <span class="label-space"></span></label>
      <select id="sampling-fraction-select" v-model="selectedSamplingFraction" style="background-color: #E8F8E0;">
        <p></p>
        <option value="0.1">0.1</option>
        <option value="0.01">0.01</option>
        <option value="0.001">0.001</option>
        <option value="all">All Dots</option>
      </select>
      <div class="info-icon1" @click="showSamplingInfo = true">?</div>
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
        <div class="gene-structure-vertical">
          <div ref="geneStructure2" class="gene-structure vertical"></div>
        </div>
        <div class="dotplot-container">
          <div ref="dotplot" class="figure-plot"></div>
          <div class="info-icon" @click="showModal = true">?</div>
        </div>
        <div class="gene-structure-horizontal">
          <div ref="geneStructure1" class="gene-structure horizontal"></div>
        </div>
      </div>
      
      <div ref="parentSelectContainer" class="parent-select-container">
        <div class="parent-select">
          <label for="parent-select1">Select transcript for Gene (X-axis):</label>
          <select id="parent-select1" v-model="selectedParent1" @change="updateGeneStructure('geneStructure1', selectedParent1)" class="styled-select">
            <option v-for="parent in Object.keys(visualizations.exon_intervals1)" :key="parent" :value="parent">{{ parent }}</option>
          </select>
        </div>
        <div class="parent-select">
          <label for="parent-select2">Select transcript for Gene (Y-axis):</label>
          <select id="parent-select2" v-model="selectedParent2" @change="updateGeneStructure('geneStructure2', selectedParent2)" class="styled-select">
            <option v-for="parent in Object.keys(visualizations.exon_intervals2)" :key="parent" :value="parent">{{ parent }}</option>
          </select>
        </div>
      </div>

      <div ref="manualZoom" class="manual-zoom-container">
        <h4>Manual Zoom</h4>
        <div class="zoom-inputs">
          <div class="zoom-input-group">
            <label>X-axis:</label>
            <div class="zoom-input-pair">
              <input v-model.number="manualZoom.x1" type="number" placeholder="Start" class="zoom-input">
              <input v-model.number="manualZoom.x2" type="number" placeholder="End" class="zoom-input">
            </div>
          </div>
          <div class="zoom-input-group">
            <label>Y-axis:</label>
            <div class="zoom-input-pair">
              <input v-model.number="manualZoom.y1" type="number" placeholder="Start" class="zoom-input">
              <input v-model.number="manualZoom.y2" type="number" placeholder="End" class="zoom-input">
            </div>
          </div>
        </div>
        <!-- Add the dropdown for sampling fraction -->
        <div class="sampling-fraction">
          <label for="manual-sampling-fraction-select">Select Sampling Fraction:<span class="label-space"></span></label>
          <select id="manual-sampling-fraction-select" v-model="manualSamplingFraction">
            <option value="0.1">0.1</option>
            <option value="0.01">0.01</option>
            <option value="0.001">0.001</option>
            <option value="all">All Dots</option>
          </select>
        </div>
        <div class="zoom-button-container">
          <button id="apply-zoom-button" @click="applyManualZoom">Apply Zoom</button>
        </div>
      </div>
    </div>

    <div v-if="showSamplingInfo" class="modal-overlay" @click.self="showSamplingInfo = false">
      <div class="modal-content">
        <h3>Sampling Fraction Information</h3>
        <p>Select the fraction of dots to display in the dotplot:</p>
        <ul>
          <li>0.1: Display 10% of the dots</li>
          <li>0.01: Display 1% of the dots</li>
          <li>0.001: Display 0.1% of the dots</li>
          <li>All Dots: Display all dots</li>
        </ul>
        <p>If the selected genes have more than 40,000 alignments, only 40% of the dots will be shown to improve performance.</p>
        <p> Recommend For long genes, samples positions will increase speed</p>

        <button id="Sbutton" @click="showSamplingInfo = false">Close</button>
      </div>
    </div>

    <!-- Export button as image -->
    <div class="export-button" v-if="visualizations">
      <img src="@/assets/camera.png" alt="Export" @click="captureScreenshot" style="cursor: pointer;" />
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
import Plotly from 'plotly.js-dist';
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
      selectedSamplingFraction: '0.1',  // Default value
      comparison_id: null,
      initialDotplotState: null,
      initialGeneStructure1State: null,
      initialGeneStructure2State: null,
      manualZoom: {
        x1: null,
        x2: null,
        y1: null,
        y2: null
      },
      isResetting: false,
      isRunning: false,
      manualSamplingFraction: 'all',    // Default value for manual zoom to "all dots"
      showSamplingInfo: false  // For showing the sampling info modal



    };
  },
  mounted() {
    this.comparison_id = (this.$route && this.$route.params && this.$route.params.comparison_id) || (this.visualizations && this.visualizations.comparison_id);

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
      this.isRunning = true;  // Disable the choose box

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
        this.errorMessage = "Please provide two Valid Ensembl Gene IDs.";
        return;
      }

      // Add the selected sampling fraction to the request
      formData.append('samplingFraction', this.selectedSamplingFraction);

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
          this.errorMessage = await response.json();
          throw new Error(this.errorMessage || 'Network response was not ok');
        }

        const data = await response.json();
        console.log("Response Data: ", data);    // Log data received from the backend
        if (data.message) {
          this.errorMessage = data.message;
          this.loading = false;
          this.isRunning = false;
          return;
        }
                // Ensure data has required properties before accessing them
        if (!data.exon_intervals1 || !data.exon_intervals2) {
            throw new Error("Incomplete data received from the server");
        }


        this.visualizations = {
          dotplot_data: data.dotplot_plot,
          gene_structure1_plot: data.gene_structure1_plot,
          gene_structure2_plot: data.gene_structure2_plot,
          exon_intervals1: data.exon_intervals1,
          exon_intervals2: data.exon_intervals2,
          comparison_id: data.comparison_id,
          data_for_manual_zoom: data.data_for_manual_zoom  // Set the data for manual zoom
        };
        this.comparison_id = data.comparison_id;
        this.yassOutput = data.yass_output;
        this.selectedParent1 = Object.keys(data.exon_intervals1)[0];
        this.selectedParent2 = Object.keys(data.exon_intervals2)[0];

        // Capture the initial state
        this.initialDotplotState = JSON.parse(JSON.stringify(this.visualizations.dotplot_data));
        this.initialGeneStructure1State = JSON.parse(JSON.stringify(this.visualizations.gene_structure1_plot));
        this.initialGeneStructure2State = JSON.parse(JSON.stringify(this.visualizations.gene_structure2_plot));

        this.$nextTick(() => {
          this.renderDotplot();
          this.renderGeneStructure(this.$refs.geneStructure1, this.visualizations.gene_structure1_plot);
          this.renderGeneStructure(this.$refs.geneStructure2, this.visualizations.gene_structure2_plot);
        });

        this.clearInputs();
      } catch (error) {
        console.error('Error running Evo Genes:', error);
        this.errorMessage = "Please Provide Vaild Ensembl Gene ID";
      } finally {
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
    renderDotplot() {
    const { dotplot_data } = this.visualizations;
    if (dotplot_data && dotplot_data.data && dotplot_data.layout) {
      Plotly.newPlot(this.$refs.dotplot, dotplot_data.data, dotplot_data.layout)
        .then(plot => {
          if (!this.initialDotplotState) {
            this.initialDotplotState = JSON.parse(JSON.stringify(dotplot_data));
          }
          plot.on('plotly_relayout', eventData => {
            if (this.isResetting) return;
            console.log('Zoom event data:', eventData);
            if (eventData['xaxis.range[0]'] && eventData['xaxis.range[1]']) {
              const x0 = eventData['xaxis.range[0]'];
              const x1 = eventData['xaxis.range[1]'];
              const y0 = eventData['yaxis.range[0]'];
              const y1 = eventData['yaxis.range[1]'];
              this.applySyncedZoom(x0, x1, y0, y1);
            } else {
              console.log('Resetting to initial state');
              this.resetPlots();
            }
          });
        });
    } else {
      console.error('Invalid dotplot data:', dotplot_data);
      }
    },

    renderGeneStructure(ref, plotData, isVertical) {
      if (plotData && plotData.data && plotData.layout) {
        if (ref === this.$refs.geneStructure2 || isVertical) {
          plotData.layout = {
            ...plotData.layout,  // Preserve any existing layout properties
            width: 550,
            height: 90,
            xaxis: {
              ...plotData.layout.xaxis,  // Preserve existing xaxis properties
              showgrid: true,
              side: 'bottom',
              tickangle: -90,
            },
            yaxis: {
              ...plotData.layout.yaxis,  // Preserve existing yaxis properties
              showgrid: false,
              showticklabels: false,
              range: [-0.1, 0.6],
              fixedrange: true,
              side: 'right',
            },
            margin: {l: 60, r: 47, t: 5, b: 45},
            hovermode: 'closest',
          };
          
        } else {
          plotData.layout = {
            ...plotData.layout,
            width: 780,
            height: 90,
            margin: {l: 5, r: 60, t: 5, b: 35},
          }
        }

        Plotly.newPlot(ref, plotData.data, plotData.layout).then(() => {
          if (ref === this.$refs.geneStructure1 && !this.initialGeneStructure1State) {
            this.initialGeneStructure1State = JSON.parse(JSON.stringify(plotData));
          } else if (ref === this.$refs.geneStructure2 && !this.initialGeneStructure2State) {
            this.initialGeneStructure2State = JSON.parse(JSON.stringify(plotData));
          }

          if (isVertical) {
            Plotly.relayout(ref, {
              'xaxis.side': 'bottom',
              'xaxis.tickangle': -90,
              'yaxis.side': 'left'
            });
          }
        });
      } else {
        console.error('Invalid gene structure plot data:', plotData);
      }
    },

  

    applySyncedZoom(x0, x1, y0, y1) {
      console.log('Sending zoom data:', { x0, x1, y0, y1 });

      const zoomData = {
        x0: x0,
        x1: x1,
        y0: y0,
        y1: y1,
        comparison_id: this.comparison_id,
        exon_intervals1: this.visualizations.exon_intervals1,
        exon_intervals2: this.visualizations.exon_intervals2,
        dotplot_data: {
          data: this.visualizations.dotplot_data.data,
          layout: {
            ...this.visualizations.dotplot_data.layout,
            x_label: this.visualizations.dotplot_data.layout.xaxis.title.text,
            y_label: this.visualizations.dotplot_data.layout.yaxis.title.text,
            inverted: this.visualizations.dotplot_data.layout.inverted

          }
        }
      };

      fetch(`${server_domain}/dash/relayout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(zoomData)
      })
        .then(response => response.json())
        .then(data => {
          console.log('Received updated plot data:', data);
          this.visualizations.dotplot_data = data.dotplot_plot;
          this.$nextTick(() => {
            this.renderDotplot();
            this.renderGeneStructure(this.$refs.geneStructure1, data.gene_structure1_plot, false);
            this.renderGeneStructure(this.$refs.geneStructure2, data.gene_structure2_plot, true);
          });
        })
        .catch(error => console.error('Error applying synced zoom:', error));
    },

    renderInitialPlots() {
      if (this.initialDotplotState && this.initialGeneStructure1State && this.initialGeneStructure2State) {
        this.visualizations.dotplot_data = JSON.parse(JSON.stringify(this.initialDotplotState));
        this.visualizations.gene_structure1_plot = JSON.parse(JSON.stringify(this.initialGeneStructure1State));
        this.visualizations.gene_structure2_plot = JSON.parse(JSON.stringify(this.initialGeneStructure2State));
        this.$nextTick(() => {
          this.renderDotplot();
          this.renderGeneStructure(this.$refs.geneStructure1, this.visualizations.gene_structure1_plot, false);
          this.renderGeneStructure(this.$refs.geneStructure2, this.visualizations.gene_structure2_plot, true);
          this.isResetting = false;
        });
      } else {
        console.error('Initial plot states are not captured');
        this.isResetting = false;
      }
    },

    resetPlots() {
      this.isResetting = true;
      this.renderInitialPlots();
    },

    updateGeneStructure(containerRef, selectedParent) {
    const exonIntervals = this.visualizations[containerRef === 'geneStructure1' ? 'exon_intervals1' : 'exon_intervals2'][selectedParent];
    const isVertical = containerRef === 'geneStructure2';
    // console.log(`Updating ${containerRef}, isVertical: ${isVertical}`);

    this.loading = true;  // Set loading to true at the beginning




    fetch(`${server_domain}/dash/plot`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ exonsPositions: exonIntervals, isVertical }),
      mode: 'cors',
    })
      .then(response => response.json())
      .then(plotData => {
        this.renderGeneStructure(this.$refs[containerRef], plotData, isVertical);

        const data_for_manual_zoom = JSON.parse(JSON.stringify(this.visualizations.data_for_manual_zoom));  // Deep clone

        // Determine the new min and max values for the dot plot based on the selected parent intervals
        const newMinX = containerRef === 'geneStructure1' ? Math.min(...exonIntervals.map(interval => interval[0])) : this.visualizations.data_for_manual_zoom.min_x;
        const newMaxX = containerRef === 'geneStructure1' ? Math.max(...exonIntervals.map(interval => interval[1])) : this.visualizations.data_for_manual_zoom.max_x;
        const newMinY = containerRef === 'geneStructure2' ? Math.min(...exonIntervals.map(interval => interval[0])) : this.visualizations.data_for_manual_zoom.min_y;
        const newMaxY = containerRef === 'geneStructure2' ? Math.max(...exonIntervals.map(interval => interval[1])) : this.visualizations.data_for_manual_zoom.max_y;

        // Update the dot plot limits if the x-axis or y-axis intervals have changed
        const dotplotUpdateData = {
          dotplot_data: data_for_manual_zoom,  // Include the necessary data
          x1: newMinX,
          x2: newMaxX,
          y1: newMinY,
          y2: newMaxY,
          sampling_fraction: this.selectedSamplingFraction,
          exon_intervals1: containerRef === 'geneStructure1' ? exonIntervals : this.visualizations.exon_intervals1[this.selectedParent1],
          exon_intervals2: containerRef === 'geneStructure2' ? exonIntervals : this.visualizations.exon_intervals2[this.selectedParent2],
          inverted: data_for_manual_zoom.inverted
        };

        fetch(`${server_domain}/dash/dotplot/update_limits`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(dotplotUpdateData),
          mode: 'cors',
        })
          .then(response => response.json())
          .then(data => {
            this.visualizations.dotplot_data = data.dotplot_plot;
            this.$nextTick(() => {
              this.renderDotplot();
            });
          })
          .catch(error => console.error('Error updating dotplot:', error))
          .finally(() => {
            this.loading = false;  // Set loading to false after data update
          });
      })
      .catch(error => {
        console.error('Error updating gene structure:', error);
        this.loading = false;  // Set loading to false if an error occurs
      });
    },
    clearManualZoomInputs() {
      this.manualZoom.x1 = null;
      this.manualZoom.x2 = null;
      this.manualZoom.y1 = null;
      this.manualZoom.y2 = null;
    },


    async applyManualZoom() {
      this.errorMessage = '';
      try {
        if (!this.visualizations || !this.visualizations.dotplot_data || !this.visualizations.data_for_manual_zoom) {
          throw new Error('Dotplot data or data for manual zoom is missing');
        }

        // Ensure the manual zoom coordinates are present

        if (this.manualZoom && this.manualZoom.x1 !== null && this.manualZoom.x2 !== null &&
          this.manualZoom.y1 !== null && this.manualZoom.y2 !== null) {
          const { x1, x2, y1, y2 } = this.manualZoom;

          const data_for_manual_zoom = JSON.parse(JSON.stringify(this.visualizations.data_for_manual_zoom));  // Deep clone

          const requestData = {
            dotplot_data: data_for_manual_zoom,  // Include the necessary data
            x1: x1,
            x2: x2,
            y1: y1,
            y2: y2,
            sampling_fraction: this.manualSamplingFraction,  // Include the selected sampling fraction
            exon_intervals1: this.visualizations.exon_intervals1,
            exon_intervals2: this.visualizations.exon_intervals2,
            inverted: data_for_manual_zoom.inverted

          };

          this.loading = true;
          this.progress = 0;

          fetch(`${server_domain}/dash/dotplot/plot_update`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData),
            mode: 'cors',
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then(data => {
              this.visualizations.dotplot_data = data.dotplot_plot; // Update dotplot data
              this.visualizations.gene_structure1_plot = data.gene_structure1_plot; // Update gene structure plot
              this.visualizations.gene_structure2_plot = data.gene_structure2_plot; // Update gene structure plot
              this.$nextTick(() => {
                this.renderDotplot();
                this.renderGeneStructure(this.$refs.geneStructure1, this.visualizations.gene_structure1_plot, false);
                this.renderGeneStructure(this.$refs.geneStructure2, this.visualizations.gene_structure2_plot, true);
              });
              this.clearManualZoomInputs();  // Clear the manual zoom inputs
            })
            .catch(error => {
              console.error('Error updating dotplot:', error);
            });
        } else {
          this.errorMessage = "Please fill in all zoom coordinates";
          throw new Error('Please fill in all zoom coordinates');
        }
      } catch (error) {
        this.errorMessage = "Invalid zoom coordinates: x1 should be less than x2 and y1 should be less than y2";
        console.error('Error in applyManualZoom:', error.message);
      } finally {
        this.loading = false;
        this.progress = 100;
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
        y_label: dotplot_data.y_label,
        isVertical: true,
        dotplot_width: 780,
        dotplot_height: 550
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
          this.renderGeneStructure(this.$refs.geneStructure1, data.gene_structure1_plot, false);
          this.renderGeneStructure(this.$refs.geneStructure2, data.gene_structure2_plot, true);
          this.$nextTick(() => {
            Plotly.react(this.$refs.dotplot, data.dotplot_plot.data, data.dotplot_plot.layout);
          });
          console.log('Relayout data applied successfully');
        })
        .catch(error => {
          console.error('Error sending relayout data:', error);
        });
    },

    captureScreenshot() {
  const combinedVisualization = document.querySelector('.visualization-container');
  const exportButton = document.querySelector('.export-button');
  const parentSelect1Container = document.querySelector('.parent-select-container');
  const manualZoom = this.$refs.manualZoom;

  if (combinedVisualization) {
    console.log('Combined visualization element found');

    // Hide the export button, parent selections, and manual zoom
    exportButton.style.display = 'none';
    if (parentSelect1Container) parentSelect1Container.style.display = 'none';
    if (manualZoom) manualZoom.style.display = 'none';

    html2canvas(combinedVisualization).then(canvas => {
      // Show the export button, parent selections, and manual zoom again
      exportButton.style.display = '';
      if (parentSelect1Container) parentSelect1Container.style.display = '';
      if (manualZoom) manualZoom.style.display = '';

      const link = document.createElement('a');
      link.download = 'combined_visualization.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
    });
  } else {
    console.error('Combined visualization element not found');
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
  max-width: 1200px;
  /* Increased maximum width */
  margin: 2vh auto;
  padding: 1vw;
  border: 0.3vw solid #ebebeb;
  background-color: rgba(244, 244, 244, 0.6);
  /* Slightly transparent background */
  border-radius: 2vw;
  box-shadow: 0.5vw 0.5vw 1vw rgba(144, 143, 143, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  margin-bottom: 2vw;
  /* Increase space below the title */
  font-size: 2.5vw;
  /* Responsive font size */
}

h3 {
  margin-bottom: 2vw;
  /* Increase space below the title */
  font-size: 2vw;
  /* Responsive font size */
  text-align: center;
}

.txt1,
.txt2 {
  display: flex;
  justify-content: center;
  /* Center horizontally */
  width: 100%;
}

.txt2 {
  margin-top: 2vw;
  /* Add space between the two text boxes */
}

.textarea {
  background-color: #c3c3c3;
  color: #205119;
  padding: 1em;
  /* Reduced padding for thinner height */
  border-radius: 1vw;
  border: 0.2vw solid transparent;
  outline: none;
  font-family: "Heebo", sans-serif;
  font-size: 1vw;
  /* Reduced font size for thinner height */
  line-height: 1.2;
  /* Adjusted line-height for thinner height */
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
  justify-content: space-evenly;
  /* Distribute space evenly */
  align-items: center;
  /* Align items vertically in the center */
  flex-wrap: wrap;
  /* Allow items to wrap on smaller screens */
  gap: 2vw;
  /* Gap between the file inputs */
}

.file-label-input {
  display: flex;
  flex-direction: column;
  /* Stack label and input vertically */
  align-items: center;
  /* Center-align the contents */
  width: 45%;
  /* Responsive width */
}

.upload-label {
  margin-bottom: 0.5vw;
  /* Space between label and input */
  font-size: 1vw;
  /* Responsive font size */
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
  margin-right: 0;
  /* Removes margin from the last upload button */
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
  justify-content: center;
  /* Centers the button horizontally */
  width: 100%;
  /* Ensure the flex container spans the full width */
  margin-top: 2vw;
  /* Add margin for spacing */
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

button>span {
  position: absolute;
  z-index: -1;
  width: 33.333%;
  height: 100%;
  background: transparent;
  opacity: 0.5;
}

button> :first-child {
  left: 0;
  top: 0;
}

button> :last-child {
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
  display: grid;
  grid-template-columns: 90px 780px;
  grid-template-rows: 550px 90px;
  width: 870px;
  height: 640px;
  margin: 0 auto;
  position: relative;
}

.gene-structure-vertical {
  grid-column: 1 / 2;
  grid-row: 1 / 2;
  width: 100px;
  height: 550px;
  position: relative;
  overflow: visible;
}

.gene-structure.vertical {
  width: 550px;
  height: 90px;
  transform: rotate(90deg) translateX(-550px);
  transform-origin: top left;
  position: absolute;
  left: 90px;
  top: 550px;
}

.dotplot-container {
  grid-column: 2 / 3;
  grid-row: 1 / 2;
  width: 780px;
  height: 550px;
}

.gene-structure-horizontal {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
  width: 780px;
  height: 90px;
}

.gene-structure.horizontal {
  width: 100%;
  height: 100%;
}

.figure-plot {
  width: 100%;
  height: 100%;
}

.manual-zoom-container {
  margin-top: 20px;
}

.figure-iframe {
  width: 100%;
  height: 870px;
  border: none;
}

.parent-select-container {
  margin-bottom: 10px;
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
  z-index: 10;

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

.sampling-fraction {
  margin-top: 30px;
  /* Adjust this value as needed */
}

#sampling-fraction-select {
  background-color: #E8F8E0;
  border-radius: 60px;
  /* Makes the box elliptical */
  padding: 5px;
  /* Adds some padding for better appearance */
  border: 1px solid #ccc;
  /* Optional: adds a border */

}

#manual-sampling-fraction-select {
  background-color: #E8F8E0;
  border-radius: 60px;
  /* Makes the box elliptical */
  padding: 5px;
  /* Adds some padding for better appearance */
  border: 1px solid #ccc;
  /* Optional: adds a border */

}

.label-space {
  margin-left: 10px;
  /* Adjust this value as needed to increase space after the colon */
}

#apply-zoom-button {
  display: flex;
  justify-content: center;
  /* Centers the button horizontally */
  margin: 0 auto;
  /* Center align the button */
  margin-top: 20px;
}
#Sbutton{
  display: flex;
  justify-content: center;
  /* Centers the button horizontally */
  margin: 0 auto;
  /* Center align the button */
  margin-top: 20px;
  width: 25%;
}

.export-button img {
  width: 50px;
  /* Adjust the size as needed */
  height: auto;
}




.zoom-inputs {
  display: flex;
  flex-direction: column;
  gap: 10px;
  /* Add space between the input groups */
}

.zoom-input-group {
  display: flex;
  align-items: center;
  gap: 10px;
  /* Add space between the label and the input pair */
}

.zoom-input-pair {
  display: flex;
  gap: 10px;
  /* Add space between the start and end inputs */
}
.info-icon1 {
  display: inline-block;
  margin-left: 10px;
  width: 20px;
  height: 20px;
  background-color: #5c715d;
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 20px;
  cursor: pointer;
}

.zoom-input {
  background-color: #c3c3c3;
  color: #205119;
  padding: 1em;
  /* Adjust padding for thicker input boxes */
  height: 3em;
  /* Adjust height for thicker input boxes */
  border-radius: 1vw;
  border: 0.2vw solid transparent;
  outline: none;
  font-family: "Heebo", sans-serif;
  font-size: 1vw;
  line-height: 1.2;
  width: 100%;
  transition: all 0.2s;
  box-shadow: 0.5vw 0.3vw 0.5vw rgba(184, 184, 184, 0.5);
}

.zoom-input:hover {
  background-color: #5a7f5ee9;
  color: #ffffff;
}

.zoom-input:focus {
  color: #333;
  background-color: #fff;
  border-color: #333;
}

.modal-content{
  background: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 40%;
  max-height: 80%;
  overflow: auto;
}
</style>
