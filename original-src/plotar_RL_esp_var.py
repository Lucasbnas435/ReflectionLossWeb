import matplotlib.pyplot as plt
import numpy as np
import base64
import os
import shutil
from io import BytesIO
from gerar_hash import get_hash

def RL_esp_var_plot(csv_filename, txt_filename, undfrequencia, espamostra, inicio, fim, passo, baixar_grafico, hash_arquivo, coaxial=False):
    inicio = float(inicio)
    fim = float(fim)
    passo = float(passo)
    menor_y = 99999999
    curva_menor_y = ""

    arq = open(f'./pythonPaginaINPE/static/files/txt_gerado/{txt_filename}','r')
    ler = arq.readlines()
    arq.close()

    if baixar_grafico:
        try:
            os.mkdir(f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}")
        except:
            shutil.rmtree(f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}")
            os.mkdir(f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}")

    #Ajuste da Referencia de L1 e L2
    d = float(espamostra)*1e-3 #[m] #Espessura da amostra (Livro chama de L)

    #CONSTANTES
    c =2.998e8 #[m/s] #velocidade da Luz no vacuo
    #Vetores - 1
    F=[] #frequencia [Hz] DE CALCULO
    F_grafic=[] #FREQUENCIA PARA PLOTAR EM [GHz]

    #Vetores - 2
    er_r = [] #permissividade real
    er_i = [] #permissividade imag
    ur_r = [] #permeabilidade real
    ur_i = [] #permeabilidade imag
    EX = []
    UX = []

    #Vetores - 3
    s11_v =[] #[a.u]

    # Entrada do passo
    inicio = float(inicio)*1e-3
    fim = float(fim)*1e-3 + 0.001e-3
    passo = float(passo)*1e-3

    fig = plt.figure(figsize=(10, 5))

    for d in np.arange(inicio,fim,passo):
        s11_v =[]
        F= []
        for n in range(0,len(ler)):
            dados = ler[n].split('\t')
            #frequencia
            f = float(dados[0])*1e9
            F.append(f)
            F_grafic.append(f/1e9)
            #Permissividade NRW
            ex = float(dados[1]) + 1j*float(dados[2])
            er_r.append(ex.real)
            er_i.append(ex.imag)
            EX.append(ex)
            #Permeabilidade NRW
            ux = float(dados[3]) + 1j*float(dados[4])
            ur_r.append(ux.real)
            ur_i.append(ux.imag)
            UX.append(ux)
            #*********************Calculo da Refletividade (RL)***************
            #Calcular impedÃ¢ncia de entrada
            z = (50*(UX[n]/EX[n])**(1.0/2.0))*np.tanh(1j*(2*np.pi*d*f/c)*((UX[n]*EX[n])**(1.0/2.0))) #COM TANH
            #Passar para S11(dB)
            db= -20*np.log10(abs((z-50)/(z+50))) #dB #somente para voltagem
            #db = -20*np.log10(abs((z-50)/(z+50))) #dB para potência
            #Passar para Lienar Mag S11 (%)
            #s11_curto = (10.0**((db/10.0))) # a.u
            #s11_v.append(s11_curto*100)# LINEAR
            y_value = round(db,5)

            if y_value < menor_y:
                menor_y = y_value
                curva_menor_y = d
            s11_v.append(round(db,5)) # dB

        #Dados para serem Plotados
        plt.plot(F,s11_v, label = str(float(d)*1e3))

        if baixar_grafico:
            contador = 0 #para impressao da matriz de resultados
            matriz = [] #matriz contendo todos rersultados obtidos
            matrizind  = [] #cabecalho
            espessura = round(d/1e-3,2)
            grav = open(f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}/mm_{espessura}mm.txt",'w')
            titulo = "%4s(%3s)  %s\n"%("Freq",undfrequencia,"RL(dB)")
            grav.write(titulo)

            coluna0 = [] #primeira coluna matriz
            colunan = [] #demais colunas matriz
            for i in range(0,len(F)):
                escrever = "%.2f %.2f\n"%(F[i],s11_v[i])
                grav.write(escrever)
                if contador==0: #insercao primeira coluna matriz
                    coluna0.append(F[i])
                colunan.append(s11_v[i]) #insercao valores matriz

        # Gravando matriz de resultados
            if contador == 0:
                matrizind.append("Freq(%3s)"%undfrequencia)
                matriz.append(coluna0) #insercao primeira coluna matriz
            matrizind.append("%s(mm)"%espessura)
            matriz.append(colunan) #insercao valores matriz
            contador = contador + 1

            grav.close()

