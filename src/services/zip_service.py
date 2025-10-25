import os
import shutil


def compactar_pasta(
    caminho_pasta_a_compactar: str, nome_arquivo_saida: str
) -> str:
    print(f"Iniciando compactação da pasta {caminho_pasta_a_compactar}")
    caminho_arquivo_saida = f"{os.getenv("STATIC_FOLDER_PATH")}/files/zip_gerado/{nome_arquivo_saida}"

    shutil.make_archive(
        base_name=caminho_arquivo_saida,
        format="zip",
        root_dir=caminho_pasta_a_compactar,
    )
    print("Pasta compactada com sucesso.")
    return f"{caminho_arquivo_saida}.zip"
