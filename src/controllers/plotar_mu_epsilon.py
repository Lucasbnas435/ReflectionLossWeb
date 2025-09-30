from flask import Blueprint, render_template, session

from src.models.grafico_mu_epsilon import GraficoMuEpsilon

plotar_mu_epsilon_bp = Blueprint(
    "plotar_mu_epsilon", __name__, url_prefix="/grafico"
)


@plotar_mu_epsilon_bp.route("/mu-epsilon", methods=["GET", "POST"])
def plotar_mu_epsilon():
    grafico_mu_epsilon = GraficoMuEpsilon(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=session.get("identificador_arquivo", ""),
    )

    dados_plotagem = grafico_mu_epsilon.plotar_grafico()

    return render_template("grafico_mu_epsilon.html", **dados_plotagem)
