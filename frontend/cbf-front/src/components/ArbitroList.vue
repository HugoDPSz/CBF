<template>
  <v-container>
    <v-card class="pa-4 mb-6">
      <v-card-title class="headline">Árbitros</v-card-title>
      <v-data-table
        :headers="headers"
        :items="arbitros"
        class="elevation-1"
        item-key="id_arbitro"
      >
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small class="mr-2" @click="editArbitro(item)">mdi-pencil</v-icon>
          <v-icon small color="red" @click="deleteArbitro(item.id_arbitro)">mdi-delete</v-icon>
        </template>
      </v-data-table>
    </v-card>

    <v-card class="pa-4">
      <v-card-title class="headline">{{ editing ? 'Editar Árbitro' : 'Criar Árbitro' }}</v-card-title>
      <v-form @submit.prevent="submitForm">
        <v-text-field v-model="form.nome" label="Nome" required />
        <v-text-field v-model="form.nacionalidade" label="Nacionalidade" required />
        <v-text-field v-model="form.categoria" label="Categoria" required />
        <v-text-field v-model.number="form.experiencia" label="Experiência (anos)" type="number" required />
        <v-text-field v-model="form.data_nascimento" label="Data de Nascimento" type="date" required />

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
      arbitros: [],
      headers: [
        { text: 'Nome', value: 'nome' },
        { text: 'Nacionalidade', value: 'nacionalidade' },
        { text: 'Categoria', value: 'categoria' },
        { text: 'Experiência', value: 'experiencia' },
        { text: 'Nascimento', value: 'data_nascimento' },
        { text: 'Status', value: 'status' },
        { text: 'Ações', value: 'actions', sortable: false }
      ],
      form: {
        id_arbitro: null,
        nome: '',
        nacionalidade: '',
        categoria: '',
        status: 'Ativo',
        data_nascimento: '',
        experiencia: null
      },
      editing: false
    };
  },
  methods: {
    fetchArbitros() {
      fetch('http://127.0.0.1:5000/arbitros/')
        .then(res => res.json())
        .then(data => (this.arbitros = data))
        .catch(err => console.error(err));
    },
    submitForm() {
      const url = `http://127.0.0.1:5000/arbitros/${this.editing ? this.form.id_arbitro : ''}`;
      fetch(url, {
        method: this.editing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.form)
      })
        .then(res => res.json())
        .then(() => {
          this.fetchArbitros();
          this.resetForm();
        })
        .catch(err => console.error(err));
    },
    deleteArbitro(id) {
      if (confirm('Deseja realmente excluir este árbitro?')) {
        fetch(`http://127.0.0.1:5000/arbitros/${id}`, {
          method: 'DELETE'
        })
          .then(() => this.fetchArbitros())
          .catch(err => console.error(err));
      }
    },
    editArbitro(arbitro) {
      this.form = { ...arbitro, data_nascimento: arbitro.data_nascimento.split('T')[0] };
      this.editing = true;
    },
    cancelEdit() {
      this.resetForm();
    },
    resetForm() {
      this.form = {
        id_arbitro: null,
        nome: '',
        nacionalidade: '',
        categoria: '',
        status: 'Ativo',
        data_nascimento: '',
        experiencia: null
      };
      this.editing = false;
    }
  },
  mounted() {
    this.fetchArbitros();
  }
};
</script>