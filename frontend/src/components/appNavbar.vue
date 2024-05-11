<template>
  <div>
    <div class="sidebar" @mouseenter="openSidebar" @mouseleave="closeSidebar">
      <div class="logo">
        <img src="/path-to-your-logo.png" alt="Logo"> <!-- Update path as needed -->
      </div>
      <nav class="nav flex-column">
        <router-link to="/" class="nav-link" @click="keepSidebarOpen"> <i class="fa fa-home"></i> <span>Home</span> </router-link>
        <router-link to="/gene-input" class="nav-link" @click="keepSidebarOpen"><i class="fa fa-dna"></i> <span>Gene Input</span> </router-link>
        <router-link to="/run-yass" class="nav-link" @click="keepSidebarOpen"><i class="fa fa-play"></i><span>Run Yass</span></router-link>
        <router-link to="/gene-sequence/:geneId" class="nav-link" @click="keepSidebarOpen"><i class="fa fa-list"></i><span>Gene Sequence Display</span></router-link>
        <router-link to="/gene-structure" class="nav-link" @click="keepSidebarOpen"><i class="fa fa-project-diagram"></i><span>Gene Structure</span></router-link>
        <router-link to="/about" class="nav-link" @click="keepSidebarOpen"><i class="fa fa-info-circle"></i><span>About</span></router-link>
      </nav>
    </div>
  </div>
</template>




<script>
export default {
  data() {
    return {
      isOpen: false
    };
  },
  methods: {
    openSidebar() {
      this.isOpen = true;
    },
    closeSidebar() {
      this.isOpen = false;
    },
    keepSidebarOpen(event) {
      event.stopPropagation(); // Prevent the sidebar from closing when a link is clicked
      this.isOpen = true;
    }
  }
}
</script>






<style scoped>
.sidebar {
  height: 100vh;
  width: 80px; /* Width of the collapsed sidebar */
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #000000;
  overflow-x: hidden;
  transition: width 0.5s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 25px;
}

.sidebar:hover, .sidebar.active {
  width: 300px; /* Expanded width */
}

.logo img {
  height: 40px;
  margin: 10px 0;
}

.nav-link {
  display: flex;
  align-items: center;
  color: white;
  text-decoration: none;
  padding: 20px; /* Adjust padding for aesthetics */
  width: 100%;
  transition: background-color 0.3s, transform 0.3s;
  border-radius: 20px; /* Rounded corners for the background */
}

.nav-link:hover {
  background-color: #e1e1e1;
  color: black; /* Change text color on hover */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Shadow for depth */
  transform: translateX(10px); /* Slight shift to the right on hover */
}

.nav-link i {
  margin-right: 15px; /* Space between icon and label */
  font-size: 24px; /* Adjusted for realistic icon size */
  transition: font-size 0.3s ease; /* Smooth transition for font size */
}

.sidebar:hover .nav-link i, .sidebar.active .nav-link i {
  font-size: 28px; /* Larger font size when sidebar is expanded */
}

.nav-link span {
  display: none; /* Hide text when sidebar is collapsed */
  white-space: nowrap;
}

.sidebar:hover .nav-link span, .sidebar.active .nav-link span {
  display: inline; /* Show text when sidebar is expanded */
}
</style>
