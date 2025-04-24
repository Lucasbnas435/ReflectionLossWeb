import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from baixar_grafico_duo import baixar_grafico_duascamadas
from menos_pontos_duo import plotar_menos_pontos_duascamadas
from gerar_hash import get_hash

class Amostra:
    def __init__(self, nome, er, ei, ur, ui, d, zin):
        self.nome = nome  # nome arquivo
        self.er = er
        self.ei = ei
        self.ur = ur
        self.ui = ui
        self.d = d  # Espessura
        self.zin = zin  # impedância

#espamostra deve ser tratado no main.py, de forma que a espessura correspondente a cada chave seja coletada da barra HTML e enviada na requisicao
def duascamadas_plot(hash_arquivo1, hash_arquivo2, espamostra, csv_filename1, csv_filename2, baixar_grafico, menos_pontos, divisor_quantidade_pontos=25):
    #Cuidado com a Sequência das amostras: a amostra encostada na placa deve ser a PRIMEIRA (índice = 0)
    TXT = [f"{hash_arquivo1}.txt", f"{hash_arquivo2}.txt"]

    # Criando os Objetos e Colocando-os dentro de um Array
    samples = []
    i = 0
    for arquivo in TXT:
        # Obtendo a espessura correspondente ao nome do arquivo do dicionário espamostra
        #D = espamostra.get(arquivo.replace('.txt', '.csv'), 0) * 1e-3
        espessura = espamostra[i]
        i += 1
        samples.append(Amostra(arquivo[:-4], [], [], [], [], espessura, []))

    # ------------------Parâmetros do Guia-------------
    #espessura = 0.0
    c = 2.998e8  # [m/s] Velocidade da luz

    # # Organizar Dados $\epsilon$ e $\mu$
    F = []  # frequencia [Hz] DE CALCULO
    F_grafic = []  # FREQUENCIA PARA PLOTAR EM [GHz]

    ler1_col = 1  # er
    ler2_col = 2  # ei
    ler3_col = 3  # ur
    ler4_col = 4  # ui

    #Abrindo o Arquivo e colocando os dados dentro dos OBJETOS
    #CUIDADO COM A FREQUÊNCIA!!!! ALGUNS ARQUIVOS JÁ VEM EM GHz
    try:
        for n in range(0, len(TXT)):
            arq = open(f"./pythonPaginaINPE/static/files/txt_gerado/{TXT[n]}", 'r')
            ler = arq.readlines()
            arq.close()

            er = []
            ei = []
            ur = []
            ui = []

            for i in range(15, len(ler)-1):
                dados = ler[i].split(',')

                if n == 0:
                    # Frequência
                    f = float(dados[0])*1e9
                    # f = float(dados[0])
                    F.append(f)
                    F_grafic.append(f/1e9)

                # e and u
                er.append(float(dados[ler1_col]))  # real
                ei.append(float(dados[ler2_col]))  # imag
                ur.append(float(dados[ler3_col]))  # real
                ui.append(float(dados[ler4_col]))  # imag

            samples[n].er = er
            samples[n].ei = ei
            samples[n].ur = ur
            samples[n].ui = ui
    except FileNotFoundError:
        pass

    S11 = []
    i = 0

    for n in range(0, len(samples)):
        while i < 1601:
            f = F[i]

            e1 = samples[n].er[i] - 1j*samples[n].ei[i]
            u1 = samples[n].ur[i] - 1j*samples[n].ui[i]
            d1 = samples[n].d
            # Impedância caracteristica (n)
            # 50 Ohm do cabo/guia
            zo = 50
            zn1 = zo*(u1/e1)**0.5

            e2 = samples[n+1].er[i] - 1j*samples[n+1].ei[i]
            u2 = samples[n+1].ur[i] - 1j*samples[n+1].ui[i]
            d2 = samples[n+1].d
            zn2 = zo*(u2/e2)**0.5

            # Cálculo
            zin1 = zn1*np.tanh((2j*np.pi*d1*f/c)*((u1*e1)**(1.0/2.0)))
            zin2 = zn2*(zin1 + zn2*np.tanh(2j*np.pi*f*d2/c*np.sqrt(u2*e2))) / \
                (zn2 + zin1*np.tanh(2j*np.pi*f*d2/c*np.sqrt(u2*e2)))

            # DE LINEAR MAG PARA DB...
            # Coeficiente de Reflexão
            r = (zin2-zo)/(zin2+zo)
            # Linear Mag
            s11 = abs(r)
            # Log Mag
            db = 20*np.log10(s11)

            S11.append(db)

            i += 1

        break

    if baixar_grafico:
        filename = baixar_grafico_duascamadas(samples, espamostra, hash_arquivo1, F, F_grafic, S11)
        return filename
    elif menos_pontos:
        filename = baixar_grafico_duascamadas(samples, espamostra, hash_arquivo1, F, F_grafic, S11)
        template_name = plotar_menos_pontos_duascamadas(samples, filename, hash_arquivo1, divisor_quantidade_pontos)
        return template_name

    # ------------------------GRAFICO 1 - Reflection Loss (RL)-----------------------
    fig = plt.figure(figsize=(10, 5))
    plt.plot(F_grafic, S11, 'r-', label="Espessura total = %.2f mm" % ((samples[0].d+samples[1].d)*1000), alpha=0.4)
    plt.title(f"Camadas: {csv_filename1} + {csv_filename2} + Placa")
    plt.xlabel('Frequency(GHz)')
    plt.ylabel("Reflection Loss (dB)")
    plt.legend()
    plt.grid(True)

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

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
	'<form action="/duascamadas" method="post">' + \
	'Espessura mínima em mm: <input type="number" name="inicio_slider" step="any" value={{inicio_slider}} required="true"><br>' + \
	'Espessura máxima em mm: <input type="number" name="fim_slider" step="any" value={{fim_slider}} required="true"><br>' + \
	'<input type="hidden" name="hash_arquivo1" value={{hash_arquivo1}}>' + \
    '<input type="hidden" name="hash_arquivo2" value={{hash_arquivo2}}>' + \
    '<input type="hidden" name="csv_filename1" value={{csv_filename1}}>' + \
    '<input type="hidden" name="csv_filename2" value={{csv_filename2}}>' + \
    '<input type="hidden" name="baixar_grafico" value="0">' + \
    '<input type="hidden" name="menos_pontos" value="0">' + \
	'<input type="range" id="espessura_amostra1" name="espessura_amostra1" min={{inicio_slider * 1e-3}} max={{fim_slider * 1e-3}} step="0.000001" value={{espessura_amostra1}} onchange=submit()>' + \
    '<label for="espessura_amostra1">Espessura 1: {{espessura_amostra1}} m</label><br>' + \
    '<input type="range" id="espessura_amostra2" name="espessura_amostra2" min={{inicio_slider * 1e-3}} max={{fim_slider * 1e-3}} step="0.000001" value={{espessura_amostra2}} onchange=submit()>' + \
    '<label for="espessura_amostra2">Espessura 2: {{espessura_amostra2}} m</label><br>' + \
	'</form>' + \
    '<form action="/duascamadas" method="post">' + \
    '<input type="hidden" name="inicio_slider" value={{inicio_slider}}>' + \
	'<input type="hidden" name="fim_slider" value={{fim_slider}}>' + \
	'<input type="hidden" name="hash_arquivo1" value={{hash_arquivo1}}>' + \
    '<input type="hidden" name="hash_arquivo2" value={{hash_arquivo2}}>' + \
    '<input type="hidden" name="csv_filename1" value={{csv_filename1}}>' + \
    '<input type="hidden" name="csv_filename2" value={{csv_filename2}}>' + \
	'<input type="hidden" id="espessura_amostra1" name="espessura_amostra1" value={{espessura_amostra1}}>' + \
    '<input type="hidden" id="espessura_amostra2" name="espessura_amostra2" value={{espessura_amostra2}}>' + \
    '<input type="hidden" name="baixar_grafico" value="1">' + \
    '<input type="hidden" name="menos_pontos" value="0">' + \
    '<button type="submit">Baixar dados do gráfico</button>' + \
    '</form>' + \
    '<form action="/menospontosduas" method="post">' + \
    '<input type="hidden" name="inicio_slider" value={{inicio_slider}}>' + \
	'<input type="hidden" name="fim_slider" value={{fim_slider}}>' + \
	'<input type="hidden" name="hash_arquivo1" value={{hash_arquivo1}}>' + \
    '<input type="hidden" name="hash_arquivo2" value={{hash_arquivo2}}>' + \
    '<input type="hidden" name="csv_filename1" value={{csv_filename1}}>' + \
    '<input type="hidden" name="csv_filename2" value={{csv_filename2}}>' + \
	'<input type="hidden" id="espessura_amostra1" name="espessura_amostra1" value={{espessura_amostra1}}>' + \
    '<input type="hidden" id="espessura_amostra2" name="espessura_amostra2" value={{espessura_amostra2}}>' + \
    '<input type="hidden" name="baixar_grafico" value="0">' + \
    '<input type="hidden" name="menos_pontos" value="1">' + \
    '<input type="hidden" name="divisor_quantidade_pontos" value="25">' + \
    '<button type="submit">Exibir gráfico com menos pontos</button>' + \
    '</form>' + \
    '<footer>' + \
    '<p>Agradecimento: PIBIC/CNPq processo nº 101700/2024-5 - Instituto Nacional de Pesquisas Espaciais</p>' + \
    '<p>Todos os direitos reservados</p>' + \
    '</footer>' + \
    '</body>' + \
    '</html>'

    complemento_nome_arquivo = get_hash(csv_filename1)
    nome_template = f"plot_{hash_arquivo1}{complemento_nome_arquivo}.html"

    with open(f'./pythonPaginaINPE/templates/{nome_template}','w') as f:
        f.write(html)

    return nome_template
