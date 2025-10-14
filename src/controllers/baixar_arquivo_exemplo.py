import os

from flask import Blueprint, send_file

baixar_arquivo_exemplo_bp = Blueprint(
    "baixar_arquivo_exemplo", __name__, url_prefix="/arquivo"
)


@baixar_arquivo_exemplo_bp.route(
    "/baixar-arquivo-exemplo", methods=["GET", "POST"]
)
def baixar_arquivo_exemplo():
    return send_file(
        f"{os.getenv("STATIC_FOLDER_PATH")}/files/exemplos/exemplo.csv",
        as_attachment=True,
        download_name="exemplo.csv",
    )
