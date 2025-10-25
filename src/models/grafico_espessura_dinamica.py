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

        print("Gerando gráfico de perda por reflexão com espessura dinâmica.")
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
        print("Gráfico de espessura dinâmica gerado com sucesso.")

        dados_plotagem = {
            "caminho_imagem": caminho_imagem,
            "nome_arquivo_imagem": nome_arquivo_imagem,
            "espessura_amostra": espessura_amostra,
            "timestamp": datetime.now().timestamp(),  # usado para cache busting
            "inicio_slider": inicio_slider,
            "fim_slider": fim_slider,
        }
        return dados_plotagem

    def baixar_dados_grafico(
        self,
        espessura_amostra: float = 1.0,
    ):
        print(
            "Gerando arquivo com dados do gráfico de espessura dinâmica para download."
        )
        pasta_arquivo = f"{os.getenv("STATIC_FOLDER_PATH")}/files/saidas/saidas_{self._identificador_arquivo}"
        os.makedirs(pasta_arquivo, exist_ok=True)

        caminho_arquivo = (
            f"{pasta_arquivo}/mm_{round(espessura_amostra, 2)}mm.txt"
        )

        with open(
            caminho_arquivo,
            "w",
            encoding="utf-8",
        ) as arquivo_dados_grafico:
            # Cabeçalho do arquivo enviado para download
            arquivo_dados_grafico.write(
                f"Frequência({self._unidade_frequencia}) RL(dB)"
            )

            frequencias_plotagem, s11_v = self._calcular_rl(
                conteudo_arquivo_txt=self._ler_dados_arquivo_txt(),
                espessura_amostra=espessura_amostra,
            )

            for frequencia, rl in zip(frequencias_plotagem, s11_v):
                arquivo_dados_grafico.write(f"\n{frequencia:.6f}\t{rl:.2f}")
        print(
            "Arquivo com dados do gráfico de espessura dinâmica gerado com sucesso."
        )
        return caminho_arquivo
