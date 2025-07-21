from app.models import db
from datetime import datetime

class Equipe(db.Model):
    __tablename__ = 'equipes'
    
    id_equipe = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sigla = db.Column(db.String(10), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    data_fundacao = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Equipe {self.nome} - {self.cidade}, {self.estado}>'