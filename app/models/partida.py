from app.models import db
from datetime import datetime

class Partida(db.Model):
    __tablename__ = 'partidas'
    
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_competicao = db.Column(db.Integer, db.ForeignKey('competicao.id'), nullable=False)
    estadio = db.Column(db.String(100), nullable=False)
    local = db.Column(db.String(100), nullable=False)
    equipe_casa_id = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=False)
    equipe_visitante_id = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=False)
    placar_casa = db.Column(db.Integer, nullable=True)
    placar_visitante = db.Column(db.Integer, nullable=True)

    equipe_casa = db.relationship('Equipe', foreign_keys=[equipe_casa_id], back_populates='partidas_em_casa')
    equipe_visitante = db.relationship('Equipe', foreign_keys=[equipe_visitante_id], back_populates='partidas_como_visitante')

    escalacao = db.relationship('Escalacao', back_populates='partida', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Partida {self.id} - {self.equipe_casa.nome} vs {self.equipe_visitante.nome}>'