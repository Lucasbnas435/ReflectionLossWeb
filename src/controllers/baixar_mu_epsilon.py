from flask import Blueprint, send_file, session

from src.models.grafico_mu_epsilon import GraficoMuEpsilon

baixar_mu_epsilon_bp = Blueprint(
    "baixar_mu_epsilon", __name__, url_prefix="/grafico"
)


@baixar_mu_epsilon_bp.route(
    "/mu-epsilon/baixar-dados", methods=["GET", "POST"]
)
def baixar_mu_epsilon():
    print("Iniciando download dos dados de mu e epsilon.")
    identificador_arquivo = session.get("identificador_arquivo", "")

    grafico_mu_epsilon = GraficoMuEpsilon(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=identificador_arquivo,
    )

    caminho_arquivo = grafico_mu_epsilon.baixar_dados_grafico()

    return send_file(
        caminho_arquivo,
        as_attachment=True,
        download_name=f"mu_epsilon_{identificador_arquivo}.txt",
    )
