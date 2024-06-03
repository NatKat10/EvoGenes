<template>
  <div class="container">
    <LoaderOverlay :visible="loading" />
    <h1>Run YASS Algorithm</h1>
    <h1>Run Evo Genes</h1>
    <!-- Sequence text inputs -->
  <!-- <div class= sequence-section :class="{ disabled: disableOtherSections && activeSection !== 'sequence' }">
    <div class="txt1">
      <textarea class="textarea" v-model="sequence1" placeholder="Enter or paste sequence 1 here" @input="handleInput('sequence')"></textarea>
    </div>
    <div class="txt2">
      <textarea class="textarea" v-model="sequence2" placeholder="Enter or paste sequence 2 here" @input="handleInput('sequence')"></textarea>
    </div>
  </div> -->
    
  <div class="upload-section" :class="{ disabled: disableOtherSections && activeSection !== 'upload' }">
      <!-- <h3>Or upload files:</h3> -->
      <div class="file-group">
        <div class="file-label-input">
          <label for="file1" class="upload-label">Choose FASTA file for Gene1:</label>
          <input type="file" id="file1" class="upload-box" ref="file1" @change="handleFileChange('file1')" accept=".fa, .fasta"/>
        </div>
        <div class="file-label-input">
          <label for="file2" class="upload-label">Choose FASTA file for Gene2:</label>
          <input type="file" id="file2" class="upload-box" ref="file2" @change="handleFileChange('file2')" accept=".fa, .fasta"/>
        </div>
      </div>
    </div>

    <div class="ensemble-section" :class="{ disabled: disableOtherSections && activeSection !== 'ensemble'}">
      <h3>Enter Ensemble Gene ID:</h3>
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
      <button @click="runYASS">
        <span></span>
        Run Evo Genes
        <span></span>
      </button>
    </div>

    <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>

    <div class="image-container">
      <img v-if="imageSrc" :src="imageSrc" alt="DotPlot Image" class="image" />
    </div>
  </div>
</template>

<script>
import LoaderOverlay from './LoaderOverlay.vue';

export default {
  name: 'RunYass',
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
      imageSrc: null,
      activeSection: null,
      loading: false,
    };
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
      // Clear file input fields
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

    async runYASS() {
      console.log('Run YASS method called');
      const formData = new FormData();

      // Append sequences as text or files based on user input
      if (this.file1 && this.file2) {
        formData.append('fasta1', this.file1);
        formData.append('fasta2', this.file2);
      } else if (this.sequence1 && this.sequence2) {
        formData.append('sequence1', this.sequence1);
        formData.append('sequence2', this.sequence2);
      } else if (this.GeneID1 && this.GeneID2) {

        formData.append('GeneID1', this.GeneID1);
        formData.append('GeneID2', this.GeneID2);
      }
       else {
        this.errorMessage = "Please provide two sequences or two FASTA files or two ensemble GeneID.";
        return;
      }

      this.loading = true;

      try {
        const response = await fetch('http://localhost:5000/run-yass', {
          method: 'POST',
          body: formData
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const blob = await response.blob();
        this.imageSrc = URL.createObjectURL(blob);
        this.clearInputs(); // Clear the inputs after successful run
      } catch (error) {
        console.error('Error running YASS:', error);
        this.errorMessage = "Incorrect Input"
      }
      finally{
        this.loading=false;
        this.clearInputs();
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
  width: 90%;
  max-width: 900px;
  margin: 5vh auto;
  padding: 2vw;
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
  background-color: #fff4ee;
  color: #a81414;
  padding: 1em; /* Reduced padding for thinner height */
  border-radius: 1vw;
  border: 0.2vw solid transparent;
  outline: none;
  font-family: "Heebo", sans-serif;
  font-size: 1vw; /* Reduced font size for thinner height */
  line-height: 1.2; /* Adjusted line-height for thinner height */
  width: 90%;
  transition: all 0.2s;
  box-shadow: 0.5vw 0.3vw 0.5vw rgba(144, 143, 143, 0.5);
}

.textarea:hover {
  background-color: #ffd3aa;
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
</style>