#Imprimindo arquivos Todos
    if baixar_grafico:
        arquivo = open(f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}/Todos.txt",'w', encoding='utf-8')
        for i in range(len(matrizind)):
            escrever = "%s "%matrizind[i]
            arquivo.write(escrever)
        arquivo.write("\n")
        for j in range(len(matriz[0])):
            for i in range(len(matriz)):
                escrever = "%.2f "%matriz[i][j]
                arquivo.write(escrever)
            arquivo.write("\n")
        arquivo.close()
        return ""

    #Plotando grafico
    plt.legend(title = 'Espessura (mm)')
    plt.xlabel('Frequência (%s)'%undfrequencia)
    plt.ylabel('Perda por Reflexão (dB)')
    plt.title('Arquivo: ' + csv_filename)

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    if coaxial:
        rota_grafico = "/rlespvarcoaxial"
        rota_informacoes = "/informacoescoaxial"
    else:
        rota_grafico = "/reflectionlossespvar"
        rota_informacoes = "/informacoes"

    html = '<html>' + \
    '<head>' + \
	'<link rel="stylesheet" type="text/css" href="{{ url_for("static", filename="css/styles.css") }}">' + \
	'</head>' + \
	'<body>' + \
	'<header>' + \
    '<b>Analisador de Amostras VNA |</b>' + \
    '<a href="/" class="btn">Home</a>' + \
    '<a href="/arquivoumacamada" class="btn">1 camada</a>' + \
    '<a href="/primeiroarquivoduo" class="btn">2 camadas</a>' + \
    '<a href="/primeiroarquivo" class="btn">3 camadas</a>' + \
    '<a href="/arquivocoaxial" class="btn">Coaxial</a>' + \
    '<a href="/gerarxml" class="btn">Gerar XML</a>' + \
    '<div class="images">' + \
    '<img src="{{ url_for("static", filename="images/logoINPE.png") }}" alt="Logotipo do INPE">' + \
    '<img src="{{ url_for("static", filename="images/logoFATEC.png") }}" alt="Logotipo da FATEC Taubate">' + \
    '</div>' + \
    '</header>' + \
	'<img src=\'data:image/png;base64,{}\'>'.format(encoded) + \
    '<h3>Curva de menor RL: Espessura {{curva_menor_y}} mm</h3>' + \
    f'<form action="{rota_grafico}" method="post">' + \
    '<input type="hidden"name="inicio" value={{val_inicio}}>' + \
    '<input type="hidden" name="fim" value={{val_fim}}>' + \
    '<input type="hidden" name="passo" value={{val_passo}}>' + \
    '<input type="hidden" name="hash_arquivo" value={{hash_arquivo}}>' + \
    '<input type="hidden" name="csv_filename" value={{csv_filename}}>' + \
    '<input type="hidden" name="txt_filename" value={{nome_arquivo_txt}}>' + \
    '<input type="hidden" name="undfrequencia" value={{undfrequencia}}>' + \
    '<input type="hidden" name="espamostra" value={{espamostra}}>' + \
    '<input type="hidden" name="baixar_grafico" value="1">' + \
    '<button type="submit">Baixar dados do gráfico</button>' + \
    '</form>' + \
	f'<form action="{rota_informacoes}" method="post">' + \
	'<input type="hidden" name="hash_arquivo" value={{hash_arquivo}}>' + \
	'<input type="hidden" name="csv_filename" value={{csv_filename}}>' + \
	'<button type="submit">Retornar ao menu</button>' + \
	'</form>' + \
	'<footer>' + \
    '<p>Agradecimento: PIBIC/CNPq processo nº 101700/2024-5 - Instituto Nacional de Pesquisas Espaciais</p>' + \
    '<p>Todos os direitos reservados</p>' + \
    '</footer>' + \
    '</body>' + \
    '</html>'

    complemento_nome_arquivo = get_hash(csv_filename)
    nome_template = f"plot_{hash_arquivo}{complemento_nome_arquivo}.html"

    with open(f'./pythonPaginaINPE/templates/{nome_template}','w') as f:
        f.write(html)

    return [nome_template, curva_menor_y * 1e3]
