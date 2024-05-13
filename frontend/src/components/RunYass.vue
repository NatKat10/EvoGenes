
<template>
  <div class="container">
    <!-- Sequence text inputs -->
    <div class="txt1">
      <textarea class="textarea" v-model="sequence1" placeholder="Enter or paste sequence 1 here" rows="4" cols="50"></textarea>
    </div>
    <div class="txt2">
      <textarea class="textarea" v-model="sequence2" placeholder="Enter or paste sequence 2 here" rows="4" cols="50"></textarea>
    </div>
    

    <!-- <div class="uplod">
      <h3>Or upload files:</h3>
     

      <input type="file" class="upload-box" ref="file1" @change="handleFileChange('file1')" accept=".fa, .fasta"/>
      

      <input type="file" class="upload-box" ref="file2" @change="handleFileChange('file2')" accept=".fa, .fasta"/>
    </div> -->


    <div class="upload-section">
      <h3>Or upload files:</h3>
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


    <!-- <button @click="runYASS" class="run-button">Run YASS</button> -->
    <div class="btn">
      <button @click="runYASS" >
        <span></span>
        Run Yass
        <span></span>
      </button>
    </div>

<!-- 
    <div class="btn">
      <svg @click="runYASS" id="play" viewBox="0 0 163 163" xmlns="http://www.w3.org/2000/svg">
        <g fill="none">
          <g transform="translate(2.000000, 2.000000)" stroke-width="4">
            <path d="M10,80 C10,118.107648 40.8923523,149 79,149 C117.107648,149 148,118.107648 148,80 C148,41.8923523 117.107648,11 79,11" stroke="#A5CB43"></path>
            <path d="M105.9,74.4158594 L67.2,44.2158594 C63.5,41.3158594 58,43.9158594 58,48.7158594 L58,109.015859 C58,113.715859 63.4,116.415859 67.2,113.515859 L105.9,83.3158594 C108.8,81.1158594 108.8,76.6158594 105.9,74.4158594" stroke="#A3CD3A" fill="rgba(22,22,22,0)"></path>
            <path d="M159,79.5 C159,35.5933624 123.406638,0 79.5,0 C35.5933624,0 0,35.5933624 0,79.5 C0,123.406638 35.5933624,159 79.5,159" stroke="#A5CB43"></path>
          </g>
        </g>
      </svg>
    </div> -->
    

    <div class="image-container">
      <img v-if="imageSrc" :src="imageSrc" alt="DotPlot Image" class="image" style="width: 100%; height: auto;" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'RunYass',
  data() {
    return {
      sequence1: '',
      sequence2: '',
      file1: null,
      file2: null,
      imageSrc: null
    };
  },
  methods: {
    handleFileChange(refName) {
      const file = this.$refs[refName].files[0];
      this[refName] = file;
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
    } else {
        alert("Please provide two sequences or two FASTA files.");
        return;
    }

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
      } catch (error) {
        console.error('Error running YASS:', error);
        alert("Incorrect Input");

      }
    }
  }
};
</script>


<style scoped>
.container {
  max-width: 90vw;
  min-width: 320px;
  margin: 5vh auto;
  padding: 5vw;
  border: 0.3vw solid #ebebeb;
  background-color: #f4f4f4;
  border-radius: 2vw;
  box-shadow: 0.5vw 0.5vw 1vw rgba(144, 143, 143, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
}
  




.file-input {
  margin-bottom: 10px;
}

.txt1{
  display: flex;
  justify-content: space-between;
  
}

.txt2{
  display: flex;
  justify-content: space-between;
  padding: 7vh 0px 8vh 0px;
  
}


.textarea {
  background-color: #fff4ee;
  color: #a81414;
  padding: 1em;
  border-radius: 1vw;
  border: 0.2vw solid transparent;
  outline: none;
  font-family: "Heebo", sans-serif;
  font-size: 1.2vw;
  line-height: 1.8;
  width: 90%;
  height: 10vh;
  transition: all 0.2s;
  box-shadow: 0.5vw 0.3vw 0.5vw rgba(144, 143, 143, 0.5);

}
.btn {
  display: flex;
  justify-content: center; /* Centers the button horizontally */
  width: 100%; /* Ensure the flex container spans the full width */
}

.textarea:hover {
  background-color: #ffd3aa;
}

.textarea:focus {
  color: #333;
  background-color: #fff;
  border-color: #333;
}

.uplod{
  align-items: center;
  text-align: center;
  padding: 0px 0px 6vh;

}

.upload-box {
  font-size: 1vw;
  background: #ebebeb;
  border-radius: 50px;
  box-shadow: 0.3vw 0.3vw 0.5vw rgb(110, 110, 110);
  width: 80%;
  outline: none;
  padding: 0.5vw 1vw;
}

.upload-box:hover {
  background-color: #ccc;
}

.upload-box:last-child {
    margin-right: 0; /* Removes margin from the last upload button */
  }

::-webkit-file-upload-button{
  color: #f4f4f4;
  background: #166844;
  padding: 20px;
  border: none;
  border-radius: 50px;
  box-shadow: 1px 0px 1px 1px rgb(83, 83, 83);
  outline: none;
}
::-webkit-file-upload-button:hover{
  background: #22a66d;

}


/* .run-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.run-button:hover {
  background-color: #0056b3;
} */

.image-container {
  margin-top: 8vh;
}

.image {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
}






button {
  font: inherit;
  padding: 20px 30px;
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
  /* background: hotpink; */
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

.upload-section {
  text-align: center;
  margin: 20px 0;
}

.file-group {
  display: flex;
  justify-content: space-evenly; /* Distribute space evenly */
  align-items: center; /* Align items vertically in the center */
}

.file-label-input {
  display: flex;
  flex-direction: column; /* Stack label and input vertically */
  align-items: center; /* Center-align the contents */
}

.upload-label {
  margin-bottom: 5px; /* Space between label and input */
}



.btn {
  display: flex;
  justify-content: center; /* Centers the button horizontally */
  width: 100%; /* Ensure the flex container spans the full width */
}










</style>


