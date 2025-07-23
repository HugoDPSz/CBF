from .jogador import bp_jogador
from .equipe import bp_equipe
from .competicao import bp_competicao
from .contrato import bp_contrato

def init_app(app):
    app.register_blueprint(bp_jogador)
    app.register_blueprint(bp_equipe)
    app.register_blueprint(bp_competicao)
    app.register_blueprint(bp_contrato)