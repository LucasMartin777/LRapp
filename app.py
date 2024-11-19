from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import sqlite3

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER_FOTOS = './uploads/fotos'
UPLOAD_FOLDER_DOCUMENTOS = './uploads/documentos'
DATABASE = 'database.db'

os.makedirs(UPLOAD_FOLDER_FOTOS, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_DOCUMENTOS, exist_ok=True)

# Rota para a página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        foto = request.files['foto']
        documento = request.files['documento']

        # Salvar foto
        if foto:
            foto_path = os.path.join(UPLOAD_FOLDER_FOTOS, foto.filename)
            foto.save(foto_path)

        # Salvar documento
        if documento:
            documento_path = os.path.join(UPLOAD_FOLDER_DOCUMENTOS, documento.filename)
            documento.save(documento_path)

        # Salvar dados no banco
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pessoas (nome, idade, foto, documento) VALUES (?, ?, ?, ?)",
            (nome, idade, foto.filename, documento.filename)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('consulta'))

    return render_template('cadastro.html')

# Rota para a página de consulta
@app.route('/consulta')
def consulta():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")
    pessoas = cursor.fetchall()
    conn.close()
    return render_template('consulta.html', pessoas=pessoas)

# Inicializar banco de dados
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            foto TEXT NOT NULL,
            documento TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
