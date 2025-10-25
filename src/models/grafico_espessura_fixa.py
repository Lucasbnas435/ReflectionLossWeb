import os

import matplotlib.pyplot as plt

from src.models.grafico_reflection_loss import GraficoReflectionLoss


class GraficoEspessuraFixa(GraficoReflectionLoss):
    def __init__(
        self,
        nome_arquivo_csv: str,
        caminho_arquivo_txt: str,
        unidade_frequencia: str,
        identificador_arquivo: str,
        espessura_amostra: float,
    ):
        super().__init__(
            nome_arquivo_csv=nome_arquivo_csv,
            caminho_arquivo_txt=caminho_arquivo_txt,
            unidade_frequencia=unidade_frequencia,
            identificador_arquivo=identificador_arquivo,
        )
        self._espessura_amostra = espessura_amostra

    def plotar_grafico(self) -> dict:
        conteudo_arquivo_txt = self._ler_dados_arquivo_txt()

        frequencias_plotagem, s11_v = self._calcular_rl(
            conteudo_arquivo_txt=conteudo_arquivo_txt,
            espessura_amostra=self._espessura_amostra,
        )

        print("Gerando gráfico de perda por reflexão com espessura fixa.")
        fig = plt.figure(figsize=(10, 5))
        plt.plot(
            frequencias_plotagem, s11_v, label=str(self._espessura_amostra)
        )  # Dados para serem plotados
        plt.legend(title="Espessura (mm)")
        plt.xlabel(f"Frequência ({self._unidade_frequencia})")
        plt.ylabel("Perda por Reflexão (dB)")
        plt.title(f"Arquivo: {self._nome_arquivo_csv}")

        nome_arquivo_imagem = (
            f"rl_epessura_fixa_{self._identificador_arquivo}.png"
        )

        caminho_imagem = f"{os.getenv("STATIC_FOLDER_PATH")}/images/graficos_gerados/{nome_arquivo_imagem}"
        fig.savefig(caminho_imagem)
        print("Gráfico de espessura fixa gerado com sucesso.")

        dados_plotagem = {
            "caminho_imagem": caminho_imagem,
            "nome_arquivo_imagem": nome_arquivo_imagem,
        }
        return dados_plotagem

    def baixar_dados_grafico(self):
        print(
            "Gerando arquivo com dados do gráfico de espessura fixa para download."
        )
        pasta_arquivo = f"{os.getenv("STATIC_FOLDER_PATH")}/files/saidas/saidas_{self._identificador_arquivo}"
        os.makedirs(pasta_arquivo, exist_ok=True)

        caminho_arquivo = (
            f"{pasta_arquivo}/mm_{round(self._espessura_amostra, 2)}mm.txt"
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
                espessura_amostra=self._espessura_amostra,
            )

            for frequencia, rl in zip(frequencias_plotagem, s11_v):
                arquivo_dados_grafico.write(f"\n{frequencia:.6f}\t{rl:.2f}")

        print(
            "Arquivo com dados do gráfico de espessura fixa gerado com sucesso."
        )
        return caminho_arquivo
