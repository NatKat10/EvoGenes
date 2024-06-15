import { createApp } from 'vue'
import App from './App.vue'
import router from './routers'; 

import { BootstrapVue3, IconsPlugin } from 'bootstrap-vue-3';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';


import '@fortawesome/fontawesome-free/js/all.js';
import 'slick-carousel/slick/slick.css'; 
import 'slick-carousel/slick/slick-theme.css'; // Slick theme
import 'vue-slick-carousel/dist/vue-slick-carousel.css';
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';


import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';



// cuurent
const app = createApp(App);
app.use(BootstrapVue3);
app.use(IconsPlugin);
app.use(router);
app.mount('#app');




//original
// createApp(App).use(router).mount('#app');


// const app = createApp(App);
// app.use(BootstrapVue);
// app.use(IconsPlugin);
// app.use(router);
// app.mount('#app');
