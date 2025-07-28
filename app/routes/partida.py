from flask import Blueprint, request, jsonify
from app.models import db
from datetime import datetime
from sqlalchemy import text

bp_partida = Blueprint('partidas', __name__, url_prefix='/partidas')

@bp_partida.route('/', methods=['GET'])
def listar_partidas():
    query = text("SELECT * FROM vw_partidas_detalhadas")
    result = db.session.execute(query).fetchall()
    
    partidas = [{
        'id': row.id,
        'data_hora': row.data_hora.isoformat(),
        'estadio': row.estadio,
        'local': row.local,
        'placar_casa': row.placar_casa,
        'placar_visitante': row.placar_visitante,
        'equipe_casa': row.equipe_casa_nome,
        'equipe_visitante': row.equipe_visitante_nome,
        'competicao': row.competicao_nome
    } for row in result]
    
    return jsonify(partidas)

@bp_partida.route('/<int:id>', methods=['GET'])
def buscar_partida_por_id(id):
    query = text("SELECT * FROM partidas WHERE id = :id")
    result = db.session.execute(query, {"id": id}).first()

    if result is None:
        return jsonify({'erro': 'Partida não encontrada'}), 404
        
    return jsonify({
        'id': result.id,
        'data_hora': result.data_hora.isoformat(),
        'id_competicao': result.id_competicao,
        'estadio': result.estadio,
        'local': result.local,
        'equipe_casa_id': result.equipe_casa_id,
        'equipe_visitante_id': result.equipe_visitante_id,
        'placar_casa': result.placar_casa,
        'placar_visitante': result.placar_visitante
    })

@bp_partida.route('/', methods=['POST'])
def criar_partida():
    data = request.json
    try:
        query = text("""
            INSERT INTO partidas (data_hora, id_competicao, estadio, local, equipe_casa_id, equipe_visitante_id, placar_casa, placar_visitante)
            VALUES (:data_hora, :id_competicao, :estadio, :local, :equipe_casa_id, :equipe_visitante_id, :placar_casa, :placar_visitante)
            RETURNING id;
        """)
        
        result = db.session.execute(query, {
            "data_hora": datetime.fromisoformat(data['data_hora']),
            "id_competicao": data['id_competicao'],
            "estadio": data['estadio'],
            "local": data['local'],
            "equipe_casa_id": data['equipe_casa_id'],
            "equipe_visitante_id": data['equipe_visitante_id'],
            "placar_casa": data.get('placar_casa'),
            "placar_visitante": data.get('placar_visitante')
        }).scalar_one()
        
        db.session.commit()
        return jsonify({'id': result}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_partida.route('/<int:id>/placar', methods=['PUT'])
def atualizar_placar_partida(id):
    data = request.json
    try:
        query = text("""
            UPDATE partidas
            SET placar_casa = :placar_casa, placar_visitante = :placar_visitante
            WHERE id = :id
        """)
        
        result = db.session.execute(query, {
            "id": id,
            "placar_casa": data.get('placar_casa'),
            "placar_visitante": data.get('placar_visitante')
        })

        if result.rowcount == 0:
            return jsonify({'erro': 'Partida não encontrada'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Placar da partida atualizado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400