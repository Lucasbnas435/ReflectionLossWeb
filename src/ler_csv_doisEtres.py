import csv

def read_csv_duas_tres_camadas(*nome_hash_arquivo):
    #Cuidado com a Sequencia das amostras: a amostra encostada na placa deve ser a PRIMEIRA (índice = 0)
    arq_csv = [f"{hash_arquivo}.csv" for hash_arquivo in nome_hash_arquivo]
    espamostra = [] #lista para armazenar as espessuras associadas aos nomes de arquivo
    for csv_file_name in arq_csv:
        with open(f"./pythonPaginaINPE/static/files/{csv_file_name}", 'r') as csv_file:
            arq = open(f"./pythonPaginaINPE/static/files/{csv_file_name}", 'r')
            ler = arq.readlines()
            espessura = float(ler[10][19:27]) * 1e-3
            espamostra.append(espessura) #Armazenar as espessuras numa lista

            txt_file_name = f"{csv_file_name[:-4]}.txt"
            with open(f"./pythonPaginaINPE/static/files/txt_gerado/{txt_file_name}", 'w') as txt_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    txt_file.write(',\t'.join(row) + '\n')

    return espamostra
