from app import app
from .jogador import bp_jogador
from .equipe import bp_equipe
from .competicao import bp_competicao

def init_app():
    app.register_blueprint(bp_jogador)
    app.register_blueprint(bp_equipe)
    app.register_blueprint(bp_competicao)