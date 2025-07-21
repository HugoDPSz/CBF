from app import app
from .jogador import bp_jogador
from .equipe import bp_equipe

def init_app():
    app.register_blueprint(bp_jogador)
    app.register_blueprint(bp_equipe)