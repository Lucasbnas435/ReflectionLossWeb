from flask import Flask, render_template, request, send_file
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from gerar_hash import get_hash
from ler_csv import read_csv
from ler_txt import read_txt
from plotar_mi_epsilon import mi_epsilon_plot
from plotar_RL_esp_fixa import RL_esp_fixa_plot
from plotar_RL_esp_var import RL_esp_var_plot
from plotar_RL_dinamico import RL_dinamico_plot
import shutil
from ler_csv_multicamadas import read_csv_multicamadas
from plotar_multicamadas import multicamadas_plot
from plotar_duo import duascamadas_plot
from ler_csv_doisEtres import read_csv_duas_tres_camadas
from ler_csv_coaxial import read_csv_coaxial
from gerar_xml import generate_xml_file_from_csv

app = Flask(__name__)
app.config['SECRET_KEY'] = "a1b2c3d4"
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired(), FileAllowed(['csv'], 'Por favor, envie um arquivo csv')])
    submit = SubmitField("Enviar arquivo")

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/arquivoumacamada', methods=['GET', 'POST'])
def arquivoumacamada():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        hash_arquivo = get_hash(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(f"{hash_arquivo}.csv")))
        csv_filename = file.filename
        return render_template("redirecionar.html", hash_arquivo=hash_arquivo, csv_filename=csv_filename)
    return render_template('arquivo_uma_camada.html', form=form)

@app.route('/informacoes', methods=['POST'])
def informacoes():
    try:
        csv_filename = request.form.get('csv_filename')
        hash_arquivo = request.form.get('hash_arquivo')
        txt_filename, compsuporteamostra, frequenciacorte, distamostra, espamostra, ifbw, power, nome_banda, undfrequencia = read_csv(hash_arquivo)
        read_txt(txt_filename)

        return render_template('informacoes.html', csv_filename=csv_filename,
        nome_arquivo_txt=txt_filename, frequenciacorte=frequenciacorte,
        compsuporteamostra=compsuporteamostra, distamostra=distamostra,
        espamostra=espamostra, ifbw=ifbw, power=power, nome_banda=nome_banda,
        undfrequencia=undfrequencia, hash_arquivo=hash_arquivo)
    except:
        return render_template('error_template.html')

@app.route('/miepsilon', methods=['POST'])
def miepsilon():
    try:
        csv_filename = request.form.get('csv_filename')
        hash_arquivo = request.form.get('hash_arquivo')
        undfrequencia = request.form.get('undfrequencia')

        mi_epsilon_plot(hash_arquivo, csv_filename, undfrequencia)
        return render_template(f'plot_mi_epsilon_{hash_arquivo}.html',
        csv_filename=csv_filename, hash_arquivo=hash_arquivo)
    except:
        return render_template('error_template.html')

@app.route('/reflectionlossespfixa', methods=['POST'])
def reflectionlossespfixa():
    try:
        hash_arquivo = request.form.get('hash_arquivo')
        csv_filename = request.form.get('csv_filename')
        txt_filename = request.form.get('txt_filename')
        undfrequencia = request.form.get('undfrequencia')
        espamostra = request.form.get('espamostra')
        baixar_grafico = int(request.form.get('baixar_grafico'))

        if baixar_grafico:
            filename = RL_esp_fixa_plot(csv_filename, txt_filename, undfrequencia,
            espamostra, baixar_grafico, hash_arquivo)
            return send_file(f"./static/files/saidas/saidas_{hash_arquivo}/{filename}", as_attachment=True)

        nome_template = RL_esp_fixa_plot(csv_filename, txt_filename, undfrequencia,
        espamostra, baixar_grafico, hash_arquivo)
        return render_template(nome_template, csv_filename=csv_filename,
        nome_arquivo_txt=txt_filename, undfrequencia=undfrequencia,
        espamostra=espamostra, hash_arquivo=hash_arquivo)
    except:
        return render_template('error_template.html')

@app.route('/reflectionlossespvar', methods=['POST'])
def reflectionlossespvar():
    try:
        inicio = request.form.get('inicio')
        fim = request.form.get('fim')
        passo = request.form.get('passo')
        hash_arquivo = request.form.get('hash_arquivo')
        csv_filename = request.form.get('csv_filename')
        txt_filename = request.form.get('txt_filename')
        undfrequencia = request.form.get('undfrequencia')
        espamostra = request.form.get('espamostra')
        baixar_grafico = int(request.form.get('baixar_grafico'))

        if baixar_grafico:
            RL_esp_var_plot(csv_filename, txt_filename, undfrequencia, espamostra,
            inicio, fim, passo, baixar_grafico, hash_arquivo)
            pasta_saidas = f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}"
            caminho_zip_gerado = f"./pythonPaginaINPE/static/files/saidas/zip_gerado/zip_{hash_arquivo}"
            shutil.make_archive(caminho_zip_gerado, 'zip', pasta_saidas)
            return send_file(f"./static/files/saidas/zip_gerado/zip_{hash_arquivo}.zip")

        nome_template, curva_menor_y = RL_esp_var_plot(csv_filename, txt_filename,
        undfrequencia, espamostra, inicio, fim, passo, baixar_grafico, hash_arquivo)
        return render_template(nome_template, val_inicio=inicio, val_fim=fim,
        val_passo=passo, csv_filename=csv_filename, nome_arquivo_txt=txt_filename,
        undfrequencia=undfrequencia, espamostra=espamostra, hash_arquivo=hash_arquivo,
        curva_menor_y=curva_menor_y)
    except:
        return render_template('error_template.html')

@app.route('/reflectionlossdinamico', methods=['POST'])
def reflectionlossdinamico():
    try:
        inicio_slider = float(request.form.get('inicio_slider'))
        fim_slider = float(request.form.get('fim_slider'))
        hash_arquivo = request.form.get('hash_arquivo')
        csv_filename = request.form.get('csv_filename')
        txt_filename = request.form.get('txt_filename')
        undfrequencia = request.form.get('undfrequencia')
        espamostra = request.form.get('espamostra')
        baixar_grafico = int(request.form.get('baixar_grafico'))

        if not espamostra:
            espamostra = inicio_slider * 1e-3

        if baixar_grafico:
            filename = RL_dinamico_plot(csv_filename, txt_filename, undfrequencia,
            espamostra, baixar_grafico, hash_arquivo)
            return send_file(f"./static/files/saidas/saidas_{hash_arquivo}/{filename}",as_attachment=True)

        nome_template = RL_dinamico_plot(csv_filename, txt_filename, undfrequencia,
        espamostra, baixar_grafico, hash_arquivo)
        return render_template(nome_template, csv_filename=csv_filename,
        nome_arquivo_txt=txt_filename, undfrequencia=undfrequencia, espamostra=espamostra,
        hash_arquivo=hash_arquivo, inicio_slider=inicio_slider, fim_slider=fim_slider)
    except:
        return render_template('error_template.html')

@app.route('/primeiroarquivo', methods=['GET', 'POST'])
def primeiroarquivo():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        csv_filename1 = file.filename
        hash_arquivo1 = get_hash(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(f"{hash_arquivo1}.csv")))
        return render_template("redirecionar_seg_arq_multicamadas.html", hash_arquivo1=hash_arquivo1, csv_filename1=csv_filename1)
    return render_template('primeiro_arquivo_multicamadas.html', form=form)

@app.route('/segundoarquivo', methods=['POST'])
def segundoarquivo():
    hash_arquivo1 = request.form.get('hash_arquivo1')
    csv_filename1 = request.form.get('csv_filename1')
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        csv_filename2 = file.filename
        hash_arquivo2 = get_hash(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(f"{hash_arquivo2}.csv")))
        return render_template("redirecionar_terc_arq_multicamadas.html", hash_arquivo1=hash_arquivo1, hash_arquivo2=hash_arquivo2, csv_filename1=csv_filename1, csv_filename2=csv_filename2)
    return render_template('segundo_arquivo_multicamadas.html', form=form, hash_arquivo1=hash_arquivo1, csv_filename1=csv_filename1)

@app.route('/terceiroarquivo', methods=['POST'])
def terceiroarquivo():
    try:
        hash_arquivo1 = request.form.get('hash_arquivo1')
        hash_arquivo2 = request.form.get('hash_arquivo2')
        csv_filename1 = request.form.get('csv_filename1')
        csv_filename2 = request.form.get('csv_filename2')
        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data
            csv_filename3 = file.filename
            hash_arquivo3 = get_hash(file.filename)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(f"{hash_arquivo3}.csv")))

            espessura_amostra1, espessura_amostra2, espessura_amostra3 = read_csv_multicamadas(hash_arquivo1, hash_arquivo2, hash_arquivo3)

            return render_template("redirecionar_grafico_multicamadas.html",
            hash_arquivo1=hash_arquivo1, hash_arquivo2=hash_arquivo2,
            hash_arquivo3=hash_arquivo3, csv_filename1=csv_filename1,
            csv_filename2=csv_filename2, csv_filename3=csv_filename3,
            espessura_amostra1=espessura_amostra1, espessura_amostra2=espessura_amostra2,
            espessura_amostra3=espessura_amostra3)
        return render_template('terceiro_arquivo_multicamadas.html', form=form,
        hash_arquivo1=hash_arquivo1, hash_arquivo2=hash_arquivo2,
        csv_filename1=csv_filename1, csv_filename2=csv_filename2)
    except:
        return render_template('error_template.html')

@app.route('/multicamadas', methods=['POST'])
def multicamadas():
    try:
        hash_arquivo1 = request.form.get('hash_arquivo1')
        hash_arquivo2 = request.form.get('hash_arquivo2')
        hash_arquivo3 = request.form.get('hash_arquivo3')
        csv_filename1 = request.form.get('csv_filename1')
        csv_filename2 = request.form.get('csv_filename2')
        csv_filename3 = request.form.get('csv_filename3')
        espessura_amostra1 = float(request.form.get('espessura_amostra1'))
        espessura_amostra2 = float(request.form.get('espessura_amostra2'))
        espessura_amostra3 = float(request.form.get('espessura_amostra3'))
        inicio_slider = float(request.form.get('inicio_slider'))
        fim_slider = float(request.form.get('fim_slider'))
        baixar_grafico = int(request.form.get('baixar_grafico'))
        menos_pontos = int(request.form.get('menos_pontos'))

        espamostra = [espessura_amostra1, espessura_amostra2, espessura_amostra3]

        if baixar_grafico:
            filename = multicamadas_plot(hash_arquivo1, hash_arquivo2, hash_arquivo3,
            espamostra, csv_filename1, csv_filename2, csv_filename3, baixar_grafico,
            menos_pontos)
            return send_file(f"./static/files/saidas/saidas_{hash_arquivo1}/{filename}", as_attachment=True)

        nome_template = multicamadas_plot(hash_arquivo1, hash_arquivo2, hash_arquivo3,
        espamostra, csv_filename1, csv_filename2, csv_filename3, baixar_grafico, menos_pontos)

        return render_template(nome_template, hash_arquivo1=hash_arquivo1,
         hash_arquivo2=hash_arquivo2, hash_arquivo3=hash_arquivo3, csv_filename1=csv_filename1,
         csv_filename2=csv_filename2, csv_filename3=csv_filename3, espessura_amostra1=espessura_amostra1,
         espessura_amostra2=espessura_amostra2, espessura_amostra3=espessura_amostra3,
         inicio_slider=inicio_slider, fim_slider=fim_slider, baixar_grafico=baixar_grafico, menos_pontos=menos_pontos)
    except:
        return render_template('error_template.html')

@app.route('/menospontosmult', methods=['POST'])
def menospontosmult():
    try:
        hash_arquivo1 = request.form.get('hash_arquivo1')
        hash_arquivo2 = request.form.get('hash_arquivo2')
        hash_arquivo3 = request.form.get('hash_arquivo3')
        csv_filename1 = request.form.get('csv_filename1')
        csv_filename2 = request.form.get('csv_filename2')
        csv_filename3 = request.form.get('csv_filename3')
        espessura_amostra1 = float(request.form.get('espessura_amostra1'))
        espessura_amostra2 = float(request.form.get('espessura_amostra2'))
        espessura_amostra3 = float(request.form.get('espessura_amostra3'))
        inicio_slider = float(request.form.get('inicio_slider'))
        fim_slider = float(request.form.get('fim_slider'))
        baixar_grafico = int(request.form.get('baixar_grafico'))
        menos_pontos = int(request.form.get('menos_pontos'))
        divisor_quantidade_pontos = int(request.form.get('divisor_quantidade_pontos'))

        espamostra = [espessura_amostra1, espessura_amostra2, espessura_amostra3]

        nome_template = multicamadas_plot(hash_arquivo1, hash_arquivo2, hash_arquivo3,
        espamostra, csv_filename1, csv_filename2, csv_filename3, baixar_grafico,
        menos_pontos, divisor_quantidade_pontos)

        return render_template(nome_template, hash_arquivo1=hash_arquivo1,
         hash_arquivo2=hash_arquivo2, hash_arquivo3=hash_arquivo3, csv_filename1=csv_filename1,
         csv_filename2=csv_filename2, csv_filename3=csv_filename3, espessura_amostra1=espessura_amostra1,
         espessura_amostra2=espessura_amostra2, espessura_amostra3=espessura_amostra3,
         inicio_slider=inicio_slider, fim_slider=fim_slider, baixar_grafico=baixar_grafico,
         menos_pontos=menos_pontos, divisor_quantidade_pontos=divisor_quantidade_pontos)
    except:
        return render_template('error_template.html')

@app.route('/primeiroarquivoduo', methods=['GET', 'POST'])
def primeiroarquivoduo():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        csv_filename1 = file.filename
        hash_arquivo1 = get_hash(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(f"{hash_arquivo1}.csv")))
        return render_template("redirecionar_seg_arq_duascamadas.html",
        hash_arquivo1=hash_arquivo1, csv_filename1=csv_filename1)
    return render_template('primeiro_arquivo_duascamadas.html', form=form)

@app.route('/segundoarquivoduo', methods=['POST'])
def segundoarquivoduo():
    try:
        hash_arquivo1 = request.form.get('hash_arquivo1')
        csv_filename1 = request.form.get('csv_filename1')
        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data
            csv_filename2 = file.filename
            hash_arquivo2 = get_hash(file.filename)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(f"{hash_arquivo2}.csv")))

            espessura_amostra1, espessura_amostra2 = read_csv_duas_tres_camadas(hash_arquivo1, hash_arquivo2)

            return render_template("redirecionar_grafico_duascamadas.html",
            hash_arquivo1=hash_arquivo1, hash_arquivo2=hash_arquivo2,
            csv_filename1=csv_filename1, csv_filename2=csv_filename2,
            espessura_amostra1=espessura_amostra1, espessura_amostra2=espessura_amostra2)
        return render_template('segundo_arquivo_duascamadas.html', form=form,
        hash_arquivo1=hash_arquivo1, csv_filename1=csv_filename1)
    except:
        return render_template('error_template.html')

@app.route('/duascamadas', methods=['POST'])
def duascamadas():
    try:
        hash_arquivo1 = request.form.get('hash_arquivo1')
        hash_arquivo2 = request.form.get('hash_arquivo2')
        csv_filename1 = request.form.get('csv_filename1')
        csv_filename2 = request.form.get('csv_filename2')
        espessura_amostra1 = float(request.form.get('espessura_amostra1'))
        espessura_amostra2 = float(request.form.get('espessura_amostra2'))
        inicio_slider = float(request.form.get('inicio_slider'))
        fim_slider = float(request.form.get('fim_slider'))
        baixar_grafico = int(request.form.get('baixar_grafico'))
        menos_pontos = int(request.form.get('menos_pontos'))

        espamostra = [espessura_amostra1, espessura_amostra2]

        if baixar_grafico:
            filename = duascamadas_plot(hash_arquivo1, hash_arquivo2,
                                        espamostra, csv_filename1, csv_filename2,
                                        baixar_grafico, menos_pontos)
            return send_file(f"./static/files/saidas/saidas_{hash_arquivo1}/{filename}", as_attachment=True)

        nome_template = duascamadas_plot(hash_arquivo1, hash_arquivo2, espamostra,
                          csv_filename1, csv_filename2, baixar_grafico, menos_pontos)

        return render_template(nome_template, hash_arquivo1=hash_arquivo1,
         hash_arquivo2=hash_arquivo2, csv_filename1=csv_filename1, csv_filename2=csv_filename2,
         espessura_amostra1=espessura_amostra1,espessura_amostra2=espessura_amostra2,
         inicio_slider=inicio_slider, fim_slider=fim_slider, baixar_grafico=baixar_grafico,
         menos_pontos=menos_pontos)
    except:
        return render_template('error_template.html')

@app.route('/menospontosduas', methods=['POST'])
def menospontosduas():
    try:
        hash_arquivo1 = request.form.get('hash_arquivo1')
        hash_arquivo2 = request.form.get('hash_arquivo2')
        csv_filename1 = request.form.get('csv_filename1')
        csv_filename2 = request.form.get('csv_filename2')
        espessura_amostra1 = float(request.form.get('espessura_amostra1'))
        espessura_amostra2 = float(request.form.get('espessura_amostra2'))
        inicio_slider = float(request.form.get('inicio_slider'))
        fim_slider = float(request.form.get('fim_slider'))
        baixar_grafico = int(request.form.get('baixar_grafico'))
        menos_pontos = int(request.form.get('menos_pontos'))
        divisor_quantidade_pontos = int(request.form.get('divisor_quantidade_pontos'))

        espamostra = [espessura_amostra1, espessura_amostra2]

        nome_template = duascamadas_plot(hash_arquivo1, hash_arquivo2, espamostra,
                          csv_filename1, csv_filename2, baixar_grafico,
                          menos_pontos, divisor_quantidade_pontos)

        return render_template(nome_template, hash_arquivo1=hash_arquivo1,
         hash_arquivo2=hash_arquivo2, csv_filename1=csv_filename1,
         csv_filename2=csv_filename2, espessura_amostra1=espessura_amostra1,
         espessura_amostra2=espessura_amostra2,
         inicio_slider=inicio_slider, fim_slider=fim_slider, baixar_grafico=baixar_grafico,
         menos_pontos=menos_pontos, divisor_quantidade_pontos=divisor_quantidade_pontos)
    except:
        return render_template('error_template.html')

@app.route('/arquivocoaxial', methods=['GET', 'POST'])
def arquivocoaxial():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        hash_arquivo = get_hash(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(f"{hash_arquivo}.csv")))
        csv_filename = file.filename
        return render_template("redirecionar_coaxial.html", hash_arquivo=hash_arquivo,
        csv_filename=csv_filename)
    return render_template('arquivo_coaxial.html', form=form)

@app.route('/informacoescoaxial', methods=['POST'])
def informacoescoaxial():
    csv_filename = request.form.get('csv_filename')
    hash_arquivo = request.form.get('hash_arquivo')
    txt_filename, espamostra, undfrequencia = read_csv_coaxial(hash_arquivo)
    read_txt(txt_filename)

    return render_template('informacoes_coaxial.html', csv_filename=csv_filename,
    nome_arquivo_txt=txt_filename, espamostra=espamostra, undfrequencia=undfrequencia,
    hash_arquivo=hash_arquivo)

@app.route('/miepsiloncoaxial', methods=['POST'])
def miepsiloncoaxial():
    csv_filename = request.form.get('csv_filename')
    hash_arquivo = request.form.get('hash_arquivo')
    undfrequencia = request.form.get('undfrequencia')

    mi_epsilon_plot(hash_arquivo, csv_filename, undfrequencia, coaxial=True)
    return render_template(f'plot_mi_epsilon_{hash_arquivo}.html',
    csv_filename=csv_filename, hash_arquivo=hash_arquivo)

@app.route('/rlespfixacoaxial', methods=['POST'])
def rlespfixacoaxial():
    hash_arquivo = request.form.get('hash_arquivo')
    csv_filename = request.form.get('csv_filename')
    txt_filename = request.form.get('txt_filename')
    undfrequencia = request.form.get('undfrequencia')
    espamostra = request.form.get('espamostra')
    baixar_grafico = int(request.form.get('baixar_grafico'))

    if baixar_grafico:
        filename = RL_esp_fixa_plot(csv_filename, txt_filename, undfrequencia,
        espamostra, baixar_grafico, hash_arquivo, coaxial=True)
        return send_file(f"./static/files/saidas/saidas_{hash_arquivo}/{filename}", as_attachment=True)

    nome_template = RL_esp_fixa_plot(csv_filename, txt_filename, undfrequencia,
    espamostra, baixar_grafico, hash_arquivo, coaxial=True)
    return render_template(nome_template, csv_filename=csv_filename,
    nome_arquivo_txt=txt_filename, undfrequencia=undfrequencia,
    espamostra=espamostra, hash_arquivo=hash_arquivo)

@app.route('/rlespvarcoaxial', methods=['POST'])
def rlespvarcoaxial():
    inicio = request.form.get('inicio')
    fim = request.form.get('fim')
    passo = request.form.get('passo')
    hash_arquivo = request.form.get('hash_arquivo')
    csv_filename = request.form.get('csv_filename')
    txt_filename = request.form.get('txt_filename')
    undfrequencia = request.form.get('undfrequencia')
    espamostra = request.form.get('espamostra')
    baixar_grafico = int(request.form.get('baixar_grafico'))

    if baixar_grafico:
        RL_esp_var_plot(csv_filename, txt_filename, undfrequencia, espamostra,
        inicio, fim, passo, baixar_grafico, hash_arquivo, coaxial=True)
        pasta_saidas = f"./pythonPaginaINPE/static/files/saidas/saidas_{hash_arquivo}"
        caminho_zip_gerado = f"./pythonPaginaINPE/static/files/saidas/zip_gerado/zip_{hash_arquivo}"
        shutil.make_archive(caminho_zip_gerado, 'zip', pasta_saidas)
        return send_file(f"./static/files/saidas/zip_gerado/zip_{hash_arquivo}.zip")

    nome_template, curva_menor_y = RL_esp_var_plot(csv_filename, txt_filename,
    undfrequencia, espamostra, inicio, fim, passo, baixar_grafico, hash_arquivo,
    coaxial=True)
    return render_template(nome_template, val_inicio=inicio, val_fim=fim,
    val_passo=passo, csv_filename=csv_filename, nome_arquivo_txt=txt_filename,
    undfrequencia=undfrequencia, espamostra=espamostra, hash_arquivo=hash_arquivo,
    curva_menor_y=curva_menor_y)

@app.route('/rldinamicocoaxial', methods=['POST'])
def rldinamicocoaxial():
    inicio_slider = float(request.form.get('inicio_slider'))
    fim_slider = float(request.form.get('fim_slider'))
    hash_arquivo = request.form.get('hash_arquivo')
    csv_filename = request.form.get('csv_filename')
    txt_filename = request.form.get('txt_filename')
    undfrequencia = request.form.get('undfrequencia')
    espamostra = request.form.get('espamostra')
    baixar_grafico = int(request.form.get('baixar_grafico'))

    if not espamostra:
        espamostra = inicio_slider * 1e-3

    if baixar_grafico:
        filename = RL_dinamico_plot(csv_filename, txt_filename, undfrequencia,
        espamostra, baixar_grafico, hash_arquivo, coaxial=True)
        return send_file(f"./static/files/saidas/saidas_{hash_arquivo}/{filename}", as_attachment=True)

    nome_template = RL_dinamico_plot(csv_filename, txt_filename, undfrequencia,
    espamostra, baixar_grafico, hash_arquivo, coaxial=True)
    return render_template(nome_template, csv_filename=csv_filename,
    nome_arquivo_txt=txt_filename, undfrequencia=undfrequencia,
    espamostra=espamostra, hash_arquivo=hash_arquivo, inicio_slider=inicio_slider,
    fim_slider=fim_slider)

@app.route('/gerarxml', methods=['GET', 'POST'])
def gerarxml():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        hash_arquivo = get_hash(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(f"{hash_arquivo}.csv")))
        csv_filename = file.filename
        generate_xml_file_from_csv(hash_arquivo, csv_filename)
        return send_file(f"./static/files/saidas/{hash_arquivo}.xml", as_attachment=True)
    return render_template('arquivo_xml.html', form=form)

@app.route('/errorteste', methods=['GET', 'POST'])
def errorteste():
    return render_template('error_template.html')

if __name__ == '__main__':
    app.run(debug=True)
