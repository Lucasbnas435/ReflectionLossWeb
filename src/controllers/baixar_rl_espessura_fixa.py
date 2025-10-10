from flask import Blueprint, send_file, session

from src.models.grafico_espessura_fixa import GraficoEspessuraFixa

baixar_rl_espessura_fixa_bp = Blueprint(
    "baixar_rl_espessura_fixa", __name__, url_prefix="/grafico"
)


@baixar_rl_espessura_fixa_bp.route(
    "/rl-espessura-fixa/baixar-dados", methods=["GET", "POST"]
)
def baixar_rl_espessura_fixa():
    espessura_amostra = session.get("espessura_amostra", 1.0)

    grafico_espessura_fixa = GraficoEspessuraFixa(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=session.get("identificador_arquivo", ""),
        espessura_amostra=espessura_amostra,
    )

    caminho_arquivo = grafico_espessura_fixa.baixar_dados_grafico()

    return send_file(
        caminho_arquivo,
        as_attachment=True,
        download_name=f"{espessura_amostra}_mm.txt",
    )
