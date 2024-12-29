from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Inicializar base de datos
def init_db():
    with sqlite3.connect('votes.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS votes (categoria TEXT, voto TEXT)')
init_db()

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    with sqlite3.connect('votes.db') as conn:
        conn.execute('INSERT INTO votes (categoria, voto) VALUES (?, ?)',
                     (data['categoria'], data['voto']))
    return jsonify({'status': 'success'})

@app.route('/results', methods=['GET'])
def results():
    with sqlite3.connect('votes.db') as conn:
        cursor = conn.execute('SELECT categoria, voto, COUNT(*) as votos FROM votes GROUP BY categoria, voto')
        results = [{'categoria': row[0], 'voto': row[1], 'votos': row[2]} for row in cursor.fetchall()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
