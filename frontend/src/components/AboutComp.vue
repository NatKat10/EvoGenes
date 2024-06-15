<template>
  <div class="container">
    <h1>Comprehensive End-to-End Gene Visualization System - "Evo-Genes"</h1>
    <p>
      As part of our final project in the Department of Software and Information Systems Engineering at Ben Gurion University of the Negev, under the guidance of Prof. Guy Shani from the Faculty of Software and Information Systems Engineering and Dr. Tal Shay from the Faculty of Life Sciences, we have developed a comprehensive end-to-end gene visualization system. The laboratory aims to unravel the complexity of how cells with identical genetic information can exhibit diverse functions and phenotypic properties. 
    </p>
    <p>
      A significant challenge in this research is the limited capability to compare gene similarities across species while maintaining the context of the original gene structure.
    </p>
    <p>
      Currently, no system allows for the simultaneous examination of sequence similarities and structural differences between species. To address this challenge, we have created a web-based system that leverages both server-side and client-side programming to interface with the extensive Ensembl database.
    </p>
    <p>
      Our system facilitates intuitive and visually engaging comparative gene sequence analysis, emphasizing the display of exons, thus optimizing comparative gene analysis. This unique feature significantly enhances the accessibility and utility of gene comparison tools, providing biologists and researchers with comprehensive insights into gene development and functional divergence. The system streamlines the comparative analysis process by automating sequence retrieval and aligning gene structures with Dot Plot outputs, thereby boosting research productivity and data analysis efficiency.
    </p>
    <p>
      We have invested considerable effort in the design and development of the system, ensuring a professional and attractive user experience, which is integral to its overall functionality.
    </p>
  </div>
</template>

<script>
export default {
  name: 'GeneVisualization'
}
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
  font-size: 23px;
}

p {
  margin-bottom: 20px; /* Adds space between paragraphs */
  text-align: justify; /* Justifies text for a cleaner look */
  font-size: 18px; /* Sets the font size for the paragraphs */
  line-height: 1.6; /* Adjusts line spacing for better readability */
}
</style>
