from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .jogador import Jogador
from .equipe import Equipe
from .contrato import Contrato
from .arbitro import Arbitro
from .competicao import Competicao
from .partida import Partida
from .arbitragem_partida import ArbitragemPartida
from .escalacao import Escalacao
from .eventos_partida import EventosPartida