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
            arquivo_csv = open(self.__caminho_arquivo_csv, "r")
            conteudo_arquivo_csv = arquivo_csv.readlines()
            arquivo_csv.close()
        except Exception as e:
            print(f"Erro ao ler o arquivo csv: {e}")

        # Valores do cabeçalho
        frequencia_corte = conteudo_arquivo_csv[7]
        unidade_da_frequencia = frequencia_corte[28:31]
        frequencia_corte = float(frequencia_corte[19:28])
        # print('Frequência de Corte: %.2f'%frequencia_corte)
        # print('Unidade Frequência de Corte: ' + unidade_da_frequencia)
        comprimento_suporte_da_amostra = conteudo_arquivo_csv[8]
        comprimento_suporte_da_amostra = float(
            comprimento_suporte_da_amostra[22:31]
        )
        # print('Comprimento do suporte da amostra (Offset): %.2f'%comprimento_suporte_da_amostra)
        distancia_da_amostra = conteudo_arquivo_csv[9]
        distancia_da_amostra = float(distancia_da_amostra[21:29])
        # print('Distância da amostra: %.2f'%distancia_da_amostra)
        espessura_da_amostra = conteudo_arquivo_csv[10]
        espessura_da_amostra = float(espessura_da_amostra[19:27])
        ifbw = conteudo_arquivo_csv[11]
        ifbw = float(ifbw[7:18])
        # print('IFBW: %.2f'%ifbw)
        power = conteudo_arquivo_csv[12]
        power = float(power[8:16])
        # print('Power: %.2f'%power)
        frequencia_inicial = conteudo_arquivo_csv[15]
        frequencia_inicial = float(frequencia_inicial[0:15])
        frequencia_final = conteudo_arquivo_csv[1615]
        frequencia_final = float(frequencia_final[0:15])
        # ESCOLHA A BANDA-------------------
        # print('Frequencia inicial: %.2f'%frequencia_inicial)
        # print('Frequencia final: %.2f'%frequencia_final)
        nome_banda = "Não reconhecida"
        if frequencia_inicial >= 8 and frequencia_final <= 12.4:
            nome_banda = "Banda X"
        if frequencia_inicial >= 12.4 and frequencia_final <= 18:
            nome_banda = "Banda Ku"
        if frequencia_inicial >= 18 and frequencia_final <= 26:
            nome_banda = "Banda K"
        if frequencia_inicial >= 26 and frequencia_final <= 40:
            nome_banda = "Banda Ka"
        # Fim Valores do cabeçalho
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
            comprimento_suporte_da_amostra,
            frequencia_corte,
            distancia_da_amostra,
            espessura_da_amostra,
            ifbw,
            power,
            nome_banda,
            unidade_da_frequencia,
        ]
