import csv


class DadosVna:
    """
    Classe para representar os dados extraídos por um VNA (Vector Network Analyzer).
    """

    def __init__(self, hash_arquivo: str):
        self.__hash_arquivo = hash_arquivo
        self.__caminho_arquivo_csv = (
            f"./pythonPaginaINPE/static/files/{hash_arquivo}.csv"
        )

    def ler_csv(self):
        try:
            with open(self.__caminho_arquivo_csv, "r") as arquivo_csv:
                conteudo_arquivo_csv = arquivo_csv.readlines()
        except Exception as e:
            print(f"Erro ao ler o arquivo csv: {e}")

        frequencia_corte = float(conteudo_arquivo_csv[7][19:28])
        unidade_frequencia = conteudo_arquivo_csv[7][28:31]

        # Comprimento do suporte da amostra = Offset da amostra
        comprimento_suporte_amostra = float(conteudo_arquivo_csv[8][22:31])
        distancia_amostra = float(conteudo_arquivo_csv[9][21:29])
        espessura_amostra = float(conteudo_arquivo_csv[10][19:27])
        ifbw = float(conteudo_arquivo_csv[11][7:18])
        power = float(conteudo_arquivo_csv[12][8:16])
        frequencia_inicial = float(conteudo_arquivo_csv[15][:15])
        frequencia_final = float(conteudo_arquivo_csv[1615][0:15])

        nome_banda = "Não reconhecida"
        if frequencia_inicial >= 8 and frequencia_final <= 12.4:
            nome_banda = "Banda X"
        if frequencia_inicial >= 12.4 and frequencia_final <= 18:
            nome_banda = "Banda Ku"
        if frequencia_inicial >= 18 and frequencia_final <= 26:
            nome_banda = "Banda K"
        if frequencia_inicial >= 26 and frequencia_final <= 40:
            nome_banda = "Banda Ka"

        txt_filename = f"mm_{self.__hash_arquivo}.txt"

        with open(
            f"./pythonPaginaINPE/static/files/{self.__hash_arquivo}.csv", "r"
        ) as csv_file:
            with open(
                f"./pythonPaginaINPE/static/files/txt_gerado/{txt_filename}",
                "w",
            ) as txt_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    txt_file.write("\t".join(row) + "\n")

        return [
            txt_filename,
            comprimento_suporte_amostra,
            frequencia_corte,
            distancia_amostra,
            espessura_amostra,
            ifbw,
            power,
            nome_banda,
            unidade_frequencia,
        ]

    def gerar_arquivo_txt(self):
        pass
