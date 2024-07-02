import os
import shutil

def baixar_grafico_duascamadas(samples, espamostra, hash_arquivo1, F, F_grafic, S11):
    espessura = float((samples[0].d+samples[1].d)*1000)
    convert_espessura = round(espessura, 2)
    placa = float(espamostra[0])
    convert_placa = round(placa, 6)
    meio = float(espamostra[1])
    convert_meio = round(meio, 6)

    caminho_para_salvar_arquivo = f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo1}"

    try:
        os.mkdir(caminho_para_salvar_arquivo)
    except:
        shutil.rmtree(caminho_para_salvar_arquivo)
        os.mkdir(caminho_para_salvar_arquivo)

    nome_arquivo = f"mm_{espamostra[0] * 1e3}mm_{espamostra[1] * 1e3}mm.txt"

    new = open(f"{caminho_para_salvar_arquivo}/{nome_arquivo}", 'w')
    new.write("Sequência\t" + str(convert_placa) + "\t" + str(convert_meio))
    new.write("\nEspessura(MM)\t" + str(convert_espessura))
    new.write("\nFreq(GHz)\tRL\n")

    for i in range(0, len(F)):
        escrever = "%f \t %f\n" % (float(F_grafic[i]), float(S11[i]))
        new.write(escrever)
    new.close()

    return nome_arquivo
