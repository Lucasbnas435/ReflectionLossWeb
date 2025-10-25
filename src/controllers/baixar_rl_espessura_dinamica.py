from flask import Blueprint, send_file, session

from src.models.grafico_espessura_dinamica import GraficoEspessuraDinamica

baixar_rl_espessura_dinamica_bp = Blueprint(
    "baixar_rl_espessura_dinamica", __name__, url_prefix="/grafico"
)


@baixar_rl_espessura_dinamica_bp.route(
    "/rl-espessura-dinamica/baixar-dados", methods=["GET", "POST"]
)
def baixar_rl_espessura_dinamica():
    print("Iniciando download dos dados de RL para espessura dinâmica.")
    espessura_amostra = float(session.get("espessura_amostra", 1.0))

    grafico_espessura_dinamica = GraficoEspessuraDinamica(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=session.get("identificador_arquivo", ""),
    )

    caminho_arquivo = grafico_espessura_dinamica.baixar_dados_grafico(
        espessura_amostra
    )

    return send_file(
        caminho_arquivo,
        as_attachment=True,
        download_name=f"{espessura_amostra}_mm.txt",
    )
