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
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img :src="images[0]" class="d-block w-100" alt="Slide 1">
          <div class="carousel-caption">
            <p class="text-danger">Slide 1</p>
            <button @click="openModal(0)" class="btn btn-primary">View Details</button>
          </div>
        </div>
        <div class="carousel-item" v-for="(image, index) in images.slice(1)" :key="index + 1">
          <img :src="image" class="d-block w-100" :alt="'Slide ' + (index + 2)">
          <div class="carousel-caption">
            <p class="text-danger">Slide {{ index + 2 }}</p>
            <button @click="openModal(index + 1)" class="btn btn-primary">View Details</button>
          </div>
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
                <th>Gene Sequence</th>
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
        require('../assets/person.png'),
        require('../assets/monkey.png'),
        require('../assets/pig.png'),
        require('../assets/fish.png'),
        require('../assets/bacter.png'),
        require('../assets/Ecoli.png')
      ],
      modalTitles: [
        'Details for Slide 1',
        'Details for Slide 2',
        'Details for Slide 3',
        'Details for Slide 4',
        'Details for Slide 5',
        'Details for Slide 6'
      ],
      tableData: [
        [
          { id: 1, col1: 'Gene A1', col2: 'Sequence A1' },
          { id: 2, col1: 'Gene A2', col2: 'Sequence A2' }
        ],
        [
          { id: 1, col1: 'Gene B1', col2: 'Sequence B1' },
          { id: 2, col1: 'Gene B2', col2: 'Sequence B2' }
        ],
        [
          { id: 1, col1: 'Gene C1', col2: 'Sequence C1' },
          { id: 2, col1: 'Gene C2', col2: 'Sequence C2' }
        ],
        [
          { id: 1, col1: 'Gene D1', col2: 'Sequence D1' },
          { id: 2, col1: 'Gene D2', col2: 'Sequence D2' }
        ],
        [
          { id: 1, col1: 'Gene E1', col2: 'Sequence E1' },
          { id: 2, col1: 'Gene E2', col2: 'Sequence E2' }
        ],
        [
          { id: 1, col1: 'Gene F1', col2: 'Sequence F1' },
          { id: 2, col1: 'Gene F2', col2: 'Sequence F2' }
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
  max-width: 600px;
}

.carousel-inner img {
  max-height: 400px;
  object-fit: cover;
}

.carousel-caption {
  position: absolute;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.carousel-caption p {
  font-size: 1.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  background: rgb(231, 231, 231);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 500px;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  font-size: 1em;
  cursor: pointer;
  background: rgba(0, 0, 0, 0.5);
  color: white;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
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

@media (max-width: 768px) {
  .container {
    padding: 2vw 1vw;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 2vw 0.5vw;
  }
}
</style>
