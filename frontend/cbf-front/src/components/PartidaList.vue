<template>
  <v-container>
    <v-card class="pa-4 mb-6">
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
          <v-icon small class="mr-2" @click="editPartida(item)">mdi-pencil</v-icon>
          <v-icon small class="mr-2" @click="openArbitragemDialog(item)">mdi-whistle</v-icon>
          <v-icon small color="red" @click="deletePartida(item.id)">mdi-delete</v-icon>
        </template>
      </v-data-table>
    </v-card>

    <v-card class="pa-4">
      <v-card-title class="headline">{{ editing ? 'Editar Partida' : 'Criar Partida' }}</v-card-title>
      <v-form @submit.prevent="submitForm">
        <v-select
          :items="competicoes"
          v-model="form.id_competicao"
          label="Competição"
          item-text="nome"
          item-value="id_competicao"
          required
        />

        <v-select
          :items="equipes"
          v-model="form.equipe_casa_id"
          label="Equipe da Casa"
          item-text="nome"
          item-value="id_equipe"
          :rules="[validateEquipeCasa]"
          required
        />

        <v-select
          :items="equipes"
          v-model="form.equipe_visitante_id"
          label="Equipe Visitante"
          item-text="nome"
          item-value="id_equipe"
          :rules="[validateEquipeVisitante]"
          required
        />

        <v-text-field v-model.number="form.placar_casa" label="Placar Casa" type="number" />
        <v-text-field v-model.number="form.placar_visitante" label="Placar Visitante" type="number" />
        <v-text-field v-model="form.estadio" label="Estádio" required />
        <v-text-field v-model="form.data_hora" label="Data/Hora" type="datetime-local" required />

        <v-btn type="submit" color="primary" class="mt-4">{{ editing ? 'Salvar' : 'Criar' }}</v-btn>
        <v-btn v-if="editing" color="grey" class="mt-4 ml-2" @click="cancelEdit">Cancelar</v-btn>
      </v-form>
    </v-card>

    <v-dialog v-model="arbitragemDialog" max-width="800px">
      <v-card>
        <v-card-title class="headline">
          Arbitragem para a Partida: {{ selectedPartida ? `${selectedPartida.equipe_casa} x ${selectedPartida.equipe_visitante}` : '' }}
        </v-card-title>

        <v-card-text>
          <v-list dense>
            <v-subheader>Árbitros Alocados</v-subheader>
            <v-list-item v-for="arbitro in arbitragemPartida" :key="arbitro.id_arbitragem">
              <v-list-item-content>
                <v-list-item-title>{{ arbitro.arbitro }}</v-list-item-title>
                <v-list-item-subtitle>{{ arbitro.funcao }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn icon @click="removerArbitro(arbitro.id_arbitragem)">
                  <v-icon color="red">mdi-delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
            <v-list-item v-if="arbitragemPartida.length === 0">
              <v-list-item-content>
                <v-list-item-title>Nenhum árbitro alocado para esta partida.</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-divider class="my-4"></v-divider>

          <v-form @submit.prevent="adicionarArbitro">
            <v-select
              :items="arbitros"
              v-model="novoArbitro.id_arbitro"
              label="Selecionar Árbitro"
              item-text="nome"
              item-value="id_arbitro"
              required
            ></v-select>
            <v-text-field
              v-model="novoArbitro.funcao"
              label="Função"
              required
            ></v-text-field>
            <v-btn type="submit" color="primary" class="mt-2">Adicionar Árbitro</v-btn>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="arbitragemDialog = false">Fechar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      partidas: [],
      arbitros: [],
      equipes: [],
      competicoes: [],
      headers: [
        { text: 'Competição', value: 'competicao' },
        { text: 'Equipe da Casa', value: 'equipe_casa' },
        { text: 'Equipe Visitante', value: 'equipe_visitante' },
        { text: 'Placar', value: 'placar', sortable: false },
        { text: 'Estádio', value: 'estadio' },
        { text: 'Data/Hora', value: 'data_hora' },
        { text: 'Ações', value: 'actions', sortable: false },
      ],
      form: {
        id: null,
        id_competicao: null,
        equipe_casa_id: null,
        equipe_visitante_id: null,
        placar_casa: null,
        placar_visitante: null,
        estadio: '',
        data_hora: ''
      },
      editing: false,
      // New data properties for arbitration dialog
      arbitragemDialog: false,
      selectedPartida: null,
      arbitragemPartida: [], // To store referees for the selected partida
      novoArbitro: {
        id_arbitro: null,
        funcao: ''
      }
    };
  },
  methods: {
    fetchArbitros() {
      fetch('http://127.0.0.1:5000/arbitros/')
        .then(res => res.json())
        .then(data => (this.arbitros = data))
        .catch(err => console.error(err));
    },
    fetchCompeticoes() {
      fetch('http://127.0.0.1:5000/competicoes/')
        .then(res => res.json())
        .then(data => (this.competicoes = data))
        .catch(err => console.error(err));
    },
    fetchEquipes() {
      fetch('http://127.0.0.1:5000/equipes/')
        .then(res => res.json())
        .then(data => (this.equipes = data))
        .catch(err => console.error(err));
    },
    fetchPartidas() {
      fetch('http://127.0.0.1:5000/partidas/')
        .then(res => res.json())
        .then(data => (this.partidas = data))
        .catch(err => console.error(err));
    },
    submitForm() {
      // Validação simples para evitar mesmo time
      if (this.form.equipe_casa_id === this.form.equipe_visitante_id) {
        alert('A equipe da casa não pode ser igual à equipe visitante.');
        return;
      }

      // Cria o payload com os nomes corretos das propriedades
      const payload = {
        data_hora: this.form.data_hora,
        id_competicao: this.form.id_competicao,
        estadio: this.form.estadio,
        local: this.form.estadio, // ajuste se local for outro campo no seu form
        equipe_casa_id: this.form.equipe_casa_id,
        equipe_visitante_id: this.form.equipe_visitante_id,
        placar_casa: this.form.placar_casa,
        placar_visitante: this.form.placar_visitante,
      };

      const url = 'http://127.0.0.1:5000/partidas/' + (this.editing ? `${this.form.id}` : '');

      fetch(url, {
        method: this.editing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(res => {
          if (!res.ok) throw new Error(`Erro: ${res.status}`);
          return res.json();
        })
        .then(() => {
          this.fetchPartidas();
          this.resetForm();
        })
        .catch(err => {
          console.error(err);
          alert('Erro ao salvar partida: ' + err.message);
        });
    },
    editPartida(partida) {
      const url = 'http://127.0.0.1:5000/partidas/' + `${partida.id}`;
      console.log(partida);
      try {
        fetch(url)
          .then(res => res.json())
          .then(data => (this.form = data))
          .catch(err => console.error(err));
                
      } catch (error){
          console.log(error);
          this.form = {
          id: null, 
          id_competicao: null,
          equipe_casa_id: null,
          equipe_visitante_id: null,
          placar_casa: null,
          placar_visitante: null,
          estadio: '',
          data_hora: ''
        };
      
      }
      
      this.editing = true;
    },
    deletePartida(id) {
      if (confirm('Deseja realmente excluir esta partida?')) {
        fetch(`http://127.0.0.1:5000/partidas/${id}`, {
          method: 'DELETE'
        })
          .then(() => this.fetchPartidas())
          .catch(err => console.error(err));
      }
    },
    cancelEdit() {
      this.resetForm();
    },
    resetForm() {
      this.form = {
        id: null,
        id_competicao: null,
        equipe_casa_id: null,
        equipe_visitante_id: null,
        placar_casa: null,
        placar_visitante: null,
        estadio: '',
        data_hora: ''
      };
      this.editing = false;
    },
    validateEquipeCasa(value) {
      return value !== this.form.equipe_visitante_id || 'A equipe da casa não pode ser igual à visitante.';
    },
    validateEquipeVisitante(value) {
      return value !== this.form.equipe_casa_id || 'A equipe visitante não pode ser igual à da casa.';
    },
    openArbitragemDialog(partida) {
      this.selectedPartida = partida;
      this.fetchArbitragemPorPartida(partida.id);
      this.arbitragemDialog = true;
    },
    fetchArbitragemPorPartida(id_partida) {
      fetch(`http://127.0.0.1:5000/arbitragem/partida/${id_partida}`)
        .then(res => res.json())
        .then(data => {
          this.arbitragemPartida = data;
        })
        .catch(err => console.error(err));
    },
    adicionarArbitro() {
      if (!this.novoArbitro.id_arbitro || !this.novoArbitro.funcao) {
        alert('Por favor, selecione um árbitro e informe a função.');
        return;
      }

      const payload = {
        id_partida: this.selectedPartida.id,
        id_arbitro: this.novoArbitro.id_arbitro,
        funcao: this.novoArbitro.funcao
      };

      fetch('http://127.0.0.1:5000/arbitragem/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(res => {
          if (!res.ok) throw new Error(`Erro: ${res.status}`);
          return res.json();
        })
        .then(() => {
          this.fetchArbitragemPorPartida(this.selectedPartida.id); // Refresh the list
          this.novoArbitro = { id_arbitro: null, funcao: '' }; // Reset form
        })
        .catch(err => {
          console.error(err);
          alert('Erro ao adicionar árbitro: ' + err.message);
        });
    },
    removerArbitro(id_arbitragem) {
      if (confirm('Deseja realmente remover este árbitro desta partida?')) {
        fetch(`http://127.0.0.1:5000/arbitragem/${id_arbitragem}`, {
          method: 'DELETE'
        })
          .then(() => {
            this.fetchArbitragemPorPartida(this.selectedPartida.id); // Refresh the list
          })
          .catch(err => console.error(err));
      }
    }
  },
  mounted() {
    this.fetchPartidas();
    this.fetchCompeticoes();
    this.fetchEquipes();
    this.fetchArbitros();
  }
};
</script>