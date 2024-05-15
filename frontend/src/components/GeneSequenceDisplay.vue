<template>

  <div class="container">

    <h1>Search Gene Sequence</h1>

    <div class="input-container">
      <input v-model="geneId" placeholder="Enter Gene ID" />
      <button @click="searchGene">Search</button>
    </div>

    <div>
      <textarea v-model="gene_seq_content" rows="7" cols="80" readonly></textarea>
    </div>


  </div>

</template>

<script>
export default {
  data() {
    return {
      geneId: '',
      gene_seq_content: '',
    };
  },
  methods: {
    async searchGene() {
      if (!this.geneId) {
        alert('Please enter a Gene ID');
        return;
      }

      await this.fetchGeneSequence();
    },
    async fetchGeneSequence() {
      try {
        // Make a request to fetch the gene sequence in JSON format
        const response = await fetch(`http://rest.ensembl.org/sequence/id/${this.geneId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch gene sequence: ${response.statusText}`);
        }

        const data = await response.json();
        // this.gene_seq_content = JSON.stringify(data, null, 2); // Display JSON content
        this.gene_seq_content = data.seq; // Display JSON content
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
};
</script>



<style>
.container {
  max-width: 80%; /* Makes the width responsive to the viewport size */
  margin: 20px auto; /* Centers the container horizontally with margin */
  padding: 2%; /* Responsive padding */
  border: 2px solid #ebebeb; /* Adjusted border thickness */
  border-radius: 10px; /* Consistent, moderate border radius */
  background-color: #f4f4f4;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Subtle shadow */
  display: flex;
  flex-direction: column; /* Stacks children vertically */
  align-items: center; /* Aligns children in the center */
}

.input-container {
  width: 100%; /* Full width of its parent container */
  margin-bottom: 20px; /* Adds space below the input container */
  display: flex;
  justify-content: space-between; /* Distributes space evenly */
  align-items: center; /* Aligns items vertically in the center */
}

input[type="text"], textarea {
  width: 70%; /* Responsive width for text input and area */
  padding: 8px; /* Comfortable padding */
  border: 2px solid #ccc; /* Subtle border */
  border-radius: 4px; /* Rounded corners */
  resize: none; /* Disables resizing for textarea */
}

button {
  padding: 10px 15px; /* Padding around the text */
  background-color: #007bff; /* Blue background for visibility */
  color: white; /* Text color */
  border: none; /* No border */
  border-radius: 4px; /* Rounded corners for the button */
  cursor: pointer; /* Pointer cursor on hover */
  transition: background-color 0.3s; /* Smooth transition for hover effect */
}

button:hover {
  background-color: #0056b3; /* Darker blue on hover */
}

@media (max-width: 768px) {
  .input-container, input[type="text"], textarea {
    flex-direction: column; /* Stacks input and textarea vertically on small screens */
    width: 90%; /* Increases width to fit smaller screens */
  }

  button {
    width: 100%; /* Button width is 100% of its container */
    margin-top: 10px; /* Adds space above the button */
  }

  .container {
    padding: 10%; /* Increases padding for smaller screens */
  }
}
</style>
