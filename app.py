from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

investimentos = {}

@app.route('/')
def index():
    return render_template('index.html', investimentos=investimentos)

@app.route('/add_mes', methods=['POST'])
def add_mes():
    mes = request.form.get('mes')
    if mes not in investimentos:
        investimentos[mes] = {
            'valor_inicial': 0.0,
            'rendimentos': 0.0,
            'aportes': [],
        }
    return redirect(url_for('index'))

@app.route('/add_aporte', methods=['POST'])
def add_aporte():
    mes = request.form.get('mes')
    valor = float(request.form.get('valor'))
    
    if mes in investimentos:
        investimentos[mes]['aportes'].append(valor)
        investimentos[mes]['valor_inicial'] += valor
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
