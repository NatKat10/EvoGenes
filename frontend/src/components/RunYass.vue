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
import LoaderOverlay from './LoaderOverlay.vue';
// This import is used to get the server domain for making API requests
import { server_domain } from '@/server_domain';

export default {
  name: 'RunEvoGenes',
  components: {
    LoaderOverlay
  },
  data() {
    return {//data properties used in the component
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
    };
  },
  computed: {
    disableOtherSections() {
      return this.sequence1 || this.sequence2 || this.file1 || this.file2 || this.GeneID1 || this.GeneID2;
    },
  },
  methods: {
    //sets the active section based on the input
    handleInput(section) {
      this.activeSection = section;
    },
    //Clears all input fields and error messages
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
    //Handles file input changes and updates the corresponding data properties
    handleFileChange(refName) {//This method is used to handle file input changes
      const file = this.$refs[refName].files[0];//accesses the specific file input element referenced by refName and get the first file
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
      } else if (this.GeneID1 && this.GeneID2) {// append keys geneid1 and geneid2 to formData object
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
          //sends the FormData to the server endpoint /run-evo-genes using a POST request.
          method: 'POST',
          body: formData
        }, (loaded, total) => {
          this.progress = Math.floor((loaded / total) * 100);//The progress of the upload is monitored and updated accordingly
        });
        //in the backend side: The server retrieves the Gene IDs from the form data
        //It fetches the gene sequences from Ensembl using the fetch_sequence_from_ensembl function
        //The fetched sequences are written to temporary FASTA files
        //The YASS alignment tool is run using the temporary FASTA files, and the output is saved to a file.
        //this is what the backend returns:

        //         return jsonify({
        //     'dotplot_data': dotplot_data,
        //     'gene_structure1_html': gene_structure1_body,
        //     'gene_structure2_html': gene_structure2_body,
        //     'exon_intervals1': normalized_exons1,
        //     'exon_intervals2': normalized_exons2,
        //     'yass_output': yass_output
        // })


        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();//response from the server to be converted from JSON format into a JavaScript object
        //the await ensures us that the function waits for the operation to complete before moving to the next line
        console.log("Response Data: ", data); // Debugging: Log the response data
        this.visualizations = {
          dotplot_data: data.dotplot_data,
          gene_structure1_html: data.gene_structure1_html,
          gene_structure2_html: data.gene_structure2_html,
          exon_intervals1: data.exon_intervals1,
          exon_intervals2: data.exon_intervals2
        };
        this.yassOutput = data.yass_output;
        //select the first parent key from the exon intervals data for each gene and assign them to selectedParent1 and selectedParent2
        this.selectedParent1 = Object.keys(data.exon_intervals1)[0];
        this.selectedParent2 = Object.keys(data.exon_intervals2)[0];
        this.$nextTick(() => {//ensures that the DOM is updated before running the provided callback function. 
          //inserts the gene structure HTML into the corresponding geneStructure1 and geneStructure2 elements. 
          this.insertGeneStructureHTML(this.$refs.geneStructure1, this.visualizations.gene_structure1_html);
          this.insertGeneStructureHTML(this.$refs.geneStructure2, this.visualizations.gene_structure2_html);
        });

        this.clearInputs();//method to reset all input fields
      } catch (error) {
        console.error('Error running Evo Genes:', error);
        this.errorMessage = "Incorrect Input";
      } finally {
        this.loading = false;
        this.progress = 100; // Ensure progress reaches 100% when done
        this.clearInputs();
        // Update the dotplot graph
        this.updateDotplot();
      }
    },

    async fetchWithProgress(url, options, onProgress) {// perform this fetch request and to report the progress of the upload (when sending gene id to backend)
      const response = await fetch(url, options);//fetch request to the specified url with the given options GET POST 
      const reader = response.body.getReader();//gets a readable stream reader from the response body
      const contentLength = +response.headers.get('Content-Length');

      let receivedLength = 0; // bytes received so far
      let chunks = []; // array of received binary chunks (comprises the body)

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

      // concatenate chunks into single Uint8Array
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
      //fetches the correct exon interval from visualizations data property
      const exonIntervals = this.visualizations[containerRef === 'geneStructure1' ? 'exon_intervals1' : 'exon_intervals2'][selectedParent];
      fetch(`${server_domain}/dash/update`, {//update the exon positions in endpoint /dash/update 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exonsPositions: exonIntervals }),
        mode: 'cors',
      })
        .then(response => response.json())//convert the response to json 
        .then(() => {//fetch request is made to get the updated gene structure plot
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
      container.innerHTML = html;//Inserts the HTML content into the specified container.
      const scripts = container.getElementsByTagName('script');//Fetches all script tags within the container
      for (const script of scripts) {//Iterates over each script tag

        const newScript = document.createElement('script');//Creates a new script element
        newScript.text = script.text;//Copies the text content from the old script to the new script
        script.replaceWith(newScript);//Replaces the old script tag with the new script tag
      }
    },

    updateDotplot() {
      if (!this.visualizations || !this.visualizations.dotplot_data) return;
      //fetch request to the backend endpoint /dash/dotplot/plot to update the dot plot.
      fetch(`${server_domain}/dash/dotplot/plot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dotplot_data: this.visualizations.dotplot_data }),
        mode: 'cors',
      })
        .then(response => response.text())//Converts the response to text
        .then(html => {//Inserts the HTML into the DOM
          this.insertDotplotHTML(this.$refs.dotplot, html);//Calls insertDotplotHTML to insert the HTML into the specified container
        })
        .catch(error => {
          console.error('Error updating dotplot:', error);
        });
    },

    insertDotplotHTML(container, html) {
      container.innerHTML = html;//Inserts the HTML content into the specified container
      const scripts = container.getElementsByTagName('script');//Fetches all script tags within the container
      for (const script of scripts) {//Iterates over each script tag
        const newScript = document.createElement('script');//Creates a new script element
        newScript.text = script.text;//Copies the text content from the old script to the new script
        script.replaceWith(newScript);//Replaces the old script tag with the new script tag
      }
    },
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
</style>
