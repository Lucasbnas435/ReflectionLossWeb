import os
from datetime import datetime

import matplotlib.pyplot as plt
from flask import render_template

from src.use_cases.calcular_rl import calcular_rl


def plotar_rl_espessura_fixa(
    nome_arquivo_csv: str,
    caminho_arquivo_txt: str,
    unidade_frequencia: str,
    identificador_arquivo: str,
    espessura_amostra: float,
    baixar_grafico: bool,
    coaxial: bool = False,
):
    with open(caminho_arquivo_txt, "r") as arquivo_txt:
        conteudo_arquivo_txt = arquivo_txt.readlines()

    frequencias, s11_v = calcular_rl(
        conteudo_arquivo_txt=conteudo_arquivo_txt,
        espessura_amostra=espessura_amostra,
    )

    if baixar_grafico:
        # Colocar comando para retornar arquivo
        with open(
            f"{os.getenv("STATIC_FOLDER_PATH")}/files/saidas/saidas_{identificador_arquivo}/mm_{round(espessura_amostra, 2)}mm.txt",
            "w",
        ) as arquivo_dados_grafico:
            # Título
            arquivo_dados_grafico.write(f"Freq {unidade_frequencia} RL(dB)")
            # Dados do gráfico
            for frequencia, rl in zip(frequencias, s11_v):
                arquivo_dados_grafico.write(f"{frequencia:.2f} {rl:.2f}")

        return f"mm_{round(espessura_amostra, 2)}mm.txt"

    # Plotando grafico
    fig = plt.figure(figsize=(10, 5))
    plt.plot(
        frequencias, s11_v, label=str(espessura_amostra)
    )  # Dados para serem plotados
    plt.legend(title="Espessura (mm)")
    plt.xlabel(f"Frequência ({unidade_frequencia})")
    plt.ylabel("Perda por Reflexão (dB)")
    plt.title(f"Arquivo: {nome_arquivo_csv}")

    nome_arquivo_imagem = f"rl_epessura_fixa_{identificador_arquivo}.png"

    caminho_imagem = (
        f"{os.getenv("STATIC_FOLDER_PATH")}/images/{nome_arquivo_imagem}"
    )
    fig.savefig(caminho_imagem)

    rota_grafico = "/reflectionlossespfixa"
    rota_informacoes = "/informacoes"
    if coaxial:
        rota_grafico = "/rlespfixacoaxial"
        rota_informacoes = "/informacoescoaxial"

    dados_view = {
        "rota_grafico": rota_grafico,
        "rota_informacoes": rota_informacoes,
        "caminho_imagem": caminho_imagem,
        "nome_arquivo_imagem": nome_arquivo_imagem,
        "timestamp": datetime.now().timestamp(),  # usado para cache busting
    }

    return render_template("grafico_espessura_fixa.html", **dados_view)
