from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'chave-secreta-para-sessoes'  # troque por algo aleatório
DATABASE = 'database.db'

# Criar tabela de produtos
def init_db():
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

init_db()

# Página inicial
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Adicionar produto
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

# Página de detalhes
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('product_detail.html', product=product)

# ------------------- ÁREA RESTRITA -------------------

# Login do administrador
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'admin123':  # 🔐 senha fixa (troque se quiser)
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template('login.html', error='Senha incorreta!')
    return render_template('login.html')

# Painel do administrador
@app.route('/admin')
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('admin.html', products=products)

# Excluir produto
@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

# Logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# -----------------------------------------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
