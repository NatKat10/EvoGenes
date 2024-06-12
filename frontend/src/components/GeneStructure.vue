<template>
  <div class="container">
    <h3>Popular Gene Sequences</h3>

    <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="3" aria-label="Slide 4"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="4" aria-label="Slide 5"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="5" aria-label="Slide 6"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="6" aria-label="Slide 7"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img :src="images[0]" class="d-block w-100 carousel-image" alt="Slide 1" @click="openModal(0)" title="Click for popular sequences">
        </div>
        <div class="carousel-item" v-for="(image, index) in images.slice(1)" :key="index + 1">
          <img :src="image" class="d-block w-100 carousel-image" :alt="'Slide ' + (index + 2)" @click="openModal(index + 1)" title="Click for popular sequences">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>

    <transition name="modal-fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <button class="close-button" @click="closeModal">X</button>
          <h3>{{ modalTitles[currentSlide] }}</h3>
          <table>
            <thead>
              <tr>
                <th>Gene Name</th>
                <th>Ensembl Gene ID</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in tableData[currentSlide]" :key="row.id">
                <td>{{ row.col1 }}</td>
                <td>{{ row.col2 }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'GeneStructure',
  data() {
    return {
      showModal: false,
      currentSlide: 0,
      images: [
        require('../assets/person1.png'),
        require('../assets/monkey.png'),
        require('../assets/pig.png'),
        require('../assets/fish.png'),
        require('../assets/bacter.png'),
        require('../assets/mouse.png'),
        require('../assets/Ecoli.png')
      ],
      modalTitles: [
        'Humans (Homo sapiens)',
        'Rhesus Monkeys (Macaca mulatta)',
        'Pigs (Sus scrofa)',
        'Zebrafish (Danio rerio)',
        'Nematodes (Caenorhabditis elegans)',
        'Mice (Mus musculus)',
        'Escherichia coli (E. coli)'
        
      ],
      tableData: [
        [
          { id: 1, col1: 'BRCA1', col2: 'ENSG00000012048' },
          { id: 2, col1: 'BRCA2', col2: 'ENSG00000139618' },
          { id: 3, col1: 'TP53', col2: 'ENSG00000141510' },
          { id: 4, col1: 'CFTR', col2: 'ENSG00000001626' },
          { id: 5, col1: 'HBB', col2: 'ENSG00000244734' },
          { id: 6, col1: 'APOE', col2: 'ENSG00000130203' }
        ],
        [
          { id: 1, col1: 'TP53', col2: 'ENSMMUG00000008639' },
          { id: 2, col1: 'BRCA1/BRCA2', col2: 'ENSMMUG00000001329' },
          { id: 3, col1: 'APOE', col2: 'ENSMMUG00000014305' },
          { id: 4, col1: 'DRD4', col2: 'ENSMMUG00000002658' }
        ],
        [
          { id: 1, col1: 'RAG1/RAG2', col2: 'ENSSSCG00040015624' },
          { id: 2, col1: 'MC4R', col2: 'ENSSSCG00000051798' },
          { id: 3, col1: 'ESR1', col2: 'ENSSSCG00070026203' },
          { id: 4, col1: 'LEP', col2: 'ENSSSCG00070028207' },
          { id: 5, col1: 'TP53', col2: 'ENSSSCG00025036064' }
        ],
        [
          { id: 1, col1: 'tp53', col2: 'ENSDARG00000035559' },
          { id: 2, col1: 'gata1', col2: 'ENSDARG00000013477' },
          { id: 3, col1: 'dmd', col2: 'ENSDARG00000008487' },
          { id: 4, col1: 'cryaa', col2: 'ENSDARG00000053502' },
          { id: 5, col1: 'notch1a', col2: 'ENSDARG00000103554' },
        ],
        [
          { id: 1, col1: 'unc-54', col2: 'WBGene00006789' },
          { id: 2, col1: 'daf-2', col2: 'WBGene00000898' },
          { id: 3, col1: 'egl-1', col2: 'WBGene00001170' },
          { id: 4, col1: 'lin-4', col2: 'WBGene00002993' },
          { id: 5, col1: 'ced-3', col2: 'WBGene00000417' },

        ],
        [
          { id: 1, col1: 'P53 (Trp53)', col2: 'ENSMUSG00000027472' },
          { id: 2, col1: 'Myc', col2: 'ENSMUSG00000022346' },
          { id: 3, col1: 'Lepr', col2: 'ENSMUSG00000057722' },
          { id: 4, col1: 'Fmr1', col2: 'ENSMUSG00000000838' },
          { id: 5, col1: 'Apoe', col2: 'ENSMUSG00000002985' }
        ],
        [
          { id: 1, col1: 'Gene G1', col2: 'Sequence G1' },
          { id: 2, col1: 'Gene G2', col2: 'Sequence G2' }
        ]
      ]
    };
  },
  methods: {
    openModal(index) {
      this.currentSlide = index;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    }
  }
};
</script>

