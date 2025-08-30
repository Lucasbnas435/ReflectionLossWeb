import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from flask import render_template

from src.use_cases.calcular_rl import calcular_rl


def plotar_rl_espessura_variavel(
    nome_arquivo_csv: str,
    caminho_arquivo_txt: str,
    unidade_frequencia: str,
    identificador_arquivo: str,
    espessura_amostra: float,
    inicio: float,
    fim: float,
    passo: float,
    baixar_grafico: bool,
    coaxial: bool = False,
):
    # menor_y = 99999999
    # curva_menor_y = float()

    with open(caminho_arquivo_txt, "r") as arquivo_txt:
        conteudo_arquivo_txt = arquivo_txt.readlines()

    # # Entrada do passo
    # inicio = inicio * 1e-3
    # fim = fim * 1e-3 + 0.001e-3
    # passo = passo * 1e-3
    # menores_valores_rl = []

    fig = plt.figure(figsize=(10, 5))

    frequencias_resultante = []
    s11_v_resultante = []

    for espessura in np.arange(inicio, fim, passo):
        espessura = round(espessura, 3)

        frequencias_plotagem, s11_v = calcular_rl(
            conteudo_arquivo_txt=conteudo_arquivo_txt,
            espessura_amostra=espessura,
        )

        frequencias_resultante.append(frequencias_plotagem)
        s11_v_resultante.append(s11_v)

        # Dados para serem Plotados
        plt.plot(frequencias_plotagem, s11_v, label=str(espessura))
        """
        if baixar_grafico:
            contador = 0  # para impressao da matriz de resultados
            matriz = []  # matriz contendo todos rersultados obtidos
            matrizind = []  # cabecalho
            espessura = round(espessura / 1e-3, 2)
            grav = open(
                f"./pythonPaginaINPE/static/files/saidas/saidas_{identificador_arquivo}/mm_{espessura}mm.txt",
                "w",
            )
            titulo = "%4s(%3s)  %s\n" % ("Freq", unidade_frequencia, "RL(dB)")
            grav.write(titulo)

            coluna0 = []  # primeira coluna matriz
            colunan = []  # demais colunas matriz
            for i in range(0, len(F)):
                escrever = "%.2f %.2f\n" % (F[i], s11_v[i])
                grav.write(escrever)
                if contador == 0:  # insercao primeira coluna matriz
                    coluna0.append(F[i])
                colunan.append(s11_v[i])  # insercao valores matriz

            # Gravando matriz de resultados
            if contador == 0:
                matrizind.append("Freq(%3s)" % unidade_frequencia)
                matriz.append(coluna0)  # insercao primeira coluna matriz
            matrizind.append("%s(mm)" % espessura)
            matriz.append(colunan)  # insercao valores matriz
            contador = contador + 1

            grav.close()
        """

    """
    # Imprimindo arquivos Todos
    if baixar_grafico:
        arquivo = open(
            f"./pythonPaginaINPE/static/files/saidas/saidas_{identificador_arquivo}/Todos.txt",
            "w",
            encoding="utf-8",
        )
        for i in range(len(matrizind)):
            escrever = "%s " % matrizind[i]
            arquivo.write(escrever)
        arquivo.write("\n")
        for j in range(len(matriz[0])):
            for i in range(len(matriz)):
                escrever = "%.2f " % matriz[i][j]
                arquivo.write(escrever)
            arquivo.write("\n")
        arquivo.close()
        return ""
    """

    # Plotando grafico
    plt.legend(title="Espessura (mm)")
    plt.xlabel(f"Frequência ({unidade_frequencia})")
    plt.ylabel("Perda por Reflexão (dB)")
    plt.title(f"Arquivo: {nome_arquivo_csv}")

    nome_arquivo_imagem = f"rl_epessura_variavel_{identificador_arquivo}.png"
    caminho_imagem = f"{os.getenv("STATIC_FOLDER_PATH")}/images/graficos_gerados/{nome_arquivo_imagem}"
    fig.savefig(caminho_imagem)

    rota_grafico = "/grafico/rl-espessura-variavel"
    rota_informacoes = "/informacoes"
    if coaxial:
        rota_grafico = "/rlespvarcoaxial"
        rota_informacoes = "/informacoescoaxial"

    dados_view = {
        # "curva_menor_y": curva_menor_y,
        "rota_grafico": rota_grafico,
        "rota_informacoes": rota_informacoes,
        "caminho_imagem": caminho_imagem,
        "nome_arquivo_imagem": nome_arquivo_imagem,
        "timestamp": datetime.now().timestamp(),  # usado para cache busting
    }

    return render_template("grafico_espessura_variavel.html", **dados_view)
