<template>
  <div class="container">
    <h1>"Evo-Genes" Help Page</h1>
    <div class="instruction-list">
      <div class="instruction-item" v-for="(item, index) in instructions" :key="index">
        <div class="icon">
          <img v-if="item.image" :src="item.image" :alt="item.title" class="button-image">
          <i v-else :class="item.icon"></i>
        </div>
        <div class="description">
          <h2>{{ item.title }}</h2>
          <div class="description-content">
            <p v-for="(line, idx) in item.description" :key="idx">{{ line }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GeneVisualization',
  data() {
    return {
      instructions: [
        {
          image: require('../assets/camera.png'),
          title: 'Camera',
          description: ['Allows you to capture a screenshot of the visualization and save it as an image file.']
        },
        {
          icon: 'fa fa-info-circle',
          title: 'Help',
          description: ['Offers additional help and support resources for using the "Evo-Genes" web application.']
        },
        {
          icon: 'fa fa-question-circle',
          title: 'Question Mark',
          description: ['Opens a modal with additional information about the YASS alignment summary.']
        },
        {
          icon: 'fa fa-play-circle',
          title: 'Run Evo Genes Button',
          description: [
            'Use this feature to compare gene sequences from the Ensembl database.',
            'Steps:',
            '1. Enter the Ensembl Gene IDs for both genes you want to compare in the provided text areas.',
            '2. Click the "Run Evo Genes" button.',
            '3. The system will fetch the sequences, run the comparison, and display the results.'
          ]
        },
        {
          icon: 'fa fa-sample',
          title: 'Sampling Fraction Dropdown',
          description: [
            'Select the fraction of alignment sequences to display in the dot plot.',
            'Options:',
            '• 0.1 (Default): Displays 10% of the alignment dots.',
            '• 0.01: Displays 1% of the alignment dots.',
            '• 0.001: Displays 0.1% of the alignment dots.',
            '• All Dots: Displays all alignment dots.',
            'Note: If there are more than 40,000 alignment sequences, only 40% of the dots will be shown for performance reasons.'
          ]
        },
        {
          icon: 'fa fa-list',
          title: 'Gene Structure Parent Selection',
          description: [
            'Choose the specific parent exon intervals to visualize for each gene.',
            'Steps:',
            '1. Use the dropdown menus under "Select Parent for Gene 1" and "Select Parent for Gene 2" to choose the desired parent.',
            '2. The visualization will update accordingly.'
          ]
        },
        {
          icon: 'fa fa-search-plus',
          title: 'Manual Zoom',
          description: [
            'Manually zoom into specific regions of the dot plot and gene structure visualizations.',
            'Steps:',
            '1. Enter the desired start and end values for both the X-axis and Y-axis.',
            '2. Select the desired sampling fraction for this zoomed view.',
            '3. Click the "Apply Zoom" button to update the visualizations.'
          ]
        },
        {
          icon: 'fa fa-sync',
          title: 'Synced Zoom',
          description: [
            'Automatically sync the zoom between the dot plot and gene structure visualizations.',
            'Steps:',
            '1. Use the built-in zoom tool in the dot plot to zoom into a specific region.',
            '2. The zoom range will be reflected in the gene structure visualizations, keeping the visualizations in sync.'
          ]
        },
        {
          icon: 'fa fa-download',
          title: 'Export Button',
          description: [
            'Export the combined visualization or individual plots as images.',
            'Steps:',
            '1. To export the combined visualization, click the camera icon.',
            '2. To export individual plots, click the respective export buttons in each plot container.',
            '3. The image(s) will be downloaded automatically.'
          ]
        },
        {
          icon: 'fa fa-info-circle',
          title: 'YASS Alignment Summary',
          description: [
            'View the summary of the YASS alignment process.',
            'Steps:',
            '1. Click the "?" icon in the dot plot container to open the modal.',
            '2. The summary of the alignment will be displayed.'
          ]
        }
      ]
    };
  }
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
  box-sizing: border-box;
}

h1 {
  margin-bottom: 40px;
  text-align: center;
  font-size: 23px;
}

.instruction-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.instruction-item {
  display: flex;
  align-items: center; /* Align items to the center */
  margin-bottom: 20px;
}

.icon {
  margin-right: 10px; /* Adjusted margin for better alignment */
  font-size: 35px;
  align-self: flex-start; /* Align icons with titles */
}

.button-image {
  width: 50px;
  height: auto;
  align-self: flex-start; /* Align images with titles */
}

.description {
  flex: 1;
}

.description h2 {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
  line-height: 1.6; /* Aligns with the icon */
}

.description-content {
  margin-left: 20px; /* Indent numbered sections */
}

.description p {
  margin: 10px 0 0 0;
  font-size: 18px;
  line-height: 1.6;
}
</style>