<style scoped>
.carousel {
  width: 100%;
  max-width: 90%;
  margin-bottom: 1rem; /* Add space below the carousel */
}

.carousel-inner {
  max-height: 30vh; /* Adjust the height to ensure images are not cropped */
}

.carousel-inner img {
  max-height: 30vh; /* Adjust the height to ensure images are not cropped */
  object-fit: contain; /* Ensure the entire image is visible */
  cursor: pointer; 
}

.carousel-image {
  box-shadow: 0 4px 8px rgba(96, 96, 96, 0.1);
  transition: all 0.3s ease;
}

.carousel-image:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
  background-color: rgb(98, 98, 98);
  border-radius: 50%;
}

.carousel-control-prev-icon:hover,
.carousel-control-next-icon:hover {
  background-color: rgb(10, 10, 10);
}

.carousel-indicators {
  bottom: -60px; /* Move indicators below the image */
}

.carousel-indicators [data-bs-target] {
  background-color: rgb(60, 60, 60);
  width: 40px; /* Make indicators thicker */
  height: 5px; /* Make indicators thicker */
}

.carousel-indicators [data-bs-target]:hover {
  background-color: rgb(23, 23, 23);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(50, 50, 50, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  background: rgb(255, 255, 255);
  padding: 1.8vw;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.34);
  width: 80%;
  max-width: 40vw;
  max-height: 60vh; /* Reduce the height of the modal box */
  overflow-y: auto; /* Add scroll for overflowing content */
  position: relative;
}

.close-button {
  position: absolute;
  top: 1vw;
  right: 1vw;
  background: transparent;
  border: none;
  font-size: 1em; /* Reduce the font size */
  cursor: pointer;
  background: rgba(255, 0, 0, 0.5);
  color: white;
  padding: 0.5em;
}

.close-button:hover {
  background-color: rgb(221, 18, 18);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1vw;
}

th, td {
  border: 1px solid #dddddd;
  padding: 0.5vw;
}

th {
  background-color: #f2f2f2;
}

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.5s;
}

.modal-fade-enter, .modal-fade-leave-to /* .modal-fade-leave-active in <2.1.8 */ {
  opacity: 0;
}

.container {
  width: 90%;
  max-width: 78%;
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

h3 {
  margin-bottom: 1rem; /* Add space between the heading and the carousel */
  font-size: 2vw;
}

@media (max-width: 768px) {
  .container {
    padding: 4vw;
  }

  h3 {
    font-size: 4vw;
  }

  .carousel-inner {
    max-height: 50vh; /* Adjust the height for smaller screens */
  }

  .carousel-inner img {
    max-height: 50vh; /* Adjust the height for smaller screens */
  }

  .modal-content {
    padding: 4vw;
  }

  .close-button {
    top: 2vw;
    right: 2vw;
    font-size: 1.5em; /* Adjusted size */
    padding: 0.5em;
  }

  table {
    font-size: 2vw;
  }

  th, td {
    padding: 1vw;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 6vw;
  }

  h3 {
    font-size: 6vw;
  }

  .carousel-inner {
    max-height: 60vh; /* Adjust the height for smaller screens */
  }

  .carousel-inner img {
    max-height: 60vh; /* Adjust the height for smaller screens */
  }

  .modal-content {
    padding: 6vw;
  }

  .close-button {
    top: 3vw;
    right: 3vw;
    font-size: 2em; /* Adjusted size */
    padding: 0.5em;
  }

  table {
    font-size: 3vw;
  }

  th, td {
    padding: 1.5vw;
  }
}
</style>
