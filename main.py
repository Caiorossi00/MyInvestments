from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

investimentos = {}

def get_mes_nome(mes):
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return meses[mes - 1]

@app.route('/')
def index():
    ano_atual = datetime.now().year
    meses_do_ano = [(f"{get_mes_nome(m)} {ano_atual}", m) for m in range(1, 13)]
    return render_template('index.html', meses=meses_do_ano)

@app.route('/mes/<int:mes>')
def mes(mes):
    ano_atual = datetime.now().year
    mes_nome = f"{get_mes_nome(mes)} {ano_atual}"
    
    dados = investimentos.get(mes_nome, {
        'valor_inicial': 0.0,
        'rendimentos': 0.0,
        'aportes': [],
    })
    
    total_aportes = sum(dados['aportes'])

    dados['aportes_com_indices'] = list(enumerate(dados['aportes']))

    return render_template('mes.html', mes=mes_nome, dados=dados, total_aportes=total_aportes)

@app.route('/add_aporte', methods=['POST'])
def add_aporte():
    mes = request.form.get('mes')
    valor = float(request.form.get('valor'))

    if mes in investimentos:
        investimentos[mes]['aportes'].append(valor)
        investimentos[mes]['valor_inicial'] += valor
    else:
        investimentos[mes] = {
            'valor_inicial': valor,
            'rendimentos': 0.0,
            'aportes': [valor],
        }

    return redirect(url_for('mes', mes=mes.split()[0]))  

@app.route('/remove_aporte', methods=['POST'])
def remove_aporte():
    mes = request.form.get('mes')
    index = int(request.form.get('index'))

    if mes in investimentos and 0 <= index < len(investimentos[mes]['aportes']):
        valor_removido = investimentos[mes]['aportes'].pop(index)
        investimentos[mes]['valor_inicial'] -= valor_removido

    return redirect(url_for('mes', mes=mes.split()[0]))  # Redireciona para a rota do mês

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
