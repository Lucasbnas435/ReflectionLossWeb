import os

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from src.forms.upload_file_form import UploadFileForm
from src.models.dados_vna import DadosVna
from src.utils.gerar_identificador import gerar_identificador

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
                app.config["UPLOAD_FOLDER"],
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


@app.route("/informacoes", methods=["POST"])
def informacoes():
    try:
        csv_filename = request.form.get("csv_filename")
        identificador_arquivo = request.form.get("identificador_arquivo")
        (
            txt_filename,
            compsuporteamostra,
            frequenciacorte,
            distamostra,
            espamostra,
            ifbw,
            power,
            nome_banda,
            undfrequencia,
        ) = read_csv(identificador_arquivo)
        read_txt(txt_filename)

        return render_template(
            "informacoes.html",
            csv_filename=csv_filename,
            nome_arquivo_txt=txt_filename,
            frequenciacorte=frequenciacorte,
            compsuporteamostra=compsuporteamostra,
            distamostra=distamostra,
            espamostra=espamostra,
            ifbw=ifbw,
            power=power,
            nome_banda=nome_banda,
            undfrequencia=undfrequencia,
            identificador_arquivo=identificador_arquivo,
        )
    except:
        return render_template("error_template.html")


@app.route("/grafico/rl-espessura-fixa", methods=["POST"])
def reflectionlossespfixa():
    try:
        identificador_arquivo = request.form.get("identificador_arquivo")
        csv_filename = request.form.get("csv_filename")
        txt_filename = request.form.get("txt_filename")
        undfrequencia = request.form.get("undfrequencia")
        espamostra = request.form.get("espamostra")
        baixar_grafico = int(request.form.get("baixar_grafico"))

        if baixar_grafico:
            filename = RL_esp_fixa_plot(
                csv_filename,
                txt_filename,
                undfrequencia,
                espamostra,
                baixar_grafico,
                identificador_arquivo,
            )
            return send_file(
                f"./static/files/saidas/saidas_{identificador_arquivo}/{filename}",
                as_attachment=True,
            )

        nome_template = RL_esp_fixa_plot(
            csv_filename,
            txt_filename,
            undfrequencia,
            espamostra,
            baixar_grafico,
            identificador_arquivo,
        )
        return render_template(
            nome_template,
            csv_filename=csv_filename,
            nome_arquivo_txt=txt_filename,
            undfrequencia=undfrequencia,
            espamostra=espamostra,
            identificador_arquivo=identificador_arquivo,
        )
    except:
        return render_template("error_template.html")


if __name__ == "__main__":
    app.run(debug=True)
