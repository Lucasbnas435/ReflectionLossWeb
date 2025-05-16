import matplotlib.pyplot as plt
import numpy as np
from flask import render_template


def plotar_rl_espessura_fixa(
    nome_arquivo_csv: str,
    caminho_arquivo_txt: str,
    unidade_frequencia: str,
    espessura_amostra: str,
    baixar_grafico: str,
    hash_arquivo: str,
    coaxial: bool = False,
):
    with open(caminho_arquivo_txt, "r") as arquivo_txt:
        conteudo_arquivo_txt = arquivo_txt.readlines()

    # [m] Espessura da amostra (Livro chama de L)
    d = float(espessura_amostra) * 1e-3

    # CONSTANTES
    c = 2.998e8  # [m/s] #velocidade da Luz no vacuo

    # Vetores - 1
    F = []  # frequencia [Hz] DE CALCULO
    F_grafic = []  # FREQUENCIA PARA PLOTAR EM [GHz]

    # Vetores - 2
    er_r = []  # permissividade real
    er_i = []  # permissividade imaginaria
    ur_r = []  # permeabilidade real
    ur_i = []  # permeabilidade imaginaria

    EX = []
    UX = []

    # Vetores - 3
    s11_v = []  # [a.u]

    for n, linha in enumerate(conteudo_arquivo_txt):
        dados = linha.split("\t")
        # frequencia
        f = float(dados[0]) * 1e9
        F.append(f)
        F_grafic.append(f / 1e9)

        # Permissividade NRW
        ex = float(dados[1]) + 1j * float(dados[2])
        er_r.append(ex.real)
        er_i.append(ex.imag)
        EX.append(ex)

        # Permeabilidade NRW
        ux = float(dados[3]) + 1j * float(dados[4])
        ur_r.append(ux.real)
        ur_i.append(ux.imag)
        UX.append(ux)

        # *********************Calculo da Refletividade (RL)***************
        # Calcular impedância de entrada
        z = (50 * (UX[n] / EX[n]) ** (1.0 / 2.0)) * np.tanh(
            1j * (2 * np.pi * d * f / c) * ((UX[n] * EX[n]) ** (1.0 / 2.0))
        )
        db = -20 * np.log10(
            abs((z - 50) / (z + 50))
        )  # [dB] somente para voltagem
        s11_v.append(round(db, 5))

    if baixar_grafico:
        # Colocar comando para retornar arquivo
        espessura = str(round(d / 1e-3, 2))
        with open(
            f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}/mm_{espessura}mm.txt",
            "w",
        ) as arquivo_dados_grafico:
            # Título
            arquivo_dados_grafico.write(f"Freq {unidade_frequencia} RL(dB)")
            # Dados do gráfico
            for i in range(len(F)):
                arquivo_dados_grafico.write(f"{F[i]:.2f} {s11_v[i]:.2f}")
        return f"mm_{espessura}mm.txt"

    # Plotando grafico
    fig = plt.figure(figsize=(10, 5))
    plt.plot(F, s11_v, label=str(float(d) * 1e3))  # Dados para serem plotados
    plt.legend(title="Espessura (mm)")
    plt.xlabel(f"Frequência ({unidade_frequencia})")
    plt.ylabel("Perda por Reflexão (dB)")
    plt.title(f"Arquivo: {nome_arquivo_csv}")

    caminho_imagem = (
        f"./pythonPaginaINPE/static/images/rl_epessura_fixa_{hash_arquivo}.png"
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
    }

    return render_template("grafico_espessura_fixa.html", **dados_view)
