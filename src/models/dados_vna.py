import csv


class DadosVna:
    """
    Classe para representar os dados extraídos por um VNA (Vector Network Analyzer).
    """

    def __init__(self, hash_arquivo: str):
        self.__hash_arquivo = hash_arquivo
        self.__caminho_arquivo_csv = (
            f"./pythonPaginaINPE/static/files/{self.__hash_arquivo}.csv"
        )
        self.__caminho_arquivo_txt = f"./pythonPaginaINPE/static/files/txt_gerado/mm_{self.__hash_arquivo}.txt"

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
                for row in conteudo_csv:
                    txt_file.write("\t".join(row) + "\n")
