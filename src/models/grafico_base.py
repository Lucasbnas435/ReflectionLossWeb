from abc import ABC, abstractmethod
from typing import Any

from src.interfaces.grafico import Grafico


class GraficoBase(Grafico, ABC):
    def __init__(
        self,
        nome_arquivo_csv: str,
        caminho_arquivo_txt: str,
        unidade_frequencia: str,
        identificador_arquivo: str,
    ):
        """
        Construtor da classe abstrata Grafico.

        Args:
            nome_arquivo_csv (str): Nome do arquivo csv que foi enviado pelo usuário.
            caminho_arquivo_txt (str): Caminho do arquivo txt que será lido.
            unidade_frequencia (str): Unidade de medida da frequência.
            identificador_arquivo (str): Identificador único dos arquivos .csv e .txt.
        """
        self._nome_arquivo_csv = nome_arquivo_csv
        self._caminho_arquivo_txt = caminho_arquivo_txt
        self._unidade_frequencia = unidade_frequencia
        self._identificador_arquivo = identificador_arquivo

    def _ler_dados_arquivo(self) -> list[str]:
        """
        Extrai os dados do arquivo .txt gerado com base no arquivo .csv obtido com o Vector Network Analyzer (VNA).

        O arquivo contém os dados da medição realizada, além da Permeabilidade Magnética e
        Permissividade Elétrica por frequência, necessária para o cálculo da Perda por
        Reflexão (Reflection Loss).

        Returns:
            list[str]: Lista em que cada elemento é uma linha do arquivo txt.
        """
        with open(self._caminho_arquivo_txt, "r") as arquivo_txt:
            return arquivo_txt.readlines()

    @abstractmethod
    def plotar_grafico(self) -> dict[str, Any]:
        """Método documentado na interface Grafico."""

    @abstractmethod
    def baixar_dados_grafico(self) -> str:
        """Método documentado na interface Grafico."""
