from .informacoes import informacoes_bp
from .plotar_mu_epsilon import plotar_mu_epsilon_bp
from .plotar_rl_espessura_dinamica import plotar_rl_espessura_dinamica_bp
from .plotar_rl_espessura_fixa import plotar_rl_espessura_fixa_bp
from .plotar_rl_espessura_variavel import plotar_rl_espessura_variavel_bp


def register_controllers(app):
    app.register_blueprint(informacoes_bp)
    app.register_blueprint(plotar_mu_epsilon_bp)
    app.register_blueprint(plotar_rl_espessura_fixa_bp)
    app.register_blueprint(plotar_rl_espessura_variavel_bp)
    app.register_blueprint(plotar_rl_espessura_dinamica_bp)
