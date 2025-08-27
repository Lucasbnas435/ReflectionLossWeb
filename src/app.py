import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from src.controllers.plotar_mi_epsilon import plotar_mi_epsilon
from src.controllers.plotar_rl_dinamico import plotar_rl_dinamico
from src.controllers.plotar_rl_espessura_fixa import plotar_rl_espessura_fixa
from src.controllers.plotar_rl_espessura_variavel import (
    plotar_rl_espessura_variavel,
)
from src.forms.upload_file_form import UploadFileForm
from src.models.dados_vna import DadosVna
from src.utils.gerar_identificador import gerar_identificador

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "a1b2c3d4"
app.config["UPLOAD_FOLDER"] = "static/files"


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/enviar-arquivo", methods=["GET", "POST"])
def enviar_arquivo():
    form = UploadFileForm()
    if form.validate_on_submit():
        arquivo = form.file.data
        identificador_arquivo = gerar_identificador()
        arquivo.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                f"{app.config["UPLOAD_FOLDER"]}/csv_enviado",
                secure_filename(f"{identificador_arquivo}.csv"),
            )
        )

        dados_vna = DadosVna(identificador_arquivo=identificador_arquivo)
        dados_vna.ler_csv()
        dados_vna.gerar_arquivo_txt()

        dados_arquivo = {
            "nome_arquivo_csv": arquivo.filename,
            "identificador_arquivo": dados_vna.identificador_arquivo,
            "caminho_arquivo_csv": dados_vna.caminho_arquivo_csv,
            "caminho_arquivo_txt": dados_vna.caminho_arquivo_txt,
            "frequencia_corte": dados_vna.frequencia_corte,
            "unidade_frequencia": dados_vna.unidade_frequencia,
            "comprimento_suporte_amostra": dados_vna.comprimento_suporte_amostra,
            "distancia_amostra": dados_vna.distancia_amostra,
            "espessura_amostra": dados_vna.espessura_amostra,
            "ifbw": dados_vna.ifbw,
            "power": dados_vna.power,
            "nome_banda": dados_vna.nome_banda,
        }

        session.update(dados_arquivo)

        return redirect(url_for("informacoes"))
    return render_template("tela_envio_de_arquivo.html", form=form)


@app.route("/informacoes", methods=["GET", "POST"])
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
    return render_template("tela_informacoes.html", **informacoes_extraidas)


@app.route("/grafico/rl-espessura-fixa", methods=["GET", "POST"])
def grafico_rl_espessura_fixa():
    return plotar_rl_espessura_fixa(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=session.get("identificador_arquivo"),
        espessura_amostra=session.get("espessura_amostra"),
        baixar_grafico=False,
        coaxial=False,
    )


@app.route("/grafico/rl-espessura-variavel", methods=["GET", "POST"])
def grafico_rl_espessura_variavel():
    espessura_amostra = float(request.form.get("espessura_amostra", 1.0))

    inicio = float(request.form.get("inicio", 0.1))
    fim = float(request.form.get("fim", 10.0))
    passo = float(request.form.get("passo", 1.0))

    return plotar_rl_espessura_variavel(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=session.get("identificador_arquivo"),
        espessura_amostra=espessura_amostra,
        inicio=inicio,
        fim=fim,
        passo=passo,
        baixar_grafico=False,
        coaxial=False,
    )


@app.route("/grafico/rl-espessura-dinamica", methods=["GET", "POST"])
def grafico_rl_espessura_dinamica():
    espessura_amostra = float(request.form.get("espessura_amostra", 1.0))

    inicio_slider = float(request.form.get("inicio_slider", 0.1))
    fim_slider = float(request.form.get("fim_slider", 10.0))

    return plotar_rl_dinamico(
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        identificador_arquivo=session.get("identificador_arquivo"),
        espessura_amostra=espessura_amostra,
        inicio_slider=inicio_slider,
        fim_slider=fim_slider,
        baixar_grafico=False,
        coaxial=False,
    )


@app.route("/grafico/mi-epsilon", methods=["GET", "POST"])
def grafico_mi_epsilon():
    return plotar_mi_epsilon(
        identificador_arquivo=session.get("identificador_arquivo"),
        caminho_arquivo_txt=session.get("caminho_arquivo_txt", ""),
        nome_arquivo_csv=session.get("nome_arquivo_csv", ""),
        unidade_frequencia=session.get("unidade_frequencia", ""),
        coaxial=False,
    )


@app.errorhandler(Exception)
def error_handler(error):
    print(f"Ocorreu um erro: {str(error)}")
    return render_template("tela_erro.html")


if __name__ == "__main__":
    app.run(debug=True)
