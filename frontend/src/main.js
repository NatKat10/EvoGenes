import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import router from './routers'; 


// createApp(App).mount('#app')
createApp(App).use(router).mount('#app');
