from flask import Blueprint, request, jsonify
from app.models import db
from sqlalchemy import text

bp_eventos = Blueprint('eventos', __name__, url_prefix='/eventos')

@bp_eventos.route('/partida/<int:id_partida>', methods=['GET'])
def listar_eventos_por_partida(id_partida):
    """Lista todos os eventos de uma partida."""
    query = text("""
        SELECT ev.id_evento, ev.tipo_evento, ev.minuto, ev.descricao,
               j.nome as jogador_nome
        FROM eventos_partida ev
        LEFT JOIN jogadores j ON ev.id_jogador = j.id_jogador
        WHERE ev.id_partida = :id_partida
        ORDER BY ev.minuto
    """)
    result = db.session.execute(query, {"id_partida": id_partida}).fetchall()

    eventos = [{
        'id_evento': row.id_evento,
        'tipo_evento': row.tipo_evento,
        'minuto': row.minuto,
        'descricao': row.descricao,
        'jogador': row.jogador_nome
    } for row in result]
    
    return jsonify(eventos)

@bp_eventos.route('/', methods=['POST'])
def registrar_evento():
    """Registra um novo evento em uma partida."""
    data = request.json
    try:
        query = text("""
            INSERT INTO eventos_partida (id_partida, id_jogador, tipo_evento, minuto, descricao)
            VALUES (:id_partida, :id_jogador, :tipo_evento, :minuto, :descricao)
            RETURNING id_evento;
        """)
        
        result = db.session.execute(query, {
            "id_partida": data['id_partida'],
            "id_jogador": data.get('id_jogador'), # Pode ser nulo para eventos gerais
            "tipo_evento": data['tipo_evento'],
            "minuto": data['minuto'],
            "descricao": data.get('descricao')
        }).scalar_one()
        
        db.session.commit()
        return jsonify({'id_evento': result, 'mensagem': 'Evento registrado com sucesso!'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_eventos.route('/<int:id_evento>', methods=['DELETE'])
def deletar_evento(id_evento):
    """Deleta um evento registrado."""
    try:
        query = text("DELETE FROM eventos_partida WHERE id_evento = :id_evento")
        result = db.session.execute(query, {"id_evento": id_evento})
        
        if result.rowcount == 0:
            return jsonify({'erro': 'Evento não encontrado'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Evento deletado com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400