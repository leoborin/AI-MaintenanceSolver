

import os
from re import template
import pandas as pd
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory, jsonify, render_template
import json

app = Flask(__name__)
UPLOAD_FOLDER = './data'


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # verifique se a solicitacao de postagem tem a parte do arquivo
        if 'file' not in request.files:
            flash('Nao tem a parte do arquivo')
            return redirect(request.url)
        file = request.files['file']

        # Se o usuario nao selecionar um arquivo, o navegador envia um
        # arquivo vazio sem um nome de arquivo.

        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <html>
    <head>
    <style>
        body {
        
        background: rgb(255,143,254);
        background: linear-gradient(160deg, rgba(255,143,254,0.7259278711484594) 0%, rgba(15,27,116,0.8127626050420168) 100%);
        background-size: cover;
        height: 860px;
      }
      
      form {
        
        width: 300px;
        background-color: #fff;
        border-radius: 5px;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3);
        margin: 0 auto;
        margin-top: 10%;
        padding: 20px;
        text-align: center;
        font-family: 'Gotham'
      }
      
      h2 {
        color: #333;
        margin-bottom: 20px;

      }
      
      .input {
        display: block;
        width: 90%;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
        border: 1px solid #ccc;
      }
      
      button {
        background-color: #4CAF50;
        color: #fff;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
      }
      .buttao {
        background-color: #9F2CF2;
        color: #fff;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        text-align: center;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3);
        transition: all 0.5s ease;
        
      }
      .button2 {
            display: block;
            margin: 20px 0;
            min-height: 50px;
            padding: 13px 24px;
            font-family: 'Lucida Grande', 'Helvetica', sans-serif;
            font-size: 16px;
            line-height: 20px;
            font-weight: bold;
            text-transform: uppercase;
            text-align: center;
            border: none;
            border-radius: 4px;
            outline: none;
            box-shadow: none;
            background-color: transparent;
            background-position: top center;
            cursor: pointer;
            transition: 0.3s ease-in-out;
            transition-property: background, color;
            }

      
      .buttao:hover {
        background-color: #581DDB;
      }
    </style>
        <title> Solver S </title>
    </head>
    <body>
        <div class="container" > 

        

        <form method="POST" action="" enctype="multipart/form-data">
        <h2> Solver S - Calibração PDM</h2>
        <br></br>
        <p><input type="file"  name="file"></p>
        <br></br>
        <p><input type="submit" class="buttao" value="Submit"></p>
        </form>
        </div>
    </body>
    </html>
        '''


@app.route('/teste', methods=['GET'])
def principal():
    return send_from_directory('', 'tratado.xlsx', as_attachment=True)


@app.route('/uploads/<name>', methods=['GET'])
def download_file(name):
    base_Original = pd.read_excel('data\{}'.format(name))
    base = pd.read_excel('data\{}'.format(name))

    base = base.sort_values(by='Flag Bolean')
    # display(base)
    media_base = (base['tempo estimado tarefa'].sum())/4
    semanamin = base['Semana'].min()
    semanamax = base['Semana'].max()
    semana = semanamin
    base_semana = base[(base.Semana == semana)]
    soma_semana = base_semana['tempo estimado tarefa'].sum()

    # variaveis HTML
    asemana1 = semanamin
    asemana2 = semana + 1
    asemana3 = semana + 2
    asemana4 = semana + 3

    base_semana1 = base[(base.Semana == asemana1)]
    base_semana2 = base[(base.Semana == asemana2)]
    base_semana3 = base[(base.Semana == asemana3)]
    base_semana4 = base[(base.Semana == asemana4)]

    aTTS1 = round(base_semana1['tempo estimado tarefa'].sum(), 2)
    aTTS2 = round(base_semana2['tempo estimado tarefa'].sum(), 2)
    aTTS3 = round(base_semana3['tempo estimado tarefa'].sum(), 2)
    aTTS4 = round(base_semana4['tempo estimado tarefa'].sum(), 2)

    aQTD1 = len(base_semana1)
    aQTD2 = len(base_semana2)
    aQTD3 = len(base_semana3)
    aQTD4 = len(base_semana4)

    #base.rename(columns={'Ativo+Tarefa+Ciclo': 'cod_completo'}, inplace = False)
    # novas_colunas(base,semanamin)
    # colocar_coluna_distinct_sum(base,semanamin)
    # equalizar_planos_iguais(semanamin,semanamax,base)
    # criar_lista_critica(base)
    # alg_tratamento(base)

    def criar_lista_critica(base):
        lista_ativos_criticos = base.groupby(by="concat_manut").sum()
        lista_ativos_criticos = lista_ativos_criticos.sort_values(
            by="Pont_total", ascending=True)
        lista_ativos_criticos = lista_ativos_criticos["Pont_total"]
        return lista_ativos_criticos

    # ajustando Base
    base.rename(columns={'Ativo+Tarefa+Ciclo': 'cod_completo'}, inplace=False)

    # novas_colunas(base,semanamin)
    base.insert(loc=25, column='new_week', value=semanamin)
    base.insert(loc=26, column='distinct_sum', value=0)
    base.insert(loc=27, column='listagem_count', value=0)
    base.insert(loc=28, column='Grupo', value=0)
    base.insert(loc=28, column='concat_manut', value=0)

    # colocar_coluna_distinct_sum(base,semanamin)

    base_teste = base
    count = base.groupby('Ativo+Tarefa+Ciclo')['BKNloja'].count()
    for item in base['Ativo+Tarefa+Ciclo']:
        resultado = count[item]
        base_teste.loc[base_teste['Ativo+Tarefa+Ciclo']
                       == item, 'distinct_sum'] = resultado
    base = base_teste

    # equalizar_planos_iguais(semanamin,semanamax,base)

    for i in range(semanamin, semanamax+1):
        base_semana = base[(base.new_week == semana)]
        for item in base_semana['id']:
            valor = max(
                base_semana.loc[base_semana['id'] == item, 'distinct_sum'].values)
            if valor >= 2:
                base_teste = base
                base_teste.rename(
                    columns={'Ativo+Tarefa+Ciclo': 'cod_completo'}, inplace=True)
                var = base.loc[base['id'] == item, 'cod_completo']
                var = var.tolist()
                var = var[0]
                base_teste = base_teste[(base_teste.cod_completo == var)]
                base_teste.sort_values(by='listagem_count')
                contador = 0
                for i in base_teste['id']:
                    base.loc[base['id'] == i, 'listagem_count'] = contador
                    contador += 1
                CicloDias = max(
                    base.loc[base['id'] == item, 'CicloDias'].values)
                ciclosemanas = round(CicloDias/7, 0)
                var_listagem_count = base.loc[base['id']
                                              == item, 'listagem_count']
                base.loc[base['id'] == item, 'new_week'] = base['new_week'] + \
                    (ciclosemanas*var_listagem_count)
    base = base.sort_values(by='cod_completo')

    # criar_lista_critica(base)

    lista_ativos_criticos = base.groupby(by="concat_manut").sum()
    lista_ativos_criticos = lista_ativos_criticos.sort_values(
        by="Pont_total", ascending=True)
    lista_ativos_criticos = lista_ativos_criticos["Pont_total"]

    # alg_tratamento(base)

    semana = semanamin
    base_semana = base[(base.new_week == semana)]
    soma_semana = base_semana['tempo estimado tarefa'].sum()
    acao_max = len(criar_lista_critica(base))
    indice_ativos_criticos = 0
    ativo_menos_critico_fixo = criar_lista_critica(
        base).index[indice_ativos_criticos]
    ativo_menos_critico = criar_lista_critica(
        base).index[indice_ativos_criticos]
    total_lista = len(criar_lista_critica(base))

    for i in range(semanamin, semanamax+1):
        base_semana = base[(base.new_week == semana)]
        soma_semana = base_semana['tempo estimado tarefa'].sum()
        gb_Ativos = base_semana.groupby(by="CodigoAtivo").sum()
        gb_Ativos_tempo = gb_Ativos['tempo estimado tarefa']
        for id2 in gb_Ativos_tempo.index:
            tmp = gb_Ativos['tempo estimado tarefa'][id2]
            tmpTotal = 0
            if tmp > media_base:
                base_semana2 = base_semana[(base_semana.CodigoAtivo == id2)]
                for id3 in base_semana2.index:
                    tmp3 = base_semana2['tempo estimado tarefa'][id3]
                    tmpTotal = tmpTotal + tmp3
                    if tmpTotal > tmp/2:
                        base_semana.loc[base_semana.index == id3, 'Grupo'] = 2
                    else:
                        base_semana.loc[base_semana.index == id3, 'Grupo'] = 1

        for x in base_semana.index:
            texto = base_semana.Grupo[x]
            base.loc[base.index == x, 'Grupo'] = texto

        for x in base.index:
            Grup = base.Grupo[x]
            CodAtv = base.CodigoAtivo[x]
            base.loc[base.index == x, 'concat_manut'] = str(
                CodAtv) + "-grupo-" + str(Grup)

            # Parte 2

        base_semana = base[(base.new_week == semana)]
        soma_semana = base_semana['tempo estimado tarefa'].sum()
        indice_ativos_criticos = 0
        lista_ativos_criticos = criar_lista_critica(base)
        for id in lista_ativos_criticos.index:
            atv_s = id
            if media_base*1.15 <= soma_semana:
                base.loc[base['concat_manut'] == atv_s,
                         'new_week'] = base['new_week']+1
            base_semana = base[(base.new_week == semana)]
            soma_semana = base_semana['tempo estimado tarefa'].sum()
            if indice_ativos_criticos < total_lista-2:
                indice_ativos_criticos = indice_ativos_criticos + 1
                ativo_menos_critico = criar_lista_critica(
                    base).index[indice_ativos_criticos]
                basesum = base.groupby(by="new_week").sum()
                basesum['tempo estimado tarefa']
        semana = semana+1
        indice_ativos_criticos = 0

    basesum = base.groupby(by="new_week").sum()
    basesum2 = base.groupby(by="Semana").sum()
    indice_semana_new = basesum['tempo estimado tarefa'].index.values.tolist()
    resultados_semana_new = basesum['tempo estimado tarefa'].values.tolist()
    indice_semana_old = basesum2['tempo estimado tarefa'].index.values.tolist()
    resultados_semana_old = basesum2['tempo estimado tarefa'].values.tolist()

    json_resultados_semana_old = json.dumps(resultados_semana_old)
    json_indice_semana_old = json.dumps(indice_semana_old)

    json_resultados_semana_new = json.dumps(resultados_semana_new)
    json_indice_semana_new = json.dumps(indice_semana_new)

    S1 = 18
    base = base

    valor = media_base*1.15
    quantidade = len(resultados_semana_old)

    limite1 = [valor] * quantidade
    limite1 = list(limite1)
    json_limite1 = json.dumps(limite1)

    quantidade2 = len(resultados_semana_new)
    limite2 = [valor] * quantidade2
    limite2 = list(limite2)
    json_limite2 = json.dumps(limite2)

    grouped = base.groupby(['CodigoAtivo', 'Semana'])[
        'tempo estimado tarefa'].sum()
    pivot_table = grouped.reset_index().pivot(
        index='CodigoAtivo', columns='Semana', values='tempo estimado tarefa')
    pivot_table.fillna(0, inplace=True)
    data_old = pivot_table.round(2)
    data_old = data_old.replace(0, "")

    data_old = data_old.reset_index()
    data_old = data_old.to_dict("records")

    grouped2 = base.groupby(['CodigoAtivo', 'new_week'])[
        'tempo estimado tarefa'].sum()
    pivot_table2 = grouped2.reset_index().pivot(
        index='CodigoAtivo', columns='new_week', values='tempo estimado tarefa')
    pivot_table2.fillna(0, inplace=True)
    data_new = pivot_table2.round(2)
    data_new = data_new.replace(0, "")
    data_new = data_new.reset_index()
    data_new = data_new.to_dict("records")

    grouped_crit = base.groupby(['CodigoAtivo', 'Semana'])[
        'N_Crit'].sum()
    pivot_table_crit = grouped_crit.reset_index().pivot(
        index='CodigoAtivo', columns='Semana', values='N_Crit')
    pivot_table_crit .fillna(0, inplace=True)
    data_old_crit = pivot_table_crit .round(2)
    data_old_crit = data_old_crit.replace(0, "")
    data_old_crit = data_old_crit.reset_index()
    data_old_crit = data_old_crit.to_dict("records")

    grouped2_crit = base.groupby(['CodigoAtivo', 'new_week'])[
        'N_Crit'].sum()
    pivot_table2_crit = grouped2_crit .reset_index().pivot(
        index='CodigoAtivo', columns='new_week', values='N_Crit')
    pivot_table2_crit .fillna(0, inplace=True)
    data_new_crit = pivot_table2_crit .round(2)
    data_new_crit = data_new_crit.replace(0, "")
    data_new_crit = data_new_crit.reset_index()
    data_new_crit = data_new_crit.to_dict("records")
    base['old_week'] = base['Semana']

    basevisao = base.loc[:, ['CodigoAtivo', 'old_week', 'new_week', 'cod_completo', 'MODELO ATIVO',
                             'tempo estimado tarefa', 'Vencido', 'is_critical', 'cod_completo', 'N_Crit']]
    basevisao = basevisao .round(2)
    basevisao = basevisao.to_dict("records")

    myarrey = [1, 2, 3, 4]
    teste = json.dumps(myarrey)

    print(resultados_semana_new)
    base = base.sort_values(by='Semana')
    base.to_excel("tratado.xlsx", sheet_name='base', header=True)
   # os.rename('tratado.xlsx', 'templates\tratado.xlsx')
    return render_template("index.html", basevisao=basevisao, data2_crit=data_new_crit, data_crit=data_old_crit, data2=data_new, data=data_old, limite_new=json_limite2, new_resultado=json_resultados_semana_new, new_indice=json_indice_semana_new, limite_old=json_limite1, old_resultado=json_resultados_semana_old, old_indice=json_indice_semana_old, semana1=0, semana2=0, semana3=0, semana4=0, TTS1=resultados_semana_old, TTS2=0, TTS3=0, TTS4=0, QTD1=0, QTD2=0, QTD3=0, QTD4=0, asemana1=asemana1, asemana2=asemana2, asemana3=asemana3, asemana4=asemana4, aTTS1=aTTS1, aTTS2=aTTS2, aTTS3=aTTS3, aTTS4=aTTS4, aQTD1=aQTD1, aQTD2=aQTD2, aQTD3=aQTD3, aQTD4=aQTD4)
    # ,


if __name__ == '__main__':
    app.run(debug=True)
