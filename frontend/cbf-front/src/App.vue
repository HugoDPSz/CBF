<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title style='color: yellow;'>CBF</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-for="page in pages" :key="page.name" text :to="page.path">
        {{ page.name }}
      </v-btn>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      pages: [
        { name: 'Home', path: '/' },
        { name: 'Jogadores', path: '/jogadores' },
        { name: 'Equipes', path: '/equipes' },
        { name: 'Contratos', path: '/contratos' },
        { name: 'Partidas', path: '/partidas' },
        { name: 'Competições', path: '/competicoes' },
        { name: 'Árbitros', path: '/arbitros' },
      ]
    };
  }
};
</script>