from flask import Blueprint, request, jsonify
from app.models.jogador import db, Jogador
from datetime import datetime

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
        'pe_prefirido' : j.pe_preferido
    }for j in jogadores])

@bp_jogador.route('/<int:id>', methods=['GET'])
def buscar_jogador_por_id(id):
    j = Jogador.query.get_or_404(id)
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