<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">EVO-GENES</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link to="/" class="nav-link" href="#">Home</router-link>
        </li>

        <li class="nav-item">
          <router-link to="/gene-input" class="nav-link" href="#">Gene Input</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/run-yass" class="nav-link" href="#">Run Yass</router-link>
        </li>

        <li class="nav-item">
          <router-link to="/gene-sequence/:geneId" class="nav-link" href="#">Gene Sequence Display</router-link>
        </li>

        <li class="nav-item">
          <router-link to="/gene-structure" class="nav-link">Gene Structure</router-link>
        </li>

        <li class="nav-item">
          <router-link to="/about" class="nav-link" href="#">About</router-link>
        </li>
        

      </ul>

    </div>
  </div>
</nav>
</template>

<script>
// import { RouterLink } from 'vue-router';

// import { createRouter, createWebHistory } from 'vue-router';
export default {
    // components: { RouterLink }
}
</script>

<style>

</style>