from flask import Blueprint, request, jsonify
from app.models import db
from sqlalchemy import text

bp_escalacao = Blueprint('escalacoes', __name__, url_prefix='/escalacoes')

@bp_escalacao.route('/partida/<int:id_partida>', methods=['GET'])
def listar_escalacao_por_partida(id_partida):
    """Lista todos os jogadores escalados para uma partida específica."""
    query = text("""
        SELECT e.id_escalacao, j.nome as jogador, eq.nome as equipe, e.numero_camisa
        FROM escalacoes e
        JOIN jogadores j ON e.id_jogador = j.id_jogador
        JOIN equipes eq ON e.id_equipe = eq.id_equipe
        WHERE e.id_partida = :id_partida
    """)
    result = db.session.execute(query, {"id_partida": id_partida}).fetchall()
    
    escalacao = [{
        'id_escalacao': row.id_escalacao,
        'jogador': row.jogador,
        'equipe': row.equipe,
        'numero_camisa': row.numero_camisa
    } for row in result]
    
    return jsonify(escalacao)

@bp_escalacao.route('/', methods=['POST'])
def escalar_jogador():
    """Adiciona um jogador a uma partida."""
    data = request.json
    try:
        query = text("""
            INSERT INTO escalacoes (id_partida, id_equipe, id_jogador, numero_camisa)
            VALUES (:id_partida, :id_equipe, :id_jogador, :numero_camisa)
            RETURNING id_escalacao;
        """)
        
        result = db.session.execute(query, {
            "id_partida": data['id_partida'],
            "id_equipe": data['id_equipe'],
            "id_jogador": data['id_jogador'],
            "numero_camisa": data['numero_camisa']
        }).scalar_one()
        
        db.session.commit()
        return jsonify({'id_escalacao': result, 'mensagem': 'Jogador escalado com sucesso!'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_escalacao.route('/<int:id_escalacao>', methods=['DELETE'])
def remover_jogador_escalado(id_escalacao):
    """Remove um jogador da escalação de uma partida."""
    try:
        query = text("DELETE FROM escalacoes WHERE id_escalacao = :id_escalacao")
        result = db.session.execute(query, {"id_escalacao": id_escalacao})
        
        if result.rowcount == 0:
            return jsonify({'erro': 'Registro de escalação não encontrado'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Jogador removido da escalação com sucesso'})
        
    except Exception as e:
        db.session.rollback()

        if 'foreign key constraint' in str(e).lower():
            return jsonify({'erro': 'Não é possível remover. Existem eventos associados a este jogador na partida.'}), 409
        return jsonify({'erro': str(e)}), 400