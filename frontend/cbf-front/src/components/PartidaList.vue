<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="headline">Partidas</v-card-title>
      <v-data-table
        :headers="headers"
        :items="partidas"
        class="elevation-1"
        item-key="id"
      >
        <template v-slot:[`item.placar`]="{ item }">
          {{ item.placar_casa }} x {{ item.placar_visitante }}
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small class="mr-2">mdi-account-multiple</v-icon>
          <v-icon small>mdi-soccer</v-icon>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      partidas: [],
      headers: [
        { text: 'Competição', value: 'competicao' },
        { text: 'Equipe da Casa', value: 'equipe_casa' },
        { text: 'Equipe Visitante', value: 'equipe_visitante' },
        { text: 'Placar', value: 'placar', sortable: false },
        { text: 'Estádio', value: 'estadio' },
        { text: 'Data/Hora', value: 'data_hora' },
        { text: 'Ações', value: 'actions', sortable: false },
      ],
    };
  },
  methods: {
    fetchPartidas() {
      fetch('http://127.0.0.1:5000/partidas/')
        .then(res => res.json())
        .then(data => (this.partidas = data))
        .catch(err => console.error(err));
    },
  },
  mounted() {
    this.fetchPartidas();
  }
};
</script>