import numpy as np


def calcular_rl(conteudo_arquivo_txt: list[str], espessura_amostra: float):
    # Ajuste da Referencia de L1 e L2
    # [m] Espessura da amostra (Livro chama de L)
    d = espessura_amostra * 1e-3

    # CONSTANTES
    C = 2.998e8  # [m/s] #velocidade da Luz no vacuo

    # Vetores - 1
    frequencias = []  # frequencia [Hz] DE CALCULO
    F_grafic = []  # FREQUENCIA PARA PLOTAR EM [GHz]

    # Vetores - 2
    er_r = []  # permissividade elétrica real
    er_i = []  # permissividade elétrica imaginaria
    ur_r = []  # permeabilidade magnética real
    ur_i = []  # permeabilidade magnética imaginaria

    permissividade_eletrica = []
    permeabilidade_magnetica = []

    # Vetores - 3
    s11_v = []  # [a.u]

    for n, linha in enumerate(conteudo_arquivo_txt):
        dados = linha.split("\t")
        # frequencia
        f = float(dados[0]) * 1e9
        frequencias.append(f)
        F_grafic.append(f / 1e9)

        # Permissividade NRW
        ex = float(dados[1]) + 1j * float(dados[2])
        er_r.append(ex.real)
        er_i.append(ex.imag)
        permissividade_eletrica.append(ex)

        # Permeabilidade NRW
        ux = float(dados[3]) + 1j * float(dados[4])
        ur_r.append(ux.real)
        ur_i.append(ux.imag)
        permeabilidade_magnetica.append(ux)

        # *********************Calculo da Refletividade (RL)***************
        # Calcular impedância de entrada
        z = (
            50
            * (permeabilidade_magnetica[n] / permissividade_eletrica[n])
            ** (1.0 / 2.0)
        ) * np.tanh(
            1j
            * (2 * np.pi * d * f / C)
            * (
                (permeabilidade_magnetica[n] * permissividade_eletrica[n])
                ** (1.0 / 2.0)
            )
        )
        db = -20 * np.log10(
            abs((z - 50) / (z + 50))
        )  # [dB] somente para voltagem
        s11_v.append(round(db, 5))
