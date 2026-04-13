from flask import Flask, jsonify, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'flask-cicd-demo'}), 200

@app.route('/items', methods=['GET'])
def get_items():
    items = [
        {'id': 1, 'name': 'Item One', 'value': 103},
        {'id': 2, 'name': 'Item Two', 'value': 200},
    ]
    return jsonify({'items': items, 'count': len(items)}), 200

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({'error': 'Missing value parameter'}), 400
    result = data['value'] * 2
    return jsonify({'input': data['value'], 'result': result}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
