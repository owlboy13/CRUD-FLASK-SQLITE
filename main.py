from flask import Flask, render_template, request, redirect, url_for
from database import TableProducts

app = Flask(__name__)


@app.route('/', methods=['GET'])
def form_product():
    return render_template('products.html')

@app.route('/', methods=['POST'])
def new_product():
    nome = request.form['nome']
    preco = float(request.form['preco'])

    db = TableProducts("produtos.db", "produtos")
    db.create_table()
    db.connect()
    db.insert(nome, preco)

    return redirect(url_for('index'))

@app.route('/index')
def index():
    db = TableProducts("produtos.db", "produtos")
    db.connect()
    produtos = db.view()

    return render_template('index.html', produtos=produtos)


if __name__ == '__main__':
    app.run(debug=True)
