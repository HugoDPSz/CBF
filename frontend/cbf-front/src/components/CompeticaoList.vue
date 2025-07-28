<template>
  <v-container>
    <v-card class="pa-4 mb-6">
      <v-card-title class="headline">Competições</v-card-title>
      <v-data-table
        :headers="headers"
        :items="competicoes"
        class="elevation-1"
        item-key="id_competicao"
      >
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small class="mr-2" @click="editCompeticao(item)">mdi-pencil</v-icon>
          <v-icon small color="red" @click="deleteCompeticao(item.id_competicao)">mdi-delete</v-icon>
        </template>
      </v-data-table>
    </v-card>

    <v-card class="pa-4">
      <v-card-title class="headline">{{ editing ? 'Editar Competição' : 'Criar Competição' }}</v-card-title>
      <v-form @submit.prevent="submitForm">
        <v-text-field v-model="form.nome" label="Nome" required />
        <v-text-field v-model="form.organizador" label="Organizador" required />
        <v-text-field v-model="form.local" label="Local" required />
        <v-text-field v-model="form.data_inicio" label="Data de Início" type="date" required />
        <v-text-field v-model="form.data_fim" label="Data de Fim" type="date" required />

        <v-btn type="submit" color="primary" class="mt-4">
          {{ editing ? 'Salvar' : 'Criar' }}
        </v-btn>
        <v-btn v-if="editing" color="grey" class="mt-4 ml-2" @click="cancelEdit">Cancelar</v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      competicoes: [],
      headers: [
        { text: 'Nome', value: 'nome' },
        { text: 'Organizador', value: 'organizador' },
        { text: 'Local', value: 'local' },
        { text: 'Início', value: 'data_inicio' },
        { text: 'Fim', value: 'data_fim' },
        { text: 'Ações', value: 'actions', sortable: false }
      ],
      form: {
        id_competicao: null,
        nome: '',
        organizador: '',
        local: '',
        data_inicio: '',
        data_fim: ''
      },
      editing: false
    };
  },
  methods: {
    fetchCompeticoes() {
      fetch('http://127.0.0.1:5000/competicoes/')
        .then(res => res.json())
        .then(data => (this.competicoes = data))
        .catch(err => console.error(err));
    },
    submitForm() {
      const url = `http://127.0.0.1:5000/competicoes/${this.editing ? this.form.id_competicao : ''}`;
      fetch(url, {
        method: this.editing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.form)
      })
        .then(res => res.json())
        .then(() => {
          this.fetchCompeticoes();
          this.resetForm();
        })
        .catch(err => console.error(err));
    },
    deleteCompeticao(id) {
      if (confirm('Deseja realmente excluir esta competição?')) {
        fetch(`http://127.0.0.1:5000/competicoes/${id}`, {
          method: 'DELETE'
        })
          .then(() => this.fetchCompeticoes())
          .catch(err => console.error(err));
      }
    },
    editCompeticao(competicao) {
      this.form = { ...competicao, data_inicio: competicao.data_inicio.split('T')[0], data_fim: competicao.data_fim.split('T')[0] };
      this.editing = true;
    },
    cancelEdit() {
      this.resetForm();
    },
    resetForm() {
      this.form = {
        id_competicao: null,
        nome: '',
        organizador: '',
        local: '',
        data_inicio: '',
        data_fim: ''
      };
      this.editing = false;
    }
  },
  mounted() {
    this.fetchCompeticoes();
  }
};
</script>