import matplotlib.pyplot as plt
import base64
from io import BytesIO
from gerar_hash import get_hash

def plotar_menos_pontos_duascamadas(samples, arquivo_saida_original, hash_arquivo1, divisor_quantidade_pontos):
    e = 1600 // divisor_quantidade_pontos
    caminho_arquivo_gerado = f"./pythonPaginaINPE/static/files/txt_gerado/menos_pontos_{hash_arquivo1}.txt"

    with open(f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo1}/{arquivo_saida_original}", "r") as f, open(caminho_arquivo_gerado, "w") as arqs:
        c = 0

        for _ in range(8):
            f.readline()  # Skip the first eight lines

        while True:
            x = f.readline().strip()
            y = f.readline().strip()
            if not x or not y:
                break
            c += 1
            if c % e == 0:
                arqs.write(f"{x}\n{y}\n")

    # Inicialize listas para armazenar os dados
    x = []
    y = []

# Leitura do arquivo-----------------------------------
    with open(caminho_arquivo_gerado, 'r') as file:
        for line in file:
            # Suponha que cada linha do arquivo tenha dois números separados por espaço----------------------------------
            dados = line.strip().split()
            if len(dados) == 2:
                x.append(float(dados[0]))
                y.append(float(dados[1]))

    fig = plt.figure(figsize=(10, 5))
    plt.plot(x, y, "-o")
    plt.xlabel('Frequência (GHz)')
    plt.ylabel('Refletion Loss (dB)')
    plt.title("Espessura total = %.2fmm" %
            ((samples[0].d+samples[1].d)*1000))

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
    '<form action="/menospontosduas" method="post">' + \
    '<input type="range" id="divisor_quantidade_pontos" name="divisor_quantidade_pontos" min="10" max="800" step="1" value={{divisor_quantidade_pontos}} onchange=submit()>' + \
    '<label for="divisor_quantidade_pontos">Regulagem da quantidade de pontos</label><br>' + \
    '<input type="hidden" name="inicio_slider" value={{inicio_slider}}><br>' + \
	'<input type="hidden" name="fim_slider" value={{fim_slider}}>' + \
	'<input type="hidden" name="hash_arquivo1" value={{hash_arquivo1}}>' + \
    '<input type="hidden" name="hash_arquivo2" value={{hash_arquivo2}}>' + \
    '<input type="hidden" name="csv_filename1" value={{csv_filename1}}>' + \
    '<input type="hidden" name="csv_filename2" value={{csv_filename2}}>' + \
	'<input type="hidden" id="espessura_amostra1" name="espessura_amostra1" value={{espessura_amostra1}}>' + \
    '<input type="hidden" id="espessura_amostra2" name="espessura_amostra2" value={{espessura_amostra2}}>' + \
    '<input type="hidden" name="baixar_grafico" value="0">' + \
    '<input type="hidden" name="menos_pontos" value="1">' + \
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
    '<input type="hidden" name="baixar_grafico" value="0">' + \
    '<input type="hidden" name="menos_pontos" value="0">' + \
    '<button type="submit">Retornar ao gráfico de duas camadas</button>' + \
    '</form>' + \
    '<footer>' + \
    '<p>Agradecimento: PIBIC/CNPq processo nº 101700/2024-5 - Instituto Nacional de Pesquisas Espaciais</p>' + \
    '<p>Todos os direitos reservados</p>' + \
    '</footer>' + \
    '</body>' + \
    '</html>'

    complemento_nome_arquivo = get_hash(hash_arquivo1)
    nome_template = f"plot_{hash_arquivo1}{complemento_nome_arquivo}.html"

    with open(f'./pythonPaginaINPE/templates/{nome_template}','w') as f:
        f.write(html)

    return nome_template
