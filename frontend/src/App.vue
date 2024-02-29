<template>
  <div id="app">
    <Navbar/>
    <router-view/>
  </div>
  <!-- <Navbar/> -->
</template>

<script>
// import { RouterView } from 'vue-router';
import Navbar from './components/appNavbar.vue';

export default {
  name: 'App',
  components: {
    Navbar,
    // RouterView
}
}
</script>

<style>

</style>
