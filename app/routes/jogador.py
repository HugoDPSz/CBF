from flask import Blueprint, request, jsonify
from app.models.jogador import db, Jogador
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import text

bp_jogador = Blueprint('jogadores', __name__, url_prefix='/jogadores')

@bp_jogador.route('/', methods=['GET'])
def listar_jogadores():
    jogadores = Jogador.query.all()
    return jsonify([{
        'id' : j.id_jogador,
        'nome' : j.nome,
        'posicao' : j.posicao,
        'altura' : j.altura,
        'peso' : j.peso,
        'data_nascimento' : j.data_nascimento.isoformat() if j.data_nascimento else None,
        'nacionalidade' : j.nacionalidade,
        'pe_prefirido' : j.pe_preferido.name
    }for j in jogadores])

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
        jogador = Jogador(
            nome = data['nome'],
            posicao = data['posicao'],
            altura = data['altura'],
            peso = data['peso'],
            data_nascimento=datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date(),
            nacionalidade = data['nacionalidade']
        )
        db.session.add(jogador)
        db.session.commit()
        return jsonify({'id': jogador.id_jogador}), 201
    except Exception as e:
        return jsonify({'erro' : str(e)}), 400

@bp_jogador.route('/<int:id>', methods=['PUT'])
def atualizar_jogador(id):
    j = Jogador.query.get_or_404(id)
    data = request.json

    j.posicao = data['posicao']
    j.altura = data['altura']
    j.peso = data['peso']
    
    db.session.commit()
    return jsonify({
        'id' : j.id_jogador,
        'nome' : j.nome,
        'posicao' : j.posicao,
        'altura' : j.altura,
        'peso' : j.peso,
        'data_nascimento' : j.data_nascimento.isoformat() if j.data_nascimento else None,
        'nacionalidade' : j.nacionalidade,
        'pe_prefirido' : j.pe_preferido
    })    

@bp_jogador.route('/<int:id>', methods=['DELETE'])
def deletar_jogador(id):
    jogador = Jogador.query.get_or_404(id)
    db.session.delete(jogador)
    db.session.commit()
    return jsonify({'mensagem' : 'jogador excluído'})

@bp_jogador.route('/<int:id>/com-idade', methods=['GET'])
def buscar_jogador_com_idade(id):
    j = Jogador.query.get_or_404(id)
    
    idade = db.session.query(func.calcular_idade(j.data_nascimento)).scalar()
    
    return jsonify({
        'id' : j.id_jogador,
        'nome' : j.nome,
        'posicao' : j.posicao,
        'data_nascimento' : j.data_nascimento.isoformat() if j.data_nascimento else None,
        'idade': idade 
    })