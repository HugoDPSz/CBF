from flask import Blueprint, request, jsonify
from app.models.equipe import db, Equipe
from datetime import datetime

bp_equipe = Blueprint('equipes', __name__, url_prefix='/equipes')

@bp_equipe.route('/', methods=['GET'])
def listar_equipes():
    equipes = Equipe.query.all()
    return jsonify([{
        'nome' : e.nome,
        'sigla' : e.sigla,
        'cidade' : e.cidade,
        'estado' : e.estado,
        'data_fundacao' : e.data_fundacao.isoformat() if e.data_fundacao else None
    }for e in equipes])

@bp_equipe.route('/<int:id>', methods = ['GET'])
def buscar_equipe_por_id(id):
    e = Equipe.query.get_or_404(id)
    return jsonify({
        'nome' : e.nome,
        'sigla' : e.sigla,
        'cidade' : e.cidade,
        'estado' : e.estado,
        'data_fundacao' : e.data_fundacao.isoformat() if e.data_fundacao else None
    })

@bp_equipe.route('/', methods=['POST'])
def criar_equipe():
    data = request.json
    try:
        equipe  = Equipe(
            nome = data['nome'],
            sigla = data['sigla'],
            cidade = data['cidade'],
            estado = data['estado'],
            data_fundacao=datetime.strptime(data['data_fundacao'], '%Y-%m-%d').date()
        )
        db.session.add(equipe)
        db.session.commit()
        return jsonify({'id': equipe.id_equipe}), 201
    except Exception as e:
        return jsonify({'erro' : str(e)}), 400
    
@bp_equipe.route('/<int:id>', methods=['PUT'])
def atualizar_equipe(id):
    e = Equipe.query.get_or_404(id)
    data = request.json

    e.nome = data['nome']
    e.sigla = data['sigla']

    db.session.commit()
    return jsonify({
        'nome' : e.nome,
        'sigla' : e.sigla,
        'cidade' : e.cidade,
        'estado' : e.estado,
        'data_fundacao' : e.data_fundacao.isoformat() if e.data_fundacao else None
    })

@bp_equipe.route('/<int:id>', methods=['PUT'])
def deletar_equipe(id):
    equipe = Equipe.query.get_or_404(id)
    db.session.delete(equipe)
    db.session.commit()
    return jsonify({'mensagem' : 'equipe excluída'})