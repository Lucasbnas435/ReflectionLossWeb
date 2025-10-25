from flask import Blueprint, render_template, request, session

from src.models.grafico_espessura_variavel import GraficoEspessuraVariavel

plotar_rl_espessura_variavel_bp = Blueprint(
    "plotar_rl_espessura_variavel", __name__, url_prefix="/grafico"
)


@plotar_rl_espessura_variavel_bp.route(
    "/rl-espessura-variavel", methods=["GET", "POST"]
)
def plotar_rl_espessura_variavel():
    print("Rota para plotagem do gráfico de espessura variável acessada.")
    inicio = float(request.form.get("inicio", 0.1))
    fim = float(request.form.get("fim", 10.0))
    passo = float(request.form.get("passo", 1.0))

    # Armazena na sessão para que a rota de baixar dados possa usar os valores
    session["inicio"] = inicio
    session["fim"] = fim
    session["passo"] = passo

    grafico_espessura_variavel = GraficoEspessuraVariavel(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=session.get("identificador_arquivo", ""),
    )

    dados_plotagem = grafico_espessura_variavel.plotar_grafico(
        inicio=inicio,
        fim=fim,
        passo=passo,
    )

    return render_template("grafico_espessura_variavel.html", **dados_plotagem)
