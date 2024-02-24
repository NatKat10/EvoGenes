import {createRouter, createWebHistory} from 'vue-router'
import Home  from './components/home.vue';
import About from './components/About.vue';


const routes = [
    {
        path:'/',
        name:'home',
        component: Home
    },
    {
        path:'/About',
        name:'About',
        component: About
    }
]

const router = createRouter({

    history:createWebHistory(),
    routes,
}
    
)
export default router;