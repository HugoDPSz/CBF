from flask import Blueprint, request, jsonify
from app.models import db
from datetime import datetime
from sqlalchemy import text

bp_arbitro = Blueprint('arbitros', __name__, url_prefix='/arbitros')

@bp_arbitro.route('/', methods=['GET'])
def listar_arbitros():
    query = text("SELECT * FROM arbitros")
    result = db.session.execute(query).fetchall()
    
    arbitros = [{
        'id_arbitro': row.id_arbitro,
        'nome': row.nome,
        'nacionalidade': row.nacionalidade,
        'categoria': row.categoria,
        'status': row.status,
        'data_nascimento': row.data_nascimento.isoformat() if row.data_nascimento else None,
        'experiencia': row.experiencia
    } for row in result]
    
    return jsonify(arbitros)

@bp_arbitro.route('/<int:id>', methods=['GET'])
def buscar_arbitro_por_id(id):
    query = text("SELECT * FROM arbitros WHERE id_arbitro = :id")
    result = db.session.execute(query, {"id": id}).first()
    
    if result is None:
        return jsonify({'erro': 'Árbitro não encontrado'}), 404
        
    return jsonify({
        'id_arbitro': result.id_arbitro,
        'nome': result.nome,
        'nacionalidade': result.nacionalidade,
        'categoria': result.categoria,
        'status': result.status,
        'data_nascimento': result.data_nascimento.isoformat() if result.data_nascimento else None,
        'experiencia': result.experiencia
    })

@bp_arbitro.route('/', methods=['POST'])
def criar_arbitro():
    data = request.json
    try:
        query = text("""
            INSERT INTO arbitros (nome, nacionalidade, categoria, status, data_nascimento, experiencia)
            VALUES (:nome, :nacionalidade, :categoria, :status, :data_nascimento, :experiencia)
        """)
        
        result = db.session.execute(query, {
            "nome": data['nome'],
            "nacionalidade": data['nacionalidade'],
            "categoria": data['categoria'],
            "status": data.get('status', 'Ativo'),
            "data_nascimento": datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date(),
            "experiencia": data['experiencia']
        })
        
        db.session.commit()
        return jsonify({'id': result.lastrowid}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_arbitro.route('/<int:id>', methods=['PUT'])
def atualizar_arbitro(id):
    data = request.json
    try:
        query = text("""
            UPDATE arbitros
            SET nome = :nome, nacionalidade = :nacionalidade, categoria = :categoria, 
                status = :status, experiencia = :experiencia, data_nascimento = :data_nascimento
            WHERE id_arbitro = :id
        """)
        
        result = db.session.execute(query, {
            "id": id,
            "nome": data['nome'],
            "nacionalidade": data['nacionalidade'],
            "categoria": data['categoria'],
            "status": data.get('status'),
            "experiencia": data.get('experiencia'),
            "data_nascimento": datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date() if 'data_nascimento' in data else None
        })

        if result.rowcount == 0:
            return jsonify({'erro': 'Árbitro não encontrado'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Árbitro atualizado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_arbitro.route('/<int:id>', methods=['DELETE'])
def deletar_arbitro(id):
    try:
        query = text("DELETE FROM arbitros WHERE id_arbitro = :id")
        result = db.session.execute(query, {"id": id})

        if result.rowcount == 0:
            return jsonify({'erro': 'Árbitro não encontrado'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Árbitro excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400