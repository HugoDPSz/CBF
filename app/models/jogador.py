from app.models import db
from datetime import datetime
import enum

class PePreferido(enum.Enum):
    DIREITO = 'Direito'
    ESQUERDO = 'Esquerdo'
    AMBIDESTRO = 'Ambidestro'

class Jogador(db.Model):
    __tablename__ = 'jogadores'
    
    id_jogador = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    posicao = db.Column(db.String(50), nullable=False)
    altura = db.Column(db.Float, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nacionalidade = db.Column(db.String(50), nullable=False)
    pe_preferido = db.Column(db.Enum(PePreferido), nullable=False, default=PePreferido.DIREITO)
    
    participacoes = db.relationship('Escalacao', back_populates='jogador', cascade="all, delete-orphan")
    eventos = db.relationship('EventosPartida', back_populates='jogador') 
    def __repr__(self):
        return f'<Jogador {self.nome} - {self.posicao}>'