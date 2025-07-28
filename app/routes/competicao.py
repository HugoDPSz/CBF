from flask import Blueprint, request, jsonify
from app.models import db
from datetime import datetime
from sqlalchemy import text

bp_competicao = Blueprint('competicoes', __name__, url_prefix='/competicoes')

@bp_competicao.route('/', methods=['GET'])
def listar_competicoes():
    query = text("SELECT * FROM competicoes")
    result = db.session.execute(query).fetchall()

    competicoes = [{
        'id_competicao': row.id_competicao,
        'nome': row.nome,
        'data_inicio': row.data_inicio.isoformat() if row.data_inicio else None,
        'data_fim': row.data_fim.isoformat() if row.data_fim else None,
        'local': row.local,
        'organizador': row.organizador
    } for row in result]
    
    return jsonify(competicoes)

@bp_competicao.route('/<int:id>', methods=['GET'])
def buscar_competicao_por_id(id):
    query = text("SELECT * FROM competicoes WHERE id_competicao = :id")
    result = db.session.execute(query, {"id": id}).first()

    if result is None:
        return jsonify({'erro': 'Competição não encontrada'}), 404
        
    return jsonify({
        'id_competicao': result.id_competicao,
        'nome': result.nome,
        'data_inicio': result.data_inicio.isoformat() if result.data_inicio else None,
        'data_fim': result.data_fim.isoformat() if result.data_fim else None,
        'local': result.local,
        'organizador': result.organizador
    })

@bp_competicao.route('/', methods=['POST'])
def criar_competicao():
    data = request.json
    try:
        query = text("""
            INSERT INTO competicoes (nome, data_inicio, data_fim, local, organizador)
            VALUES (:nome, :data_inicio, :data_fim, :local, :organizador)
        """)
        
        result = db.session.execute(query, {
            "nome": data['nome'],
            "data_inicio": datetime.strptime(data['data_inicio'], '%Y-%m-%d').date(),
            "data_fim": datetime.strptime(data['data_fim'], '%Y-%m-%d').date(),
            "local": data['local'],
            "organizador": data['organizador']
        })
        
        db.session.commit()
        return jsonify({'id': result.lastrowid}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400
    
@bp_competicao.route('/<int:id>', methods=['PUT'])
def atualizar_competicao(id):
    data = request.json
    try:
        query = text("""
            UPDATE competicoes
            SET nome = :nome, data_inicio = :data_inicio, data_fim = :data_fim, 
                local = :local, organizador = :organizador
            WHERE id_competicao = :id
        """)
        
        result = db.session.execute(query, {
            "id": id,
            "nome": data['nome'],
            "data_inicio": datetime.strptime(data['data_inicio'], '%Y-%m-%d').date(),
            "data_fim": datetime.strptime(data['data_fim'], '%Y-%m-%d').date(),
            "local": data['local'],
            "organizador": data['organizador']
        })

        if result.rowcount == 0:
            return jsonify({'erro': 'Competição não encontrada'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Competição atualizada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_competicao.route('/<int:id>', methods=['DELETE'])
def deletar_competicao(id):
    try:
        query = text("DELETE FROM competicoes WHERE id_competicao = :id")
        result = db.session.execute(query, {"id": id})

        if result.rowcount == 0:
            return jsonify({'erro': 'Competição não encontrada'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Competição excluída com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400