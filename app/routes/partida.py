from flask import Blueprint, request, jsonify
from app.models.partida import db, Partida
from datetime import datetime

bp_partida = Blueprint('partidas', __name__, url_prefix='/partidas')

@bp_partida.route('/', methods=['GET'])
def listar_partidas():
    partidas = Partida.query.all()
    return jsonify([{
        'id': p.id,
        'data_hora': p.data_hora.isoformat(),
        'id_competicao': p.id_competicao,
        'estadio': p.estadio,
        'local': p.local,
        'equipe_casa_id': p.equipe_casa_id,
        'equipe_visitante_id': p.equipe_visitante_id,
        'placar_casa': p.placar_casa,
        'placar_visitante': p.placar_visitante
    } for p in partidas])

@bp_partida.route('/<int:id>', methods=['GET'])
def buscar_partida_por_id(id):
    p = Partida.query.get_or_404(id)
    return jsonify({
        'id': p.id,
        'data_hora': p.data_hora.isoformat(),
        'id_competicao': p.id_competicao,
        'estadio': p.estadio,
        'local': p.local,
        'equipe_casa_id': p.equipe_casa_id,
        'equipe_visitante_id': p.equipe_visitante_id,
        'placar_casa': p.placar_casa,
        'placar_visitante': p.placar_visitante
    })

@bp_partida.route('/', methods=['POST'])
def criar_partida():
    data = request.json
    try:
        partida = Partida(
            data_hora=datetime.fromisoformat(data['data_hora']),
            id_competicao=data['id_competicao'],
            estadio=data['estadio'],
            local=data['local'],
            equipe_casa_id=data['equipe_casa_id'],
            equipe_visitante_id=data['equipe_visitante_id'],
            placar_casa=data.get('placar_casa'),
            placar_visitante=data.get('placar_visitante')
        )
        db.session.add(partida)
        db.session.commit()
        return jsonify({'id': partida.id}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@bp_partida.route('/<int:id>', methods=['PUT'])
def atualizar_partida(id):
    p = Partida.query.get_or_404(id)
    data = request.json
    try:
        p.data_hora = datetime.fromisoformat(data.get('data_hora', p.data_hora.isoformat()))
        p.estadio = data.get('estadio', p.estadio)
        p.local = data.get('local', p.local)
        p.placar_casa = data.get('placar_casa', p.placar_casa)
        p.placar_visitante = data.get('placar_visitante', p.placar_visitante)
        db.session.commit()
        return jsonify({'id': p.id, 'mensagem': 'Partida atualizada com sucesso!'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400