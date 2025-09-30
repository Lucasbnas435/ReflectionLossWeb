from flask import Blueprint, render_template, request, session

from src.models.grafico_espessura_dinamica import GraficoEspessuraDinamica

plotar_rl_espessura_dinamica_bp = Blueprint(
    "plotar_rl_espessura_dinamica", __name__, url_prefix="/grafico"
)


@plotar_rl_espessura_dinamica_bp.route(
    "/rl-espessura-dinamica", methods=["GET", "POST"]
)
def plotar_rl_espessura_dinamica():
    espessura_amostra = float(request.form.get("espessura_amostra", 1.0))

    inicio_slider = float(request.form.get("inicio_slider", 0.1))
    fim_slider = float(request.form.get("fim_slider", 10.0))

    grafico_espessura_dinamica = GraficoEspessuraDinamica(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=session.get("identificador_arquivo", ""),
    )

    dados_plotagem = grafico_espessura_dinamica.plotar_grafico(
        espessura_amostra=espessura_amostra,
        inicio_slider=inicio_slider,
        fim_slider=fim_slider,
    )

    return render_template("grafico_espessura_dinamica.html", **dados_plotagem)
