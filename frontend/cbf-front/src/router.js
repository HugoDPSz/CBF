
import Jogador from '../src/components/JogadorList.vue';
import Equipe from '../src/components/EquipeList.vue';
import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';


Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HelloWorld
    },
    {
      path: '/jogadores',
      name: 'Jogador',
      component: Jogador
    },
    {
      path: '/equipes',
      name: 'Equipes',
      component: Equipe
    }
  ]
});

