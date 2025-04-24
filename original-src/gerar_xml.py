import numpy as np
import csv
from datetime import date

def generate_xml_file_from_csv(hash_arquivo, csv_filename):
    csv_file_path = f'./pythonPaginaINPE/static/files/{hash_arquivo}.csv'
    txt_file_path = f'./pythonPaginaINPE/static/files/mm_{hash_arquivo}.txt'
    xml_file_path = f'./pythonPaginaINPE/static/files/saidas/{hash_arquivo}.xml'

    arq = open(csv_file_path,'r')
    ler = arq.readlines()
    arq.close()

    with open(csv_file_path, 'r') as csv_file:
    	with open(txt_file_path, 'w') as txt_file:
    		csv_reader = csv.reader(csv_file)
    		for row in csv_reader:
    			txt_file.write('\t'.join(row) + '\n')

    with open(txt_file_path, 'r') as arq:
    	file_formatt = arq.read()

    start_file = file_formatt.index('Transmission ')
    end_file = file_formatt.index('frequency(GHz)') + len("frequency(GHz),e',e'',u',u''")

    # Remove o cabecalho usando fatiamento
    file_formatt = file_formatt[:start_file] + file_formatt[end_file:]

    # Remove espacos desnecessrios no inicio e no final das linhas
    file_formatt = file_formatt.strip()

    # Salva o texto atualizado em um arquivo ou em uma nova variavel
    with open(txt_file_path, 'w') as file:
    	file.write(file_formatt)
    arq = open(txt_file_path,'r')
    ler = arq.readlines()
    arq.close()

    # FIM DA CONVERSAO EM TXT
    # Le o arquivo de texto e armazena os dados em arrays
    dados = np.loadtxt(txt_file_path)

    # Extrai as colunas
    frequencia = dados[:, 0]
    e = dados[:, 1]
    e_prime = dados[:, 2]
    u = dados[:, 3]
    u_prime = dados[:, 4]

    #Cria arquivo xml equivalente
    nomearqxml = f"{csv_filename}.xml"
    arquivo = open(xml_file_path,'w', encoding='utf-8')

    arquivo.write("<?xml version='1.0' encoding='UTF-8'?>")
    arquivo.write('\n')
    data = str(date.today())
    arquivo.write('<materialDB creator="Lab_Baldan" date="'+data+'" version="1.0">')
    arquivo.write('\n')
    arquivo.write(' <material name="'+nomearqxml[:-4]+'">')
    arquivo.write('\n')

    for n in range(0,len(ler)):
    	freq = str( round(frequencia[n],4) )
    	el = str( round(e[n],4) )
    	ell = str( round(u[n],4) )
    	dlt = str( round(e_prime[n]/e[n],4) )
    	mlt = str( round(u_prime[n]/u[n],4) )
    	arquivo.write('<dataPoint freq="'+freq+'e9" permittivity="'+el+'" permeability="'+ell+'" diel_loss_tangent="'+dlt+'" mag_loss_tangent="'+mlt+'" />')
    	arquivo.write('\n')

    arquivo.write(' </material>')
    arquivo.write('\n')
    arquivo.write(' </materialDB>')
    arquivo.write('\n')
    arquivo.close()
