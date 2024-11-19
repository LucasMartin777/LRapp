from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
import uuid  # Para criar nomes únicos para os arquivos

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'  # Necessária para usar flash messages

# Configurações
UPLOAD_FOLDER_FOTOS = './uploads/fotos'
UPLOAD_FOLDER_DOCUMENTOS = './uploads/documentos'
DATABASE = 'database.db'

os.makedirs(UPLOAD_FOLDER_FOTOS, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_DOCUMENTOS, exist_ok=True)

# Rota para a página inicial
@app.route('/')
def home():
    return redirect(url_for('cadastro'))

# Rota para a página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            idade = request.form['idade']
            foto = request.files['foto']
            documento = request.files['documento']

            # Verificar se os campos obrigatórios estão preenchidos
            if not nome or not idade or not foto or not documento:
                flash('Todos os campos são obrigatórios!', 'error')
                return redirect(url_for('cadastro'))

            # Salvar foto com nome único
            foto_nome = f"{uuid.uuid4()}_{foto.filename}"
            foto_path = os.path.join(UPLOAD_FOLDER_FOTOS, foto_nome)
            foto.save(foto_path)

            # Salvar documento com nome único
            documento_nome = f"{uuid.uuid4()}_{documento.filename}"
            documento_path = os.path.join(UPLOAD_FOLDER_DOCUMENTOS, documento_nome)
            documento.save(documento_path)

            # Salvar dados no banco de dados
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pessoas (nome, idade, foto, documento) VALUES (?, ?, ?, ?)",
                (nome, idade, foto_nome, documento_nome)
            )
            conn.commit()
            conn.close()

            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('consulta'))
        except Exception as e:
            flash(f"Ocorreu um erro: {str(e)}", 'error')
            return redirect(url_for('cadastro'))

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
