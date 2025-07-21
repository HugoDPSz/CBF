from app.models import db
from datetime import datetime

class ArbitragemPartida(db.Model):
    __tablename__ = 'arbitragem_partidas'
    
    id_arbitragem = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partidas.id'), nullable=False)
    id_arbitro = db.Column(db.Integer, db.ForeignKey('arbitros.id'), nullable=False)
    funcao = db.Column(db.String(50), nullable=False)  # e.g., 'arbitro_principal', 'assistente_1', 'assistente_2'

    partida = db.relationship('Partida', back_populates='arbitragem')
    arbitro = db.relationship('Arbitro', back_populates='arbitragems')

    def __repr__(self):
        return f'<ArbitragemPartida {self.id_arbitragem} - Partida {self.partida.id} - Arbitro {self.arbitro.nome}>'