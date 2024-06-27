import csv

def read_csv(hash_arquivo):
    #LER ARQUIVO CSV PARA CONVERSÃO
    try:
        arq = open(f'./pythonPaginaINPE/static/files/{hash_arquivo}.csv','r')
        ler = arq.readlines()
        arq.close()
    except:
        print("O arquivo enviado nao foi encontrado no servidor")

    #Valores do cabeçalho
    frequenciacorte = ler[7]
    undfrequencia = frequenciacorte[28:31]
    frequenciacorte = float(frequenciacorte[19:28])
    #print('Frequência de Corte: %.2f'%frequenciacorte)
    #print('Unidade Frequência de Corte: ' + undfrequencia)
    compsuporteamostra = ler[8]
    compsuporteamostra = float(compsuporteamostra[22:31])
    #print('Comprimento do suporte da amostra (Offset): %.2f'%compsuporteamostra)
    distamostra = ler[9]
    distamostra = float(distamostra[21:29])
    #print('Distância da amostra: %.2f'%distamostra)
    espamostra = ler[10]
    espamostra = float(espamostra[19:27])
    ifbw = ler[11]
    ifbw = float(ifbw[7:18])
    #print('IFBW: %.2f'%ifbw)
    power = ler[12]
    power = float(power[8:16])
    #print('Power: %.2f'%power)
    freqini = ler[15]
    freqini = float(freqini[0:15])
    freqfinal = ler[1615]
    freqfinal = float(freqfinal[0:15])
    #ESCOLHA A BANDA-------------------
    #print('Frequencia inicial: %.2f'%freqini)
    #print('Frequencia final: %.2f'%freqfinal)
    if freqini>=8 and freqfinal<=12.4:
        nome_banda = "Banda X"
    if freqini>=12.4 and freqfinal<=18:
        nome_banda = "Banda Ku"
    if freqini>=18 and freqfinal<=26:
        nome_banda = "Banda K"
    if freqini>=26 and freqfinal<=40:
        nome_banda = "Banda Ka"
    #Fim Valores do cabeçalho
    txt_filename = f"mm_{hash_arquivo}.txt"

    with open(f'./pythonPaginaINPE/static/files/{hash_arquivo}.csv', 'r') as csv_file:
        with open(f'./pythonPaginaINPE/static/files/txt_gerado/{txt_filename}', 'w') as txt_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                txt_file.write('\t'.join(row) + '\n')

    return [txt_filename, compsuporteamostra, frequenciacorte, distamostra, espamostra, ifbw, power, nome_banda, undfrequencia]
