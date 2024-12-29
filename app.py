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
    data = request.json  # Recibe el JSON enviado desde el front-end
    if not data or not isinstance(data, dict):
        return jsonify({'status': 'error', 'message': 'Datos inválidos'}), 400

    try:
        # Extraer categoría y voto
        for category, nominee in data.items():
            if isinstance(nominee, dict):  # Si el nominado es un dict, extraer su nombre
                nominee = nominee.get('name', 'Desconocido')  # Ajustar según tu formato
            with sqlite3.connect(DATABASE) as conn:
                conn.execute(
                    'INSERT INTO votes (categoria, voto) VALUES (?, ?)',
                    (category, nominee)  # Asegúrate de enviar strings
                )
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/results', methods=['GET'])
def results():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute('SELECT categoria, voto, COUNT(*) as votos FROM votes GROUP BY categoria, voto')
        results = [{'categoria': row[0], 'voto': row[1], 'votos': row[2]} for row in cursor.fetchall()]
    return jsonify(results)

if __name__ == '__main__':
    app.run()  # Ejecutar sin debug en producción

