import {createRouter, createWebHistory} from 'vue-router'
import Home  from './pages/HomePage.vue';
import GeneStructure from './pages/GeneInPage.vue';
import RunYass from './pages/YassPage.vue';
import GeneInput from './pages/GeneInPage.vue';
import GeneSequenceDisplay from './pages/GeneSeqPage.vue';
import About from './pages/HelpPage.vue';



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
    {   
        path: '/gene-structure', 
        component: GeneStructure 
    },
    {   
        path: '/gene-image', 
        component: GeneStructure 
    },
    {   
        path: '/run-yass', 
        component: RunYass 
    },
]

const router = createRouter({
    history:createWebHistory(),
    routes,
}
    
)
export default router;