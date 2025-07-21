from app.models import db
from datetime import datetime

class Contrato(db.Model):
    __tablename__ = 'contratos'
    
    id_contrato = db.Column(db.Integer, primary_key=True)
    id_jogador = db.Column(db.Integer, db.ForeignKey('jogadores.id_jogador'), nullable=False)
    id_equipe = db.Column(db.Integer, db.ForeignKey('equipes.id_equipe'), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Ativo')  # Ex: Ativo, Encerrado, Rescindido
    salario = db.Column(db.Float, nullable=False)

    jogador = db.relationship('Jogador', backref='contratos')
    equipe = db.relationship('Equipe', backref='contratos')

    def __repr__(self):
        return f'<Contrato {self.id_contrato} - Jogador: {self.jogador.nome}, Equipe: {self.equipe.nome}>'