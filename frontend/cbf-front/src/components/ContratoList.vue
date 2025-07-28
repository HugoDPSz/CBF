<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="headline">Contratos Ativos</v-card-title>
      <v-data-table
        :headers="headers"
        :items="contratos"
        class="elevation-1"
        item-key="id_contrato"
      >
        <template v-slot:[`item.actions`]="{ item }">
          <v-btn small color="error" @click="rescindirContrato(item.id_contrato)">Rescindir</v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      contratos: [],
      headers: [
        { text: 'Jogador', value: 'nome_jogador' },
        { text: 'Equipe', value: 'nome_equipe' },
        { text: 'Salário', value: 'salario' },
        { text: 'Início', value: 'data_inicio' },
        { text: 'Fim', value: 'data_fim' },
        { text: 'Status', value: 'status' },
        { text: 'Ações', value: 'actions', sortable: false }
      ],
    };
  },
  methods: {
    fetchContratos() {
      fetch('http://127.0.0.1:5000/contratos/')
        .then(res => res.json())
        .then(data => (this.contratos = data.filter(c => c.status === 'Ativo')))
        .catch(err => console.error(err));
    },
    rescindirContrato(id) {
      if (confirm('Deseja realmente rescindir este contrato?')) {
        fetch(`http://127.0.0.1:5000/contratos/${id}/rescindir`, {
          method: 'PUT'
        })
          .then(res => {
            if (!res.ok) throw new Error('Falha ao rescindir contrato');
            return res.json();
          })
          .then(() => {
            alert('Contrato rescindido com sucesso!');
            this.fetchContratos();
          })
          .catch(err => {
            console.error(err)
            alert('Erro ao rescindir o contrato.');
          });
      }
    }
  },
  mounted() {
    this.fetchContratos();
  }
};
</script>