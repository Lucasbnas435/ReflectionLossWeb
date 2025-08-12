import csv
import os


class DadosVna:
    """
    Classe para representar os dados extraídos por um VNA (Vector Network Analyzer).
    """

    def __init__(self, identificador_arquivo: str):
        self.__identificador_arquivo = identificador_arquivo
        self.__caminho_arquivo_csv = f"{os.getenv("STATIC_FOLDER_PATH")}/files/csv_enviado/{self.__identificador_arquivo}.csv"
        self.__caminho_arquivo_txt = f"{os.getenv("STATIC_FOLDER_PATH")}/files/txt_gerado/mm_{self.__identificador_arquivo}.txt"

    @property
    def identificador_arquivo(self):
        return self.__identificador_arquivo

    @property
    def caminho_arquivo_csv(self):
        return self.__caminho_arquivo_csv

    @property
    def caminho_arquivo_txt(self):
        return self.__caminho_arquivo_txt

    @property
    def frequencia_corte(self):
        return self.__frequencia_corte

    @property
    def unidade_frequencia(self):
        return self.__unidade_frequencia

    @property
    def comprimento_suporte_amostra(self):
        return self.__comprimento_suporte_amostra

    @property
    def distancia_amostra(self):
        return self.__distancia_amostra

    @property
    def espessura_amostra(self):
        return self.__espessura_amostra

    @property
    def ifbw(self):
        return self.__ifbw

    @property
    def power(self):
        return self.__power

    @property
    def nome_banda(self):
        return self.__nome_banda

    def ler_csv(self):
        try:
            with open(self.__caminho_arquivo_csv, "r") as arquivo_csv:
                conteudo_arquivo_csv = arquivo_csv.readlines()
        except Exception as e:
            print(f"Erro ao ler o arquivo csv: {e}")

        self.__frequencia_corte = float(conteudo_arquivo_csv[7][19:28])
        self.__unidade_frequencia = conteudo_arquivo_csv[7][28:31]

        # Comprimento do suporte da amostra = Offset da amostra
        self.__comprimento_suporte_amostra = float(
            conteudo_arquivo_csv[8][22:31]
        )
        self.__distancia_amostra = float(conteudo_arquivo_csv[9][21:29])
        self.__espessura_amostra = float(conteudo_arquivo_csv[10][19:27])
        self.__ifbw = float(conteudo_arquivo_csv[11][7:18])
        self.__power = float(conteudo_arquivo_csv[12][8:16])
        self.__frequencia_inicial = float(conteudo_arquivo_csv[15][:15])
        self.__frequencia_final = float(conteudo_arquivo_csv[1615][0:15])

        self.__nome_banda = "Não reconhecida"
        if self.__frequencia_inicial >= 8 and self.__frequencia_final <= 12.4:
            self.__nome_banda = "Banda X"
        if self.__frequencia_inicial >= 12.4 and self.__frequencia_final <= 18:
            self.__nome_banda = "Banda Ku"
        if self.__frequencia_inicial >= 18 and self.__frequencia_final <= 26:
            self.__nome_banda = "Banda K"
        if self.__frequencia_inicial >= 26 and self.__frequencia_final <= 40:
            self.__nome_banda = "Banda Ka"

    def gerar_arquivo_txt(self):
        with open(self.__caminho_arquivo_csv, "r") as csv_file:
            with open(
                self.__caminho_arquivo_txt,
                "w",
            ) as txt_file:
                conteudo_csv = csv.reader(csv_file)

                # Pula as 15 primeiras linhas, que são o cabeçalho do arquivo
                for _ in range(15):
                    next(conteudo_csv)

                linhas_conteudo_csv = list(conteudo_csv)

                # Formata o conteudo do arquivo csv e escreve no txt
                for row in linhas_conteudo_csv[:-1]:
                    txt_file.write("\t".join(row).strip() + "\n")
