from app.models import db
from datetime import datetime

class Arbitro(db.Model):
    __tablename__ = 'arbitros'
    
    id_arbitro = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    nacionalidade = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # Ex: FIFA, CBF, etc.
    status = db.Column(db.String(20), nullable=False, default='Ativo')  # Ex: Ativo, Inativo
    data_nascimento = db.Column(db.Date, nullable=False)
    experiencia = db.Column(db.Integer, nullable=False)  # Anos de experiência

    def __repr__(self):
        return f'<Arbitro {self.nome} - Nacionalidade: {self.nacionalidade}>'