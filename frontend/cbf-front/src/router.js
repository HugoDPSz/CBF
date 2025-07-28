import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import Jogador from '../src/components/JogadorList.vue';
import Equipe from '../src/components/EquipeList.vue';
import Contrato from '../src/components/ContratoList.vue';
import Partida from '../src/components/PartidaList.vue';
import Competicao from '../src/components/CompeticaoList.vue';
import Arbitro from '../src/components/ArbitroList.vue';


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
    },
    {
      path: '/contratos',
      name: 'Contratos',
      component: Contrato
    },
    {
      path: '/partidas',
      name: 'Partidas',
      component: Partida
    },
    {
      path: '/competicoes',
      name: 'Competições',
      component: Competicao
    },
    {
      path: '/arbitros',
      name: 'Árbitros',
      component: Arbitro
    }
  ]
});