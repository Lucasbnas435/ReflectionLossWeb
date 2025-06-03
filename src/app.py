import os

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from src.forms.upload_file_form import UploadFileForm
from src.utils.gerar_identificador import gerar_identificador

app = Flask(__name__)
app.config["SECRET_KEY"] = "a1b2c3d4"
app.config["UPLOAD_FOLDER"] = "static/files"


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/arquivo", methods=["GET", "POST"])
def arquivoumacamada():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        hash_arquivo = gerar_identificador()
        file.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                secure_filename(f"{hash_arquivo}.csv"),
            )
        )
        csv_filename = file.filename
        return render_template(
            "redirecionar.html",
            hash_arquivo=hash_arquivo,
            csv_filename=csv_filename,
        )
    return render_template("arquivo_uma_camada.html", form=form)


@app.route("/informacoes", methods=["POST"])
def informacoes():
    try:
        csv_filename = request.form.get("csv_filename")
        hash_arquivo = request.form.get("hash_arquivo")
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
        ) = read_csv(hash_arquivo)
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
            hash_arquivo=hash_arquivo,
        )
    except:
        return render_template("error_template.html")


@app.route("/grafico/rl-espessura-fixa", methods=["POST"])
def reflectionlossespfixa():
    try:
        hash_arquivo = request.form.get("hash_arquivo")
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
                hash_arquivo,
            )
            return send_file(
                f"./static/files/saidas/saidas_{hash_arquivo}/{filename}",
                as_attachment=True,
            )

        nome_template = RL_esp_fixa_plot(
            csv_filename,
            txt_filename,
            undfrequencia,
            espamostra,
            baixar_grafico,
            hash_arquivo,
        )
        return render_template(
            nome_template,
            csv_filename=csv_filename,
            nome_arquivo_txt=txt_filename,
            undfrequencia=undfrequencia,
            espamostra=espamostra,
            hash_arquivo=hash_arquivo,
        )
    except:
        return render_template("error_template.html")


if __name__ == "__main__":
    app.run(debug=True)
