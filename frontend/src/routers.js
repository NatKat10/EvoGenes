import {createRouter, createWebHistory} from 'vue-router'
import Home  from './components/home.vue';
import About from './components/About.vue';
import GeneInput from './components/GeneInput.vue';
import GeneSequenceDisplay from './components/GeneSequenceDisplay.vue';
import GeneStructure from './components/GeneStructure.vue';




const routes = [
    {
        path:'/',
        name:'home-page',
        component: Home
    },
    {
        path:'/about',
        name:'about',
        component: About
    },
    {
        path: '/gene-input',
        name: 'gene-input',
        component: GeneInput,
    },
    {
        path: '/gene-sequence/:geneId',
        name: 'gene-sequence',
        component: GeneSequenceDisplay,
        props: true,
    },
    { path: '/gene-structure', component: GeneStructure },
]

const router = createRouter({

    history:createWebHistory(),
    routes,
}
    
)
export default router;