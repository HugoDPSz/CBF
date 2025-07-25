from flask import Blueprint, request, jsonify
from app.models.contrato import db, Contrato
from app.models.jogador import Jogador
from datetime import datetime

bp_contrato = Blueprint('contratos', __name__, url_prefix='/contratos')

@bp_contrato.route('/', methods=['GET'])
def listar_contratos():
    contratos = Contrato.query.all()
    return jsonify([{
        'id': c.id_contrato,
        'data_inicio': c.data_inicio.isoformat() if c.data_inicio else None,
        'data_fim': c.data_fim.isoformat() if c.data_fim else None,
        'salario': c.salario,
        'id_jogador': c.id_jogador,
        'id_equipe': c.id_equipe
    } for c in contratos])

@bp_contrato.route('/<int:id>', methods=['GET'])
def buscar_contrato_por_id_jogador(id):
    
    c = Contrato.query.filter_by(id_jogador=id).first_or_404()
    return jsonify({
        'id': c.id_contrato,
        'data_inicio': c.data_inicio.isoformat() if c.data_inicio else None,
        'data_fim': c.data_fim.isoformat() if c.data_fim else None,
        'salario': c.salario,
        'id_jogador': c.id_jogador,
        'id_equipe': c.id_equipe
    })

@bp_contrato.route('/', methods=['POST'])
def criar_contrato():
    data = request.json
    try:
        contrato = Contrato(
            data_inicio=datetime.strptime(data['data_inicio'], '%Y-%m-%d').date(),
            data_fim=datetime.strptime(data['data_fim'], '%Y-%m-%d').date(),
            salario=data['salario'],
            id_jogador=data['id_jogador'],
            id_equipe=data['id_equipe']
        )
        db.session.add(contrato)
        db.session.commit()
        return jsonify({'id': contrato.id_contrato}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@bp_contrato.route('/<int:id>', methods=['PUT'])
def atualizar_contrato(id):
    c = Contrato.query.get_or_404(id)
    data = request.json
    try:
        c.data_inicio = datetime.strptime(data['data_inicio'], '%Y-%m-%d').date()
        c.data_fim = datetime.strptime(data['data_fim'], '%Y-%m-%d').date()
        c.salario = data['salario']
        c.id_jogador = data['id_jogador']
        c.id_equipe = data['id_equipe']
        db.session.commit()
        return jsonify({
            'id': c.id_contrato,
            'data_inicio': c.data_inicio.isoformat(),
            'data_fim': c.data_fim.isoformat(),
            'salario': c.salario,
            'id_jogador': c.id_jogador,
            'id_equipe': c.id_equipe
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@bp_contrato.route('/<int:id>', methods=['DELETE'])
def deletar_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    db.session.delete(contrato)
    db.session.commit()
    return jsonify({'mensagem': 'Contrato excluído com sucesso'})
