import { createApp } from 'vue'
import App from './App.vue'
import router from './routers'; 


import 'bootstrap/dist/css/bootstrap.min.css'
import BootstrapVue3 from 'bootstrap-vue-3';

import '@fortawesome/fontawesome-free/js/all.js';
import 'slick-carousel/slick/slick.css'; 
import 'slick-carousel/slick/slick-theme.css'; // Slick theme
import 'vue-slick-carousel/dist/vue-slick-carousel.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';


// import {
//     CarouselPlugin
// } from "bootstrap-vue";
// [
//     CarouselPlugin
// ].forEach((x) => Vue.use(x));

const app = createApp(App);

app.use(BootstrapVue3);
app.use(router);

app.mount('#app');


//original
// createApp(App).use(router).mount('#app');



