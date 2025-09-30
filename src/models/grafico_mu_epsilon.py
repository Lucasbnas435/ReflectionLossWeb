import os

import matplotlib.pyplot as plt
import numpy as np

from src.interfaces.grafico import Grafico


class GraficoMuEpsilon(Grafico):
    def __init__(
        self,
        nome_arquivo_csv: str,
        caminho_arquivo_txt: str,
        unidade_frequencia: str,
        identificador_arquivo: str,
    ):
        self._nome_arquivo_csv = nome_arquivo_csv
        self._caminho_arquivo_txt = caminho_arquivo_txt
        self._unidade_frequencia = unidade_frequencia
        self._identificador_arquivo = identificador_arquivo

    def _ler_dados_arquivo_txt(self) -> tuple:
        try:
            dados = np.loadtxt(self._caminho_arquivo_txt)
        except Exception as e:
            print(f"Erro ao ler arquivo txt para plotar mi e epsilon: {e}")
            raise

        print("Extraindo dados de mi e epsilon")
        frequencia = dados[:, 0]
        epsilon = dados[:, 1]
        epsilon_prime = dados[:, 2]
        mi = dados[:, 3]
        mi_prime = dados[:, 4]

        return frequencia, epsilon, epsilon_prime, mi, mi_prime

    def plotar_grafico(self):
        frequencia, epsilon, epsilon_prime, mi, mi_prime = (
            self._ler_dados_arquivo()
        )

        print("Iniciando plotagem do gráfico de permissividade elétrica")
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 2, 1)
        plt.plot(frequencia, epsilon, label="\u03b5'")
        plt.plot(frequencia, epsilon_prime, label="\u03b5''")
        plt.xlabel(f"Frequência ({self._unidade_frequencia})")
        plt.ylabel("Permissividade Elétrica Relativa (\u03b5\u1d63)")
        plt.title(
            f"Arquivo: {self._nome_arquivo_csv}\nGráfico \u03b5' vs. \u03b5'' em função da Frequência"
        )
        plt.legend()
        plt.grid(True)
        print("Plotagem do gráfio de permissividade elétrica finalizada")

        print("Iniciando plotagem do gráfico de permeabilidade magnética")
        ax = fig.add_subplot(1, 2, 2)
        plt.plot(frequencia, mi, label="\u00b5'")
        plt.plot(frequencia, mi_prime, label="\u00b5''")
        plt.xlabel(f"Frequência ({self._unidade_frequencia})")
        plt.ylabel("Permeabilidade Magnética Relativa (\u00b5\u1d63)")
        plt.title(
            f"Arquivo: {self._nome_arquivo_csv}\nGráfico \u00b5' vs. \u00b5'' em função da Frequência"
        )
        plt.legend()
        plt.grid(True)
        print("Plotagem do gráfico de permeabilidade magnética finalizada")

        nome_arquivo_imagem = f"mi_epsilon_{self._identificador_arquivo}.png"
        caminho_imagem = f"{os.getenv("STATIC_FOLDER_PATH")}/images/graficos_gerados/{nome_arquivo_imagem}"
        fig.savefig(caminho_imagem)

        dados_plotagem = {
            "nome_arquivo_imagem": nome_arquivo_imagem,
        }

        return dados_plotagem
