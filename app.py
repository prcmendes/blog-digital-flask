from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'

# Função para criar banco e tabela
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                download_link TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# Inicializa o banco ao iniciar o app
init_db()

# Página inicial - lista produtos
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Página para adicionar produto
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        download_link = request.form['download_link']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, description, price, download_link)
            VALUES (?, ?, ?, ?)
        ''', (name, description, price, download_link))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_product.html')

# Página de detalhe do produto
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('product_detail.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
