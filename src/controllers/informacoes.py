from flask import Blueprint, render_template, session

informacoes_bp = Blueprint("informacoes", __name__)


@informacoes_bp.route("/informacoes", methods=["GET", "POST"])
def informacoes():
    informacoes_extraidas = {
        "nome_arquivo_csv": session.get(
            "nome_arquivo_csv", "Nome não encontrado"
        ),
        "frequencia_corte": session.get("frequencia_corte", ""),
        "unidade_frequencia": session.get("unidade_frequencia", ""),
        "comprimento_suporte_amostra": session.get(
            "comprimento_suporte_amostra", ""
        ),
        "distancia_amostra": session.get("distancia_amostra", ""),
        "espessura_amostra": session.get("espessura_amostra", ""),
        "ifbw": session.get("ifbw", ""),
        "power": session.get("power", ""),
        "nome_banda": session.get("nome_banda", ""),
    }
    print(
        f"Informações do arquivo extraídas da sessão: {informacoes_extraidas}"
    )
    return render_template("tela_informacoes.html", **informacoes_extraidas)
