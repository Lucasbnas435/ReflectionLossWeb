import os
import shutil
import matplotlib.pyplot as plt
import numpy as np

def plotar_rl_dinamico(
    nome_arquivo_csv: str,
    caminho_arquivo_txt: str,
    unidade_frequencia: str,
    identificador_arquivo: str,
    espessura_amostra: float,
    baixar_grafico: bool,
    coaxial: bool = False,
):
    arq = open(
        f"./pythonPaginaINPE/static/files/txt_gerado/{caminho_arquivo_txt}", "r"
    )
    ler = arq.readlines()
    arq.close()

    # Ajuste da Referencia de L1 e L2
    d = float(espessura_amostra)  # [m] #Espessura da amostra (Livro chama de L)

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

    for n in range(0, len(ler)):
        dados = ler[n].split("\t")
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
        # Calcular impedÃ¢ncia de entrada
        z = (50 * (UX[n] / EX[n]) ** (1.0 / 2.0)) * np.tanh(
            1j * (2 * np.pi * d * f / c) * ((UX[n] * EX[n]) ** (1.0 / 2.0))
        )  # COM TANH
        # Passar para S11(dB)
        db = -20 * np.log10(
            abs((z - 50) / (z + 50))
        )  # dB #somente para voltagem
        # db = -20*np.log10(abs((z-50)/(z+50))) #dB para potência
        # Passar para Lienar Mag S11 (%)
        # s11_curto = (10.0**((db/10.0))) # a.u
        # s11_v.append(s11_curto*100)# LINEAR
        s11_v.append(round(db, 5))  # dB

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

    fig = plt.figure(figsize=(10, 5))
    # Dados para serem Plotados
    plt.plot(F, s11_v, label=str(float(d) * 1e3))

    # Plotando grafico
    plt.xlabel(f"Frequência ({unidade_frequencia})")
    plt.ylabel("Perda por Reflexão (dB)")
    plt.title("Arquivo: " + nome_arquivo_csv)

    caminho_imagem = (
        f"./pythonPaginaINPE/static/images/rl_epessura_dinamica_{identificador_arquivo}.png"
    )
    fig.savefig(caminho_imagem)

	rota_grafico = "/reflectionlossdinamico"
	rota_informacoes = "/informacoes"
    if coaxial:
        rota_grafico = "/rldinamicocoaxial"
        rota_informacoes = "/informacoescoaxial"

    complemento_nome_arquivo = get_hash(nome_arquivo_csv)
    nome_template = f"plot_{identificador_arquivo}{complemento_nome_arquivo}.html"

    return nome_template
