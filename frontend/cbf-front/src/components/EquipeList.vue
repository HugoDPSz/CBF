<template>
  <v-container>
    <v-card class="pa-4 mb-6">
      <v-card-title class="headline">Equipes</v-card-title>
      <v-data-table
        :headers="headers"
        :items="equipes"
        class="elevation-1"
        item-key="id_equipe"
      >
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small class="mr-2" @click="editEquipe(item)">mdi-pencil</v-icon>
          <v-icon small color="red" @click="deleteEquipe(item.id_equipe)">mdi-delete</v-icon>
        </template>
      </v-data-table>
    </v-card>

    <v-card class="pa-4">
      <v-card-title class="headline">{{ editing ? 'Editar Equipe' : 'Criar Equipe' }}</v-card-title>
      <v-form @submit.prevent="submitForm">
        <v-text-field v-model="form.nome" label="Nome" required />
        <v-text-field v-model="form.sigla" label="Sigla" required />
        <v-text-field v-model="form.cidade" label="Cidade" required />
        <v-text-field v-model="form.estado" label="Estado" required />
        <v-text-field v-model="form.data_fundacao" label="Data de Fundação" type="date" required />

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
      equipes: [],
      headers: [
        { text: 'Nome', value: 'nome' },
        { text: 'Sigla', value: 'sigla' },
        { text: 'Cidade', value: 'cidade' },
        { text: 'Estado', value: 'estado' },
        { text: 'Fundação', value: 'data_fundacao' },
        { text: 'Ações', value: 'actions', sortable: false }
      ],
      form: {
        id_equipe: null,
        nome: '',
        sigla: '',
        cidade: '',
        estado: '',
        data_fundacao: ''
      },
      editing: false
    };
  },
  methods: {
    fetchEquipes() {
      fetch('http://127.0.0.1:5000/equipes/')
        .then(res => res.json())
        .then(data => (this.equipes = data))
        .catch(err => console.error(err));
    },
    submitForm() {
      const url = `http://127.0.0.1:5000/equipes/${this.editing ? this.form.id_equipe : ''}`;
      fetch(url, {
        method: this.editing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.form)
      })
        .then(res => res.json())
        .then(() => {
          this.fetchEquipes();
          this.resetForm();
        })
        .catch(err => console.error(err));
    },
    deleteEquipe(id) {
      if (confirm('Deseja realmente excluir esta equipe?')) {
        fetch(`http://127.0.0.1:5000/equipes/${id}`, {
          method: 'DELETE'
        })
          .then(() => this.fetchEquipes())
          .catch(err => console.error(err));
      }
    },
    editEquipe(equipe) {
      this.form = { ...equipe, id_equipe: equipe.id_equipe };
      this.editing = true;
    },
    cancelEdit() {
      this.resetForm();
    },
    resetForm() {
      this.form = {
        id_equipe: null,
        nome: '',
        sigla: '',
        cidade: '',
        estado: '',
        data_fundacao: ''
      };
      this.editing = false;
    }
  },
  mounted() {
    this.fetchEquipes();
  }
};
</script>
