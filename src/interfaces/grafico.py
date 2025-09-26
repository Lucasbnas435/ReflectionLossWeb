from abc import ABC, abstractmethod
from typing import Any


class Grafico(ABC):
    """
    Interface para as classes responsáveis pela criação de gráficos a partir dos dados extraídos de arquivos .txt.
    """

    @abstractmethod
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

    @abstractmethod
    def _ler_dados_arquivo(self) -> list[str] | tuple:
        """
        Extrai os dados do arquivo .txt gerado com base no arquivo .csv obtido com o Vector Network Analyzer (VNA).

        O arquivo contém os dados da medição realizada, além da Permeabilidade Magnética e
        Permissividade Elétrica por frequência, necessária para o cálculo da Perda por
        Reflexão (Reflection Loss).

        Returns:
            list[str] | tuple: Lista em que cada elemento é uma linha do arquivo txt ou
                tupla com múltiplas listas com conteúdo do arquivo txt.
        """

    @abstractmethod
    def plotar_grafico(
        self,
    ) -> dict[str, Any]:
        """
        Plota o gráfico referente à amostra analisada pelo usuário e obtém os dados necessários para renderizá-lo.

        Returns:
            dict[str, Any]: Dicionário contendo os dados necessários para renderizar o gráfico.
        """

    @abstractmethod
    def baixar_dados_grafico(self) -> str:
        """
        Gera um arquivo .txt para download contendo os dados apresentados no gráfico.

        Returns:
            str: Caminho do arquivo .txt gerado.
        """
