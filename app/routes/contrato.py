from flask import Blueprint, request, jsonify
from app.models import db
from datetime import datetime
from sqlalchemy import text

bp_contrato = Blueprint('contratos', __name__, url_prefix='/contratos')

@bp_contrato.route('/', methods=['GET'])
def listar_contratos():
    """Lista os contratos utilizando a view vw_jogadores_contratos_ativos."""
    query = text("SELECT * FROM vw_jogadores_contratos_ativos")
    result = db.session.execute(query).fetchall()
    
    contratos = [{
        'id_contrato': c.id_contrato,
        'id_jogador': c.id_jogador,
        'nome_jogador': c.nome_jogador,
        'nome_equipe': c.nome_equipe,
        'data_inicio': c.data_inicio.isoformat() if c.data_inicio else None,
        'data_fim': c.data_fim.isoformat() if c.data_fim else None,
        'salario': c.salario,
        'status': c.status,
    } for c in result]
    
    return jsonify(contratos)

@bp_contrato.route('/jogador/<int:id_jogador>', methods=['GET'])
def buscar_contrato_por_id_jogador(id_jogador):
    query = text("SELECT * FROM contratos WHERE id_jogador = :id_jogador AND status = 'Ativo' ORDER BY data_inicio DESC")
    result = db.session.execute(query, {"id_jogador": id_jogador}).first()
    
    if result is None:
        return jsonify({'erro': 'Nenhum contrato ativo encontrado para este jogador'}), 404
        
    return jsonify({
        'id': result.id_contrato,
        'data_inicio': result.data_inicio.isoformat() if result.data_inicio else None,
        'data_fim': result.data_fim.isoformat() if result.data_fim else None,
        'salario': result.salario,
        'status': result.status,
        'id_jogador': result.id_jogador,
        'id_equipe': result.id_equipe
    })

@bp_contrato.route('/', methods=['POST'])
def criar_contrato():
    data = request.json
    try:
        query = text("""
            INSERT INTO contratos (id_jogador, id_equipe, data_inicio, data_fim, salario, status)
            VALUES (:id_jogador, :id_equipe, :data_inicio, :data_fim, :salario, :status)
        """)
        
        result = db.session.execute(query, {
            "id_jogador": data['id_jogador'],
            "id_equipe": data['id_equipe'],
            "data_inicio": datetime.strptime(data['data_inicio'], '%Y-%m-%d').date(),
            "data_fim": datetime.strptime(data['data_fim'], '%Y-%m-%d').date(),
            "salario": data['salario'],
            "status": data.get('status', 'Ativo')
        })
        
        db.session.commit()
        return jsonify({'id': result.lastrowid}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_contrato.route('/<int:id>', methods=['PUT'])
def atualizar_contrato(id):
    data = request.json
    try:
        query = text("""
            UPDATE contratos
            SET data_inicio = :data_inicio, data_fim = :data_fim, salario = :salario, status = :status
            WHERE id_contrato = :id
        """)
        
        result = db.session.execute(query, {
            "id": id,
            "data_inicio": datetime.strptime(data['data_inicio'], '%Y-%m-%d').date(),
            "data_fim": datetime.strptime(data['data_fim'], '%Y-%m-%d').date(),
            "salario": data['salario'],
            "status": data['status']
        })
        
        if result.rowcount == 0:
            return jsonify({'erro': 'Contrato não encontrado'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Contrato atualizado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_contrato.route('/<int:id>', methods=['DELETE'])
def deletar_contrato(id):
    try:
        query = text("DELETE FROM contratos WHERE id_contrato = :id")
        result = db.session.execute(query, {"id": id})
        
        if result.rowcount == 0:
            return jsonify({'erro': 'Contrato não encontrado'}), 404
            
        db.session.commit()
        return jsonify({'mensagem': 'Contrato excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_contrato.route('/registrar-via-procedure', methods=['POST'])
def criar_contrato_procedure():
    data = request.json
    try:
        db.session.execute(
            text('CALL registrar_contrato(:id_jogador, :id_equipe, :data_inicio, :data_fim, :salario)'),
            {
                'id_jogador': data['id_jogador'],
                'id_equipe': data['id_equipe'],
                'data_inicio': data['data_inicio'],
                'data_fim': data['data_fim'],
                'salario': data['salario']
            }
        )
        db.session.commit()
        return jsonify({'mensagem': 'Contrato registrado com sucesso via procedure!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400
        
@bp_contrato.route('/<int:id>/rescindir', methods=['PUT'])
def rescindir_contrato(id):
    """Rescinde um contrato utilizando a stored procedure."""
    try:
        db.session.execute(text('CALL sp_rescindir_contrato(:id)'), {'id': id})
        db.session.commit()
        return jsonify({'mensagem': 'Contrato rescindido com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400