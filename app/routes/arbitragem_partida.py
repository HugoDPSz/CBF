from flask import Blueprint, request, jsonify
from app.models import db
from sqlalchemy import text

bp_arbitragem = Blueprint('arbitragem', __name__, url_prefix='/arbitragem')

@bp_arbitragem.route('/partida/<int:id_partida>', methods=['GET'])
def listar_arbitragem_por_partida(id_partida):
    """Lista a equipe de arbitragem de uma partida."""
    query = text("""
        SELECT ap.id_arbitragem, a.nome as arbitro, ap.funcao
        FROM arbitragem_partidas ap
        JOIN arbitros a ON ap.id_arbitro = a.id_arbitro
        WHERE ap.id_partida = :id_partida
    """)
    result = db.session.execute(query, {"id_partida": id_partida}).fetchall()

    arbitragem = [{
        'id_arbitragem': row.id_arbitragem,
        'arbitro': row.arbitro,
        'funcao': row.funcao
    } for row in result]
    
    return jsonify(arbitragem)

@bp_arbitragem.route('/', methods=['POST'])
def alocar_arbitro_partida():
    """Aloca um árbitro para uma partida com uma função específica."""
    data = request.json
    try:
        query = text("""
            INSERT INTO arbitragem_partidas (id_partida, id_arbitro, funcao)
            VALUES (:id_partida, :id_arbitro, :funcao)
            RETURNING id_arbitragem;
        """)
        
        result = db.session.execute(query, {
            "id_partida": data['id_partida'],
            "id_arbitro": data['id_arbitro'],
            "funcao": data['funcao']
        }).scalar_one()
        
        db.session.commit()
        return jsonify({'id_arbitragem': result, 'mensagem': 'Árbitro alocado com sucesso!'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_arbitragem.route('/<int:id_arbitragem>', methods=['DELETE'])
def remover_arbitro_alocado(id_arbitragem):
    """Remove um árbitro da equipe de arbitragem de uma partida."""
    try:
        query = text("DELETE FROM arbitragem_partidas WHERE id_arbitragem = :id_arbitragem")
        result = db.session.execute(query, {"id_arbitragem": id_arbitragem})
        
        if result.rowcount == 0:
            return jsonify({'erro': 'Registro de arbitragem não encontrado'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Árbitro removido da partida com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400