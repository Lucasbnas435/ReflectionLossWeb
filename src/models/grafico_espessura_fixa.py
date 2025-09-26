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

        rota_grafico = "/grafico/rl-espessura-fixa"
        rota_informacoes = "/informacoes"

        dados_plotagem = {
            "rota_grafico": rota_grafico,
            "rota_informacoes": rota_informacoes,
            "caminho_imagem": caminho_imagem,
            "nome_arquivo_imagem": nome_arquivo_imagem,
        }

        return dados_plotagem
