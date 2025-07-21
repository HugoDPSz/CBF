from app.models import db
from datetime import datetime

class EventosPartida(db.Model):
    __tablename__ = 'eventos_partida'
    
    id_evento = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partidas.id'), nullable=False)
    id_jogador = db.Column(db.Integer, db.ForeignKey('jogadores.id'), nullable=True)
    tipo_evento = db.Column(db.String(50), nullable=False)  # e.g., 'gol', 'cartao_amarelo', 'substituicao'
    minuto = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(255), nullable=True)  # Descrição opcional do evento

    partida = db.relationship('Partida', back_populates='eventos')
    jogador = db.relationship('Jogador', back_populates='eventos')

    def __repr__(self):
        return f'<Evento {self.tipo_evento} - Partida {self.partida.id} - Jogador {self.jogador.nome if self.jogador else "N/A"}>'