import matplotlib.pyplot as plt
import numpy as np
import base64
import os
import shutil
from io import BytesIO

def RL_esp_fixa_plot(csv_filename, txt_filename, undfrequencia, espamostra, baixar_grafico, hash_arquivo, coaxial=False):
	arq = open(f'./pythonPaginaINPE/static/files/txt_gerado/{txt_filename}','r')
	ler = arq.readlines()
	arq.close()

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

	#teste = input()

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
		s11_v.append(round(db,5)) # dB

	if baixar_grafico:
		#esse try sera retirado quando o hash for implantado
		try:
			os.mkdir(f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}")
		except:
			shutil.rmtree(f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}")
			os.mkdir(f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}")

		espessura = str(round(d/1e-3,2))
		grav = open(f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}/mm_{espessura}mm.txt",'w')
		titulo = "%4s(%3s)  %s\n"%("Freq",undfrequencia,"RL(dB)")
		grav.write(titulo)

		for i in range(0,len(F)):
			escrever = "%.2f %.2f\n"%(F[i],s11_v[i])
			grav.write(escrever)

		grav.close()
		return f"mm_{espessura}mm.txt"


	fig = plt.figure(figsize=(10, 5))
	#Dados para serem Plotados
	plt.plot(F,s11_v, label = str(float(d)*1e3))

	#Plotando grafico
	plt.legend(title = 'Espessura (mm)')
	plt.xlabel('Frequência (%s)'%undfrequencia)
	plt.ylabel('Perda por Reflexão (dB)')
	plt.title('Arquivo: ' + csv_filename)

	tmpfile = BytesIO()
	fig.savefig(tmpfile, format='png')
	encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

	if coaxial:
	    rota_grafico = "/rlespfixacoaxial"
	    rota_informacoes = "/informacoescoaxial"
	else:
	    rota_grafico = "/reflectionlossespfixa"
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
    '<a href="/arquivocoaxial" class="btn">Coaxial</a>' + \
    '<a href="/gerarxml" class="btn">Gerar XML</a>' + \
    '<div class="images">' + \
    '<img src="{{ url_for("static", filename="images/logoINPE.png") }}" alt="Logotipo do INPE">' + \
    '<img src="{{ url_for("static", filename="images/logoFATEC.png") }}" alt="Logotipo da FATEC Taubate">' + \
    '</div>' + \
    '</header>' + \
	'<img src=\'data:image/png;base64,{}\'>'.format(encoded) + \
	f'<form action="{rota_grafico}" method="post">' + \
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

	nome_template = f"plot_RL_esp_fixa_{hash_arquivo}.html"

	with open(f'./pythonPaginaINPE/templates/{nome_template}','w') as f:
		f.write(html)

	return nome_template
