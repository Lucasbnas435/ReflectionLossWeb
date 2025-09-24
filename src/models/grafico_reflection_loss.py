from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from src.models.grafico_base import GraficoBase


class GraficoReflectionLoss(GraficoBase, ABC):
    def calcular_rl(
        self, conteudo_arquivo_txt: list[str], espessura_amostra: float
    ) -> tuple[list[float], list[float]]:
        # Ajuste da Referencia de L1 e L2
        # [m] Espessura da amostra (Livro chama de L)
        d = espessura_amostra * 1e-3

        # CONSTANTES
        C = 2.998e8  # [m/s] #velocidade da Luz no vacuo

        # Vetores - 1
        frequencias_plotagem = []  # frequencias para plotar o gráfico [GHz]

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
            frequencia_ghz = float(dados[0])
            frequencias_plotagem.append(frequencia_ghz)
            frequencia_hz = frequencia_ghz * 1e9

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
                * (2 * np.pi * d * frequencia_hz / C)
                * (
                    (permeabilidade_magnetica[n] * permissividade_eletrica[n])
                    ** (1.0 / 2.0)
                )
            )
            db = -20 * np.log10(
                abs((z - 50) / (z + 50))
            )  # [dB] somente para voltagem
            s11_v.append(round(db, 5))

        return frequencias_plotagem, s11_v

    @abstractmethod
    def plotar_grafico(self) -> dict[str, Any]:
        """Método obrigatório, conforme definido em GraficoBase."""

    @abstractmethod
    def baixar_dados_grafico(self) -> str:
        """Método obrigatório, conforme definido em GraficoBase."""
