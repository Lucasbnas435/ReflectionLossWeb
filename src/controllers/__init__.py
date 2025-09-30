from .plotar_mu_epsilon import plotar_mu_epsilon_bp
from .plotar_rl_espessura_fixa import plotar_rl_espessura_fixa_bp


def register_controllers(app):
    app.register_blueprint(plotar_mu_epsilon_bp)
    app.register_blueprint(plotar_rl_espessura_fixa_bp)
