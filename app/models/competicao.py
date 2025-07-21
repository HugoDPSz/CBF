from app.models import db
from datetime import datetime

class Competicao(db.Model):
    __tablename__ = 'competicoes'
    
    id_competicao = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    local = db.Column(db.String(100), nullable=False)
    organizador = db.Column(db.String(100), nullable=False)  # Ex: CBF, FIFA, etc.

    def __repr__(self):
        return f'<Competicao {self.nome} - {self.local}>'