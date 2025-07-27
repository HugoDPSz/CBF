from .jogador import bp_jogador
from .equipe import bp_equipe
from .competicao import bp_competicao
from .contrato import bp_contrato
from .arbitro import bp_arbitro  
from .partida import bp_partida  
from .escalacao import bp_escalacao
from .arbitragem_partida import bp_arbitragem
from .eventos_partidas import bp_eventos

def init_app(app):
    app.register_blueprint(bp_jogador)
    app.register_blueprint(bp_equipe)
    app.register_blueprint(bp_competicao)
    app.register_blueprint(bp_contrato)
    app.register_blueprint(bp_arbitro)  
    app.register_blueprint(bp_partida)  
    app.register_blueprint(bp_escalacao)
    app.register_blueprint(bp_arbitragem)
    app.register_blueprint(bp_eventos)