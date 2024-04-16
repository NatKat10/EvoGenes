
<!-- <template>
  <div class="container">
    <input type="file" ref="file1" @change="handleFileChange('file1')" accept=".fa, .fasta" class="file-input" />
    <input type="file" ref="file2" @change="handleFileChange('file2')" accept=".fa, .fasta" class="file-input" />
    <button @click="runYASS" class="run-button">Run YASS</button>
    <div class="image-container">
      <img v-if="imageSrc" :src="imageSrc" alt="DotPlot Image" class="image" style="width: 100%; height: auto;" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
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
      formData.append('fasta1', this.file1);
      formData.append('fasta2', this.file2);

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
      }
    }
  }
};
</script> -->
<template>
  <div class="container">
    <!-- Sequence text inputs -->
    <textarea v-model="sequence1" placeholder="Enter or paste sequence 1 here" rows="6" cols="50"></textarea>
    <textarea v-model="sequence2" placeholder="Enter or paste sequence 2 here" rows="6" cols="50"></textarea>
    <div>
      <h3>Or upload files:</h3>
      <input type="file" ref="file1" @change="handleFileChange('file1')" accept=".fa, .fasta" class="file-input" />
      <input type="file" ref="file2" @change="handleFileChange('file2')" accept=".fa, .fasta" class="file-input" />
    </div>
    <button @click="runYASS" class="run-button">Run YASS</button>
    <div class="image-container">
      <img v-if="imageSrc" :src="imageSrc" alt="DotPlot Image" class="image" style="width: 100%; height: auto;" />
    </div>
  </div>
</template>

<script>
export default {
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
      } else {
        formData.append('sequence1', this.sequence1);
        formData.append('sequence2', this.sequence2);
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
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.file-input, textarea {
  margin-bottom: 10px;
}

.run-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.run-button:hover {
  background-color: #0056b3;
}

.image-container {
  margin-top: 20px;
}

.image {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
}
</style>

