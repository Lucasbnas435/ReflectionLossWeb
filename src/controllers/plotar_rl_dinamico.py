import os

# import shutil
from datetime import datetime

import matplotlib.pyplot as plt
from flask import render_template

from src.use_cases.calcular_rl import calcular_rl


def plotar_rl_dinamico(
    nome_arquivo_csv: str,
    caminho_arquivo_txt: str,
    unidade_frequencia: str,
    identificador_arquivo: str,
    espessura_amostra: float,
    inicio_slider: float,
    fim_slider: float,
    baixar_grafico: bool,
    coaxial: bool = False,
):
    with open(caminho_arquivo_txt, "r") as arquivo_txt:
        conteudo_arquivo_txt = arquivo_txt.readlines()

    frequencias_plotagem, s11_v = calcular_rl(
        conteudo_arquivo_txt=conteudo_arquivo_txt,
        espessura_amostra=espessura_amostra,
    )

    """
    if baixar_grafico:
        try:
            os.mkdir(
                f"./pythonPaginaINPE/static/files/saidas/saidas_{identificador_arquivo}"
            )
        except:
            shutil.rmtree(
                f"./pythonPaginaINPE/static/files/saidas/saidas_{identificador_arquivo}"
            )
            os.mkdir(
                f"./pythonPaginaINPE/static/files/saidas/saidas_{identificador_arquivo}"
            )

        espessura = str(round(d / 1e-3, 2))
        grav = open(
            f"./pythonPaginaINPE/static/files/saidas/saidas_{identificador_arquivo}/mm_{espessura}mm.txt",
            "w",
        )
        titulo = "%4s(%3s)  %s\n" % ("Freq", unidade_frequencia, "RL(dB)")
        grav.write(titulo)

        for i in range(0, len(F)):
            escrever = "%.2f %.2f\n" % (F[i], s11_v[i])
            grav.write(escrever)

        grav.close()
        return f"mm_{espessura}mm.txt"
    """

    fig = plt.figure(figsize=(10, 5))
    # Dados para serem Plotados
    plt.plot(frequencias_plotagem, s11_v, label=str(espessura_amostra))

    # Plotando grafico
    plt.legend(title="Espessura (mm)")
    plt.xlabel(f"Frequência ({unidade_frequencia})")
    plt.ylabel("Perda por Reflexão (dB)")
    plt.title(f"Arquivo: {nome_arquivo_csv}")

    nome_arquivo_imagem = f"rl_epessura_dinamica_{identificador_arquivo}.png"

    caminho_imagem = f"{os.getenv("STATIC_FOLDER_PATH")}/images/graficos_gerados/{nome_arquivo_imagem}"
    fig.savefig(caminho_imagem)

    rota_grafico = "/grafico/rl-espessura-dinamica"
    rota_informacoes = "/informacoes"
    if coaxial:
        rota_grafico = "/rldinamicocoaxial"
        rota_informacoes = "/informacoescoaxial"

    dados_view = {
        "rota_grafico": rota_grafico,
        "rota_informacoes": rota_informacoes,
        "caminho_imagem": caminho_imagem,
        "nome_arquivo_imagem": nome_arquivo_imagem,
        "espessura_amostra": espessura_amostra,
        "timestamp": datetime.now().timestamp(),  # usado para cache busting
        "inicio_slider": inicio_slider,
        "fim_slider": fim_slider,
    }
    return render_template("grafico_espessura_dinamica.html", **dados_view)
