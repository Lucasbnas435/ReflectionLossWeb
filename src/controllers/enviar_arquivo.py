import os

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from src.forms.upload_file_form import UploadFileForm
from src.models.dados_vna import DadosVna
from src.utils.gerar_identificador import gerar_identificador

enviar_arquivo_bp = Blueprint("enviar_arquivo", __name__)


@enviar_arquivo_bp.route("/enviar-arquivo", methods=["GET", "POST"])
def enviar_arquivo():
    print("Rota para envio de arquivo acessada.")
    form = UploadFileForm()

    if form.validate_on_submit():
        print("Arquivo recebido com sucesso.")
        arquivo = form.file.data
        identificador_arquivo = gerar_identificador()
        arquivo.save(
            os.path.join(
                current_app.root_path,
                f"{current_app.config["UPLOAD_FOLDER"]}/csv_enviado",
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

        return redirect(url_for("informacoes.informacoes"))
    return render_template("tela_envio_de_arquivo.html", form=form)
