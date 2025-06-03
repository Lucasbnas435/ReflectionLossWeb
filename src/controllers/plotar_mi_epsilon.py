import matplotlib.pyplot as plt
import numpy as np
from flask import render_template


def plotar_mi_epsilon(
    hash_arquivo: str,
    caminho_arquivo_txt: str,
    nome_arquivo_csv: str,
    unidade_frequencia: str,
    coaxial: bool = False,
):
    try:
        dados = np.loadtxt(caminho_arquivo_txt)
    except Exception as e:
        print(f"Erro ao ler arquivo txt para plotar mi e epsilon: {e}")
        raise

    print("Extraindo dados de mi e epsilon")
    frequencia = dados[:, 0]
    e = dados[:, 1]
    e_prime = dados[:, 2]
    u = dados[:, 3]
    u_prime = dados[:, 4]

    print("Iniciando plotagem do gráfico de permissividade elétrica")
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 2, 1)
    plt.plot(frequencia, e, label="\u03b5'")
    plt.plot(frequencia, e_prime, label="\u03b5''")
    plt.xlabel(f"Frequência ({unidade_frequencia})")
    plt.ylabel("Permissividade Elétrica Relativa (\u03b5\u1d63)")
    plt.title(
        f"Arquivo: {nome_arquivo_csv}\nGráfico \u03b5' vs. \u03b5'' em função da Frequência"
    )
    plt.legend()
    plt.grid(True)
    print("Plotagem do gráfio de permissividade elétrica finalizada")

    print("Iniciando plotagem do gráfico de permeabilidade magnética")
    ax = fig.add_subplot(1, 2, 2)
    plt.plot(frequencia, u, label="\u00b5'")
    plt.plot(frequencia, u_prime, label="\u00b5''")
    plt.xlabel(f"Frequência ({unidade_frequencia})")
    plt.ylabel("Permeabilidade Magnética Relativa (\u00b5\u1d63)")
    plt.title(
        f"Arquivo: {nome_arquivo_csv}\nGráfico \u00b5' vs. \u00b5'' em função da Frequência"
    )
    plt.legend()
    plt.grid(True)
    print("Plotagem do gráfico de permeabilidade magnética finalizada")

    caminho_imagem = (
        f"./pythonPaginaINPE/static/images/mi_epsilon_{hash_arquivo}.png"
    )
    fig.savefig(caminho_imagem)

    rota_informacoes = "/informacoes"
    if coaxial:
        rota_informacoes = "/informacoescoaxial"

    return render_template("grafico_mi_epsilon.html")
