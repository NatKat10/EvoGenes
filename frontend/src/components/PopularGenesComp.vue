<template>
  <div class="container">
    <div class="card rounded-pill text-center overflow-hidden" style="width: 18rem;">
      <img :src="imageUrl" class="card-img-top clickable-image" @click="openModal" alt="..." />
      <div class="card-body bg-dark text-white">
        <h5 class="card-title">{{ title }}</h5>
        <p class="card-text">{{ description }}</p>
        <a href="#" class="btn btn-light px-3 rounded-pill" @click="openModal">{{ buttonLabel }}</a>
      </div>
    </div>
    
    <transition name="modal-fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <button class="close-button" @click="closeModal">X</button>
          <h3>{{ modalTitle }}</h3>
          <table>
            <thead>
              <tr>
                <th>Gene Name</th>
                <th>Gene Sequence</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in tableData" :key="row.id">
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
  name: 'PopularGenesComp',
  props: {
    imageUrl: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    buttonLabel: {
      type: String,
      required: true
    },
    modalTitle: {
      type: String,
      required: true
    },
    tableData: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      showModal: false
    };
  },
  methods: {
    openModal(event) {
      event.preventDefault();
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 10vh;
}

.card {
  cursor: pointer;
}

.card-img-top {
  cursor: pointer;
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
  background: white;
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
</style>
