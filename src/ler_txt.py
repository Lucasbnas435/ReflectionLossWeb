def read_txt(txt_filename):
    try:
        with open(f'./pythonPaginaINPE/static/files/txt_gerado/{txt_filename}', 'r') as arq:
            file_formatt = arq.read()
    except:
        print("Erro ao ler arquivo txt gerado a partir do csv enviado pelo usuario")

    start_file = file_formatt.index('Transmission ')
    end_file = file_formatt.index('frequency(GHz)') + len("frequency(GHz),e',e'',u',u''")

    # Remove o cabecalho usando fatiamento
    file_formatt = file_formatt[:start_file] + file_formatt[end_file:]

    # Remove espacos desnecessarios no ini­cio e no final das linhas
    file_formatt = file_formatt.strip()

    # Salva o texto atualizado em um arquivo ou em uma nova variavel
    with open(f'./pythonPaginaINPE/static/files/txt_gerado/{txt_filename}', 'w') as file:
        file.write(file_formatt)
