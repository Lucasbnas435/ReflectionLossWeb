import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def mi_epsilon_plot(hash_arquivo, csv_filename, undfrequencia, coaxial=False):
    try:
        dados = np.loadtxt(f'./pythonPaginaINPE/static/files/txt_gerado/mm_{hash_arquivo}.txt')
    except:
        print("O arquivo txt nao foi recuperado ao plotar o grafico de mi e epsilon")

    # Extrai as colunas
    frequencia = dados[:, 0]
    e = dados[:, 1]
    e_prime = dados[:, 2]
    u = dados[:, 3]
    u_prime = dados[:, 4]

    # Criação do primeiro gráfico E' vs. E''
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 2, 1)
    plt.plot(frequencia, e, label="\u03B5'")
    plt.plot(frequencia, e_prime, label="\u03B5''")
    plt.xlabel(f"Frequência ({undfrequencia})")
    plt.ylabel("Permissividade Elétrica Relativa (\u03B5\u1D63)")
    plt.title('Arquivo: ' + csv_filename + "\nGráfico \u03B5' vs. \u03B5'' em função da Frequência")
    plt.legend()
    plt.grid(True)

    # Criação do segundo gráfico U' vs. U''
    ax = fig.add_subplot(1, 2, 2)
    plt.plot(frequencia, u, label="\u00B5'")
    plt.plot(frequencia, u_prime, label="\u00B5''")
    plt.xlabel(f"Frequência ({undfrequencia})")
    plt.ylabel("Permeabilidade Magnética Relativa (\u00B5\u1D63)")
    plt.title('Arquivo: ' + csv_filename + "\nGráfico \u00B5' vs. \u00B5'' em função da Frequência")
    plt.legend()
    plt.grid(True)

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    if coaxial:
        rota_informacoes = "/informacoescoaxial"
    else:
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
    '<body>' + \
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

    with open(f'./pythonPaginaINPE/templates/plot_mi_epsilon_{hash_arquivo}.html','w') as f:
        f.write(html)
