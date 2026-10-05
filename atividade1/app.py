from flask import Flask, render_template, jsonify
from monitor import get_system_status
import dataclasses

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/system-status')
def system_status():
    status = get_system_status()
    # Converte a dataclass para dicionário nativo do Python
    return jsonify(dataclasses.asdict(status))

if __name__ == '__main__':
    # Roda em 0.0.0.0 para acesso externo na rede local
    app.run(host='0.0.0.0', port=5000, debug=True)
