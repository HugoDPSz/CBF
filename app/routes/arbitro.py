from flask import Blueprint, request, jsonify
from app.models.arbitro import db, Arbitro
from datetime import datetime

bp_arbitro = Blueprint('arbitros', __name__, url_prefix='/arbitros')

@bp_arbitro.route('/', methods=['GET'])
def listar_arbitros():
    arbitros = Arbitro.query.all()
    return jsonify([{
        'id_arbitro': a.id_arbitro,
        'nome': a.nome,
        'nacionalidade': a.nacionalidade,
        'categoria': a.categoria,
        'status': a.status,
        'data_nascimento': a.data_nascimento.isoformat() if a.data_nascimento else None,
        'experiencia': a.experiencia
    } for a in arbitros])

@bp_arbitro.route('/<int:id>', methods=['GET'])
def buscar_arbitro_por_id(id):
    a = Arbitro.query.get_or_404(id)
    return jsonify({
        'id_arbitro': a.id_arbitro,
        'nome': a.nome,
        'nacionalidade': a.nacionalidade,
        'categoria': a.categoria,
        'status': a.status,
        'data_nascimento': a.data_nascimento.isoformat() if a.data_nascimento else None,
        'experiencia': a.experiencia
    })

@bp_arbitro.route('/', methods=['POST'])
def criar_arbitro():
    data = request.json
    try:
        arbitro = Arbitro(
            nome=data['nome'],
            nacionalidade=data['nacionalidade'],
            categoria=data['categoria'],
            status=data.get('status', 'Ativo'),
            data_nascimento=datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date(),
            experiencia=data['experiencia']
        )
        db.session.add(arbitro)
        db.session.commit()
        return jsonify({'id': arbitro.id_arbitro}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@bp_arbitro.route('/<int:id>', methods=['PUT'])
def atualizar_arbitro(id):
    a = Arbitro.query.get_or_404(id)
    data = request.json
    try:
        a.nome = data.get('nome', a.nome)
        a.nacionalidade = data.get('nacionalidade', a.nacionalidade)
        a.categoria = data.get('categoria', a.categoria)
        a.status = data.get('status', a.status)
        a.experiencia = data.get('experiencia', a.experiencia)
        if 'data_nascimento' in data:
            a.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'id': a.id_arbitro, 'mensagem': 'Árbitro atualizado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@bp_arbitro.route('/<int:id>', methods=['DELETE'])
def deletar_arbitro(id):
    arbitro = Arbitro.query.get_or_404(id)
    db.session.delete(arbitro)
    db.session.commit()
    return jsonify({'mensagem': 'Árbitro excluído com sucesso'})