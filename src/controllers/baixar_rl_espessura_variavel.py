from flask import Blueprint, send_file, session

from src.models.grafico_espessura_variavel import GraficoEspessuraVariavel
from src.services.zip_service import compactar_pasta

baixar_rl_espessura_variavel_bp = Blueprint(
    "baixar_rl_espessura_variavel", __name__, url_prefix="/grafico"
)


@baixar_rl_espessura_variavel_bp.route(
    "/rl-espessura-variavel/baixar-dados", methods=["GET", "POST"]
)
def baixar_rl_espessura_variavel():
    print("Iniciando download dos dados de RL para espessura variável.")
    identificador_arquivo = session.get("identificador_arquivo", "")

    grafico_espessura_variavel = GraficoEspessuraVariavel(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=identificador_arquivo,
    )

    pasta_arquivos_saida = grafico_espessura_variavel.baixar_dados_grafico(
        inicio=float(session.get("inicio", 0.1)),
        fim=float(session.get("fim", 10.0)),
        passo=float(session.get("passo", 1.0)),
    )

    caminho_arquivo = compactar_pasta(
        pasta_arquivos_saida, identificador_arquivo
    )

    return send_file(
        caminho_arquivo,
        as_attachment=True,
        download_name=f"{identificador_arquivo}.zip",
    )
