<template>
    <div>
      <h1>Gene Input Page hiiiiiiiiii</h1>
      <form @submit.prevent="submitForm">
        <label for="gene1">Gene 1:</label>
        <textarea v-model="gene1" id="gene1" rows="4" cols="50" required></textarea>
        <br>
        <label for="gene2">Gene 2:</label>
        <textarea v-model="gene2" id="gene2" rows="4" cols="50" required></textarea>
        <br>
        <button type="submit">Generate Graph</button>
      </form>
    </div>
  </template>
  
  <script>
  import { server_domain } from '@/server_domain';

  export default {
    data() {
      return {
        gene1: '',
        gene2: '',
        geneId: '', // New data property for gene ID search
        x_fasta_content: '', // New data property for x-fasta content
      };
    },
    methods: {
      submitForm() {
        // Your existing YASS algorithm code
        const requestData = {
          gene_name: 'user_input',  
          sequence1: this.gene1,
          sequence2: this.gene2,
        };
  
        fetch(`${server_domain}/generate`, { 
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData),
        })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          // Handle the response, e.g., display the generated graph
        })
        .catch(error => {
          console.error('Error:', error);
        });
      },
    },
  };
  </script>
  
  <style>
  /* Add your styles here */
  </style>
  