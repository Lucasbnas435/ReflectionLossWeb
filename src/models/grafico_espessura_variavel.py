import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from src.models.grafico_reflection_loss import GraficoReflectionLoss


class GraficoEspessuraVariavel(GraficoReflectionLoss):
    def plotar_grafico(
        self, inicio: float = 1.0, fim: float = 10.0, passo: float = 1.0
    ):
        conteudo_arquivo_txt = self._ler_dados_arquivo_txt()

        print("Gerando gráfico de perda por reflexão com espessura variável.")
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
        print("Gráfico de espessura variável gerado com sucesso.")

        dados_plotagem = {
            "espessura_menor_rl": espessura_menor_rl,
            "caminho_imagem": caminho_imagem,
            "nome_arquivo_imagem": nome_arquivo_imagem,
            "timestamp": datetime.now().timestamp(),  # usado para cache busting
        }
        return dados_plotagem

    def baixar_dados_grafico(
        self,
        inicio: float = 1.0,
        fim: float = 10.0,
        passo: float = 1.0,
    ):
        print(
            "Gerando arquivo com dados do gráfico de espessura variável para download."
        )
        pasta_arquivos_saida = f"{os.getenv("STATIC_FOLDER_PATH")}/files/saidas/saidas_{self._identificador_arquivo}"
        os.makedirs(pasta_arquivos_saida, exist_ok=True)

        frequencias_agrupamento = (
            list()
        )  # armazena as frequencias (valores x) do gráfico para gerar arquivo único
        s11_v_agrupadas = []  # armazena todos os valores de RL do gráfico

        for espessura in np.arange(inicio, fim, passo):
            espessura = round(espessura, 3)
            # Criando arquivo individual para cada espessura
            with open(
                f"{pasta_arquivos_saida}/mm_{espessura}mm.txt",
                "w",
                encoding="utf-8",
            ) as arquivo_grafico_individual:
                # Cabeçalho do arquivo enviado para download
                arquivo_grafico_individual.write(
                    f"Frequência({self._unidade_frequencia}) RL(dB)"
                )

                frequencias_plotagem, s11_v = self._calcular_rl(
                    conteudo_arquivo_txt=self._ler_dados_arquivo_txt(),
                    espessura_amostra=espessura,
                )

                # Salva dados para arquivo com todas as espessuras
                frequencias_agrupamento = frequencias_plotagem
                s11_v_agrupadas.append(s11_v)

                # Grava dados no arquivo individual
                for frequencia, rl in zip(frequencias_plotagem, s11_v):
                    arquivo_grafico_individual.write(
                        f"\n{frequencia:.6f}\t{rl:.2f}"
                    )

        dados_grafico_agrupado = [frequencias_agrupamento] + s11_v_agrupadas

        # Criando arquivo único com todas as espessuras
        with open(
            f"{pasta_arquivos_saida}/todos.txt",
            "w",
            encoding="utf-8",
        ) as arquivo_grafico_agrupado:
            for linha in zip(*dados_grafico_agrupado):
                valores = (float(valor) for valor in linha)
                arquivo_grafico_agrupado.write(
                    "  ".join(f"{v:.6f}" for v in valores) + "\n"
                )

        print(
            "Arquivo com dados do gráfico de espessura variável gerado com sucesso."
        )
        return pasta_arquivos_saida
