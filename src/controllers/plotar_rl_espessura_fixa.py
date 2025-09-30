from flask import Blueprint, render_template, session

from src.models.grafico_espessura_fixa import GraficoEspessuraFixa

plotar_rl_espessura_fixa_bp = Blueprint(
    "plotar_rl_espessura_fixa", __name__, url_prefix="/grafico"
)


@plotar_rl_espessura_fixa_bp.route(
    "/rl-espessura-fixa", methods=["GET", "POST"]
)
def plotar_rl_espessura_fixa():
    grafico_espessura_fixa = GraficoEspessuraFixa(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=session.get("identificador_arquivo", ""),
        espessura_amostra=session.get("espessura_amostra", 1.0),
    )

    dados_plotagem = grafico_espessura_fixa.plotar_grafico()

    return render_template("grafico_espessura_fixa.html", **dados_plotagem)
