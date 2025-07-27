from flask import Blueprint, request, jsonify
from app.models import db
from datetime import datetime
from sqlalchemy import text

bp_jogador = Blueprint('jogadores', __name__, url_prefix='/jogadores')

@bp_jogador.route('/', methods=['GET'])
def listar_jogadores():
    query = text("SELECT * FROM jogadores")
    result = db.session.execute(query).fetchall()
    
    jogadores = [{
        'id': row.id_jogador,
        'nome': row.nome,
        'posicao': row.posicao,
        'altura': row.altura,
        'peso': row.peso,
        'data_nascimento': row.data_nascimento.isoformat() if row.data_nascimento else None,
        'nacionalidade': row.nacionalidade,
        'pe_preferido': row.pe_preferido
    } for row in result]
    
    return jsonify(jogadores)

@bp_jogador.route('/<int:id>', methods=['GET'])
def buscar_jogador_por_id(id):
    query = text("SELECT * FROM jogadores WHERE id_jogador = :id")
    result = db.session.execute(query, {"id": id}).first()
    
    if result is None:
        return jsonify({'erro': 'Jogador não encontrado'}), 404

    jogador_dict = {
        'id': result.id_jogador,
        'nome': result.nome,
        'posicao': result.posicao,
        'altura': result.altura,
        'peso': result.peso,
        'data_nascimento': result.data_nascimento.isoformat() if result.data_nascimento else None,
        'nacionalidade': result.nacionalidade,
        'pe_preferido': result.pe_preferido
    }
    
    return jsonify(jogador_dict)

@bp_jogador.route('/', methods=['POST'])
def criar_jogador():
    data = request.json
    try:
        query = text("""
            INSERT INTO jogadores (nome, posicao, altura, peso, data_nascimento, nacionalidade, pe_preferido)
            VALUES (:nome, :posicao, :altura, :peso, :data_nascimento, :nacionalidade, :pe_preferido)
            RETURNING id_jogador;
        """)
        
        result = db.session.execute(query, {
            "nome": data['nome'],
            "posicao": data['posicao'],
            "altura": data['altura'],
            "peso": data['peso'],
            "data_nascimento": datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date(),
            "nacionalidade": data['nacionalidade'],
            "pe_preferido": data.get('pe_preferido', 'Direito') 
        }).scalar_one() 
        
        db.session.commit()
        return jsonify({'id': result}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_jogador.route('/<int:id>', methods=['PUT'])
def atualizar_jogador(id):
    data = request.json
    try:
        query = text("""
            UPDATE jogadores
            SET posicao = :posicao, altura = :altura, peso = :peso
            WHERE id_jogador = :id
        """)
        db.session.execute(query, {
            "id": id,
            "posicao": data['posicao'],
            "altura": data['altura'],
            "peso": data['peso']
        })
        db.session.commit()
        return jsonify({'mensagem': 'Jogador atualizado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_jogador.route('/<int:id>', methods=['DELETE'])
def deletar_jogador(id):
    try:
        query = text("DELETE FROM jogadores WHERE id_jogador = :id")
        result = db.session.execute(query, {"id": id})
        
        if result.rowcount == 0:
            return jsonify({'erro': 'Jogador não encontrado'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Jogador excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_jogador.route('/<int:id>/com-idade', methods=['GET'])
def buscar_jogador_com_idade(id):
    query_jogador = text("SELECT data_nascimento, nome, posicao FROM jogadores WHERE id_jogador = :id")
    jogador = db.session.execute(query_jogador, {"id": id}).first()
    
    if jogador is None:
        return jsonify({'erro': 'Jogador não encontrado'}), 404
    query_idade = text("SELECT calcular_idade(:data_nasc)")
    idade = db.session.execute(query_idade, {"data_nasc": jogador.data_nascimento}).scalar()
    
    return jsonify({
        'id': id,
        'nome': jogador.nome,
        'posicao': jogador.posicao,
        'data_nascimento': jogador.data_nascimento.isoformat() if jogador.data_nascimento else None,
        'idade': idade
    })