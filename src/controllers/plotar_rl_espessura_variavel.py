import matplotlib.pyplot as plt
import numpy as np
from flask import render_template


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
    menor_y = 99999999
    curva_menor_y = float()

    with open(caminho_arquivo_txt, "r") as arquivo_txt:
        conteudo_arquivo_txt = arquivo_txt.readlines()

    # Ajuste da Referencia de L1 e L2
    # [m] #Espessura da amostra (Livro chama de L)
    d = espessura_amostra * 1e-3

    # CONSTANTES
    c = 2.998e8  # [m/s] #velocidade da Luz no vacuo
    # Vetores - 1
    F = []  # frequencia [Hz] DE CALCULO
    F_grafic = []  # FREQUENCIA PARA PLOTAR EM [GHz]

    # Vetores - 2
    er_r = []  # permissividade real
    er_i = []  # permissividade imag
    ur_r = []  # permeabilidade real
    ur_i = []  # permeabilidade imag
    EX = []
    UX = []

    # Vetores - 3
    s11_v = []  # [a.u]

    # Entrada do passo
    inicio = inicio * 1e-3
    fim = fim * 1e-3 + 0.001e-3
    passo = passo * 1e-3

    fig = plt.figure(figsize=(10, 5))

    for d in np.arange(inicio, fim, passo):
        s11_v = []
        F = []
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

            y_value = round(db, 5)

            if y_value < menor_y:
                menor_y = y_value
                curva_menor_y = d
            s11_v.append(y_value)  # dB

        # Dados para serem Plotados
        plt.plot(F, s11_v, label=str(float(d) * 1e3))

        if baixar_grafico:
            contador = 0  # para impressao da matriz de resultados
            matriz = []  # matriz contendo todos rersultados obtidos
            matrizind = []  # cabecalho
            espessura = round(d / 1e-3, 2)
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

    # Plotando grafico
    plt.legend(title="Espessura (mm)")
    plt.xlabel(f"Frequência ({unidade_frequencia})")
    plt.ylabel("Perda por Reflexão (dB)")
    plt.title(f"Arquivo: {nome_arquivo_csv}")

    caminho_imagem = f"./pythonPaginaINPE/static/images/rl_epessura_variavel_{identificador_arquivo}.png"
    fig.savefig(caminho_imagem)

    rota_grafico = "/reflectionlossespvar"
    rota_informacoes = "/informacoes"
    if coaxial:
        rota_grafico = "/rlespvarcoaxial"
        rota_informacoes = "/informacoescoaxial"

    dados_view = {
        "curva_menor_y": curva_menor_y * 1e3,
        "rota_grafico": rota_grafico,
        "rota_informacoes": rota_informacoes,
    }

    return render_template("grafico_espessura_variavel.html", **dados_view)
