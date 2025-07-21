from app.models import db
from datetime import datetime

class Escalacao(db.Model):
    __tablename__ = 'escalacoes'
    
    id_escalacao = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partidas.id'), nullable=False)
    id_equipe = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=False)
    id_jogador = db.Column(db.Integer, db.ForeignKey('jogadores.id'), nullable=False)
    numero_camisa = db.Column(db.Integer, nullable=False)

    partida = db.relationship('Partida', back_populates='escalacao')
    jogador = db.relationship('Jogador', back_populates='participacoes')
    equipe = db.relationship('Equipe')

    def __repr__(self):
        return f'<Escalacao {self.id} - Partida {self.partida.id} - Equipe {self.equipe.nome}>'