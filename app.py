from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde otros dominios

# Ruta para la base de datos
DATABASE = os.path.join(os.getcwd(), 'votes.db')

# Inicializar base de datos
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS votes (categoria TEXT, voto TEXT)')
init_db()

@app.route('/')
def index():
    return render_template('index.html')  # Sirve el archivo index.html desde templates/

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    if not data:
        return jsonify({'status': 'error', 'message': 'No se enviaron datos'}), 400

    with sqlite3.connect(DATABASE) as conn:
        conn.execute('INSERT INTO votes (categoria, voto) VALUES (?, ?)', 
                     (list(data.keys())[0], list(data.values())[0]))
    return jsonify({'status': 'success'})

@app.route('/results', methods=['GET'])
def results():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute('SELECT categoria, voto, COUNT(*) as votos FROM votes GROUP BY categoria, voto')
        results = [{'categoria': row[0], 'voto': row[1], 'votos': row[2]} for row in cursor.fetchall()]
    return jsonify(results)

if __name__ == '__main__':
    app.run()  # Ejecutar sin debug en producción
