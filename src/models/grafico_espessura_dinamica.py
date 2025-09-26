import os
from datetime import datetime

import matplotlib.pyplot as plt

from src.models.grafico_reflection_loss import GraficoReflectionLoss


class GraficoEspessuraDinamica(GraficoReflectionLoss):
    def plotar_grafico(
        self,
        espessura_amostra: float = 1.0,
        inicio_slider: float = 1.0,
        fim_slider: float = 10.0,
    ):
        conteudo_arquivo_txt = self._ler_dados_arquivo_txt()

        frequencias_plotagem, s11_v = self._calcular_rl(
            conteudo_arquivo_txt=conteudo_arquivo_txt,
            espessura_amostra=espessura_amostra,
        )

        fig = plt.figure(figsize=(10, 5))
        plt.plot(frequencias_plotagem, s11_v, label=str(espessura_amostra))
        plt.legend(title="Espessura (mm)")
        plt.xlabel(f"Frequência ({self._unidade_frequencia})")
        plt.ylabel("Perda por Reflexão (dB)")
        plt.title(f"Arquivo: {self._nome_arquivo_csv}")

        nome_arquivo_imagem = (
            f"rl_epessura_dinamica_{self._identificador_arquivo}.png"
        )

        caminho_imagem = f"{os.getenv("STATIC_FOLDER_PATH")}/images/graficos_gerados/{nome_arquivo_imagem}"
        fig.savefig(caminho_imagem)

        dados_plotagem = {
            "rota_grafico": "/grafico/rl-espessura-dinamica",
            "rota_informacoes": "/informacoes",
            "caminho_imagem": caminho_imagem,
            "nome_arquivo_imagem": nome_arquivo_imagem,
            "espessura_amostra": espessura_amostra,
            "timestamp": datetime.now().timestamp(),  # usado para cache busting
            "inicio_slider": inicio_slider,
            "fim_slider": fim_slider,
        }

        return dados_plotagem
