import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from src.models.grafico_reflection_loss import GraficoReflectionLoss


class GraficoEspessuraVariavel(GraficoReflectionLoss):
    def plotar_grafico(
        self, inicio: float = 1.0, fim: float = 10.0, passo: float = 1.0
    ):
        conteudo_arquivo_txt = self._ler_dados_arquivo()

        fig = plt.figure(figsize=(10, 5))

        menor_rl_global = float("inf")
        espessura_menor_rl = float("inf")

        for espessura in np.arange(inicio, fim, passo):
            espessura = round(espessura, 3)

            frequencias_plotagem, s11_v = self._calcular_rl(
                conteudo_arquivo_txt=conteudo_arquivo_txt,
                espessura_amostra=espessura,
            )

            menor_rl_da_curva = min(s11_v)
            if menor_rl_da_curva < menor_rl_global:
                menor_rl_global = menor_rl_da_curva
                espessura_menor_rl = espessura

            # Dados para serem plotados em uma linha individual
            plt.plot(frequencias_plotagem, s11_v, label=str(espessura))

        # Plotando grafico final com todas as linhas
        plt.legend(title="Espessura (mm)")
        plt.xlabel(f"Frequência ({self._unidade_frequencia})")
        plt.ylabel("Perda por Reflexão (dB)")
        plt.title(f"Arquivo: {self._nome_arquivo_csv}")

        nome_arquivo_imagem = (
            f"rl_epessura_variavel_{self._identificador_arquivo}.png"
        )
        caminho_imagem = f"{os.getenv("STATIC_FOLDER_PATH")}/images/graficos_gerados/{nome_arquivo_imagem}"
        fig.savefig(caminho_imagem)

        dados_plotagem = {
            "espessura_menor_rl": espessura_menor_rl,
            "rota_grafico": "/grafico/rl-espessura-variavel",
            "rota_informacoes": "/informacoes",
            "caminho_imagem": caminho_imagem,
            "nome_arquivo_imagem": nome_arquivo_imagem,
            "timestamp": datetime.now().timestamp(),  # usado para cache busting
        }

        return dados_plotagem
