from flask import Blueprint, request, jsonify
from app.models import db
from datetime import datetime
from sqlalchemy import text

bp_equipe = Blueprint('equipes', __name__, url_prefix='/equipes')

@bp_equipe.route('/', methods=['GET'])
def listar_equipes():
    query = text("SELECT * FROM equipes")
    result = db.session.execute(query).fetchall()
    
    equipes = [{
        'id_equipe': row.id_equipe,
        'nome': row.nome,
        'sigla': row.sigla,
        'cidade': row.cidade,
        'estado': row.estado,
        'data_fundacao': row.data_fundacao.isoformat() if row.data_fundacao else None
    } for row in result]
    
    return jsonify(equipes)

@bp_equipe.route('/<int:id>', methods=['GET'])
def buscar_equipe_por_id(id):
    query = text("SELECT * FROM equipes WHERE id_equipe = :id")
    result = db.session.execute(query, {"id": id}).first()
    
    if result is None:
        return jsonify({'erro': 'Equipe não encontrada'}), 404
        
    return jsonify({
        'id_equipe': result.id_equipe,
        'nome': result.nome,
        'sigla': result.sigla,
        'cidade': result.cidade,
        'estado': result.estado,
        'data_fundacao': result.data_fundacao.isoformat() if result.data_fundacao else None
    })

@bp_equipe.route('/', methods=['POST'])
def criar_equipe():
    data = request.json
    try:
        query = text("""
            INSERT INTO equipes (nome, sigla, cidade, estado, data_fundacao)
            VALUES (:nome, :sigla, :cidade, :estado, :data_fundacao)
        """)
        
        result = db.session.execute(query, {
            "nome": data['nome'],
            "sigla": data['sigla'],
            "cidade": data['cidade'],
            "estado": data['estado'],
            "data_fundacao": datetime.strptime(data['data_fundacao'], '%Y-%m-%d').date()
        })
        
        db.session.commit()
        return jsonify({'id': result.lastrowid}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400
    
@bp_equipe.route('/<int:id>', methods=['PUT'])
def atualizar_equipe(id):
    data = request.json
    try:
        query = text("""
            UPDATE equipes
            SET nome = :nome, sigla = :sigla
            WHERE id_equipe = :id
        """)
        
        result = db.session.execute(query, {
            "id": id,
            "nome": data['nome'],
            "sigla": data['sigla']
        })
        
        if result.rowcount == 0:
            return jsonify({'erro': 'Equipe não encontrada'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Equipe atualizada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_equipe.route('/<int:id>', methods=['DELETE'])
def deletar_equipe(id):
    try:
        query = text("DELETE FROM equipes WHERE id_equipe = :id")
        result = db.session.execute(query, {"id": id})
        
        if result.rowcount == 0:
            return jsonify({'erro': 'Equipe não encontrada'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Equipe excluída com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400