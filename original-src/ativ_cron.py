import os
import shutil

diretorio_templates = "/home/lucasbnas435/pythonPaginaINPE/templates"

for template in os.listdir(diretorio_templates):
    if (not os.path.isdir(f"{diretorio_templates}/{template}")) and template[:5] == "plot_":
        os.remove(f"{diretorio_templates}/{template}")

diretorio_csv = "/home/lucasbnas435/pythonPaginaINPE/static/files"

for arquivo in os.listdir(diretorio_csv):
    if (not os.path.isdir(f"{diretorio_csv}/{arquivo}")) and arquivo[-4:] == ".csv":
        os.remove(f"{diretorio_csv}/{arquivo}")

diretorio_saidas = "/home/lucasbnas435/pythonPaginaINPE/static/files/saidas"

for pasta in os.listdir(diretorio_saidas):
    if os.path.isdir(f"{diretorio_saidas}/{pasta}") and pasta[:7] == "saidas_":
        shutil.rmtree(f"{diretorio_saidas}/{pasta}")

diretorio_zip = "/home/lucasbnas435/pythonPaginaINPE/static/files/saidas/zip_gerado"

for arquivo in os.listdir(diretorio_zip):
    if (not os.path.isdir(f"{diretorio_zip}/{arquivo}")) and arquivo[-4:] == ".zip":
        os.remove(f"{diretorio_zip}/{arquivo}")

diretorio_txt = "/home/lucasbnas435/pythonPaginaINPE/static/files/txt_gerado"

for arquivo in os.listdir(diretorio_txt):
    if (not os.path.isdir(f"{diretorio_txt}/{arquivo}")) and arquivo[-4:] == ".txt":
        os.remove(f"{diretorio_txt}/{arquivo}")
