import csv

def read_csv_coaxial(hash_arquivo):
    #LER ARQUIVO CSV PARA CONVERSÃO
    try:
        arq = open(f'./pythonPaginaINPE/static/files/{hash_arquivo}.csv','r')
        ler = arq.readlines()
        arq.close()
    except:
        print("O arquivo enviado nao foi encontrado no servidor")

    #Valores do cabeçalho
    espamostra = ler[9]
    espamostra = float(espamostra[19:27])
    cabecalho = ler[13]
    undfrequencia = cabecalho[10:13]
    freqini = ler[14]
    freqini = float(freqini[0:15])
    freqfinal = ler[1614]
    freqfinal = float(freqfinal[0:14])

    #Fim Valores do cabeçalho
    txt_filename = f"mm_{hash_arquivo}.txt"

    with open(f'./pythonPaginaINPE/static/files/{hash_arquivo}.csv', 'r') as csv_file:
        with open(f'./pythonPaginaINPE/static/files/txt_gerado/{txt_filename}', 'w') as txt_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                txt_file.write('\t'.join(row) + '\n')

    return [txt_filename, espamostra, undfrequencia]
