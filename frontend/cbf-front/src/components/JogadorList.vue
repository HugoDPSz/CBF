<template>
  <v-container>
    <v-card class="pa-4 mb-6">
      <v-card-title class="headline">Jogadores</v-card-title>
      <v-data-table
        :headers="headers"
        :items="jogadores"
        class="elevation-1"
        item-key="id"
      >

      <template v-slot:[`item.actions`]="{ item }">
          
          <v-icon small class="mr-2" @click="checkContrato(item.id)">mdi-file-document</v-icon>
          <v-icon small class="mr-2" @click="editJogador(item)">mdi-pencil</v-icon>
          <v-icon small color="red" @click="deleteJogador(item.id)">mdi-delete</v-icon>
        </template>
      </v-data-table>
    </v-card>

    <v-card class="pa-4">
      <v-card-title class="headline">{{ editing ? 'Editar Jogador' : 'Criar Jogador' }}</v-card-title>
      <v-form @submit.prevent="submitForm">
        <v-text-field v-model="form.nome" label="Nome" required />
        <v-text-field v-model="form.posicao" label="Posição" required />
        <v-text-field v-model.number="form.altura" label="Altura" type="number" step="0.01" required />
        <v-text-field v-model.number="form.peso" label="Peso" type="number" step="0.1" required />
        <v-text-field v-model="form.data_nascimento" label="Data de Nascimento" type="date" required />
        <v-text-field v-model="form.nacionalidade" label="Nacionalidade" required />

        <v-btn type="submit" color="primary" class="mt-4">{{ editing ? 'Salvar' : 'Criar' }}</v-btn>
        <v-btn v-if="editing" color="grey" class="mt-4 ml-2" @click="cancelEdit">Cancelar</v-btn>
      </v-form>
    </v-card>
    <v-dialog v-model="dialog" max-width="600px">
    
    <v-card>
      <v-card-title> Contrato</v-card-title>

      <v-card-text>
        <v-form ref="form">
          <v-text-field v-model="contrato.salario" label="Salário" type="number"></v-text-field>
          <v-menu ref="startMenu" v-model="menuStart" :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
              <v-text-field v-model="contrato.data_inicio" label="Data de Início" readonly v-bind="attrs" v-on="on" />
            </template>
            <v-date-picker v-model="contrato.data_inicio" @input="menuStart = false"></v-date-picker>
          </v-menu>

          <v-menu ref="endMenu" v-model="menuEnd" :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
              <v-text-field v-model="contrato.data_fim" label="Data de Fim" readonly v-bind="attrs" v-on="on" />
            </template>
            <v-date-picker v-model="contrato.data_fim" @input="menuEnd = false"></v-date-picker>
          </v-menu>

          <v-select :items="equipes" v-model="contrato.id_equipe" label="Equipe" item-text="nome" item-value="id_equipe"></v-select>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false">Cancelar</v-btn>
        <v-btn color="green darken-1" text @click="submit">Salvar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  </v-container>

 
</template>


<script>
export default {
  data() {
    return {
      jogadores: [],
      equipes: [],
      contratos: [],
      headers: [
        { text: 'Nome', value: 'nome' },
        { text: 'Posição', value: 'posicao' },
        { text: 'Altura', value: 'altura' },
        { text: 'Peso', value: 'peso' },
        { text: 'Nascimento', value: 'data_nascimento' },
        { text: 'Nacionalidade', value: 'nacionalidade' },
        { text: 'Ações', value: 'actions', sortable: false }
      ],
      dialog: false,
      menuStart: false,
      menuEnd: false,
      contrato: {
        id_jogador: null,
        id_equipe: null,
        data_inicio: '',
        data_fim: '',
        status: 'Ativo',
        salario: null
      },
      form: {
        id: null,
        nome: '',
        posicao: '',
        altura: null,
        peso: null,
        data_nascimento: '',
        nacionalidade: ''
      },
      editing: false
    };
  },
  methods: {
    fetchJogadores() {
      fetch('http://127.0.0.1:5000/jogadores/')
        .then(res => res.json())
        .then(data => (this.jogadores = data))
        .catch(err => console.error(err));
    },
    fetchContratos() {
      fetch('http://127.0.0.1:5000/contratos/')
        .then(res => res.json())
        .then(data => (this.contratos = data))
        .catch(err => console.error(err));
    },
    fetchEquipes() {
      fetch('http://127.0.0.1:5000/equipes/')
        .then(res => res.json())
        .then(data => (this.equipes = data))
        .catch(err => console.error(err));
    },
    checkContrato(jogadorId) {
      const url = 'http://127.0.0.1:5000/contratos/jogador/'+ `${jogadorId}`;
      try {
        fetch(url)
          .then(res => res.json())
          .then(data => (this.contrato = data))
          .catch(err => console.error(err));
                
      } catch (error) {
        this.contrato = {
        id_jogador: jogadorId,
        id_equipe: null,
        data_inicio: '',
        data_fim: '',
        status: 'Ativo',
        salario: null
      };
      }
      
      
      this.dialog = true;
    },
    submit() {
      fetch('http://127.0.0.1:5000/contratos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.contrato)
      })
        .then(res => res.json())
        .then(() => {
          this.dialog = false;
          
        })
        .catch(err => console.error(err));
    },
    submitForm() {
      const url = 'http://127.0.0.1:5000/jogadores/' + (this.editing ? `${this.form.id}` : '');
      fetch(url, {
        method: this.editing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.form)
      })
        .then(res => res.json())
        .then(() => {
          this.fetchJogadores();
          this.resetForm();
        })
        .catch(err => console.error(err));
    },
    deleteJogador(id) {
      if (confirm('Deseja realmente excluir este jogador?')) {
        fetch(`http://127.0.0.1:5000/jogadores/${id}`, {
          method: 'DELETE'
        })
          .then(() => this.fetchJogadores())
          .catch(err => console.error(err));
      }
    },
    editJogador(jogador) {
      this.form = { ...jogador };
      this.editing = true;
    },
    cancelEdit() {
      this.resetForm();
    },
    resetForm() {
      this.form = {
        id: null,
        nome: '',
        posicao: '',
        altura: null,
        peso: null,
        data_nascimento: '',
        nacionalidade: ''
      };
      this.editing = false;
    }
  },
  mounted() {
    this.fetchJogadores();
    this.fetchEquipes();
  }
};

</script>
