from flask import Blueprint, request, jsonify
from app.models.competicao import Competicao, db
from datetime import datetime

bp_competicao = Blueprint('competicoes', __name__, url_prefix='/competicoes')

@bp_competicao.route('/', methods=['GET'])
def listar_competicoes():
    competicoes = Competicao.query.all()
    return jsonify([{
        'nome' : c.nome,
        'data_inicio' : c.data_inicio.isoformat() if c.data_inicio else None,
        'data_fim' : c.data_fim.isoformat() if c.data_fim else None,
        'local' : c.local,
        'organizador' : c.organizador
    }for c in competicoes])

@bp_competicao.route('/<int:id>', methods=['GET'])
def buscar_competicao_por_id(id):
    c = Competicao.query.get_or_404(id)
    return jsonify({
        'nome' : c.nome,
        'data_inicio' : c.data_inicio.isoformat() if c.data_inicio else None,
        'data_fim' : c.data_fim.isoformat() if c.data_fim else None,
        'local' : c.local,
        'organizador' : c.organizador
    })

@bp_competicao.route('/', methods=['POST'])
def criar_competicao():
    data = request.json
    try:
        competicao = Competicao(
            nome = data['nome'],
            data_inicio = datetime.strptime(data['data_inicio'], '%Y-$m-%d').date(),
            data_fim = datetime.strptime(data['data_fim'], '%Y-%m-%d').date(),
            local = data['local'],
            organizador = data['organizador']
        )
        db.session.add(competicao)
        db.session.commit()
        return jsonify({'id': competicao.id_competicao}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
    
@bp_competicao.route('/<int:id>', methods=['PUT'])
def atualizar_competicao(id):
    c = Competicao.query.get_or_404(id)
    data = request.json

    c.data_inicio = datetime.strptime(data['data_inicio'], '%Y-$m-%d').date()
    c.data_fim = datetime.strptime(data['data_fim'], '%Y-%m-%d').date()
    c.local = data['local']
    c.organizador = data['local']

    db.session.commit()
    return jsonify({
        'nome' : c.nome,
        'data_inicio' : c.data_inicio.isoformat() if c.data_inicio else None,
        'data_fim' : c.data_fim.isoformat() if c.data_fim else None,
        'local' : c.local,
        'organizador' : c.organizador
    })

@bp_competicao.route('/<int:id>', methods=['DELETE'])
def deletar_competicao():
    competicao = Competicao.query.get_or_404(id)
    db.session.delete(competicao)
    db.session.commit()
    return jsonify({'mensagem' : 'Competição excluída'})