from flask import Flask, request, jsonify
from model import translate

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate_api():
    data = request.get_json()
    texts = data.get('texts')
    if not texts:
        return jsonify({'error': 'No text provided'}), 400
    results = translate(texts)
    if isinstance(results, dict) and 'error' in results:
        return jsonify(results), 400
    return jsonify({'translated': results})

if __name__ == '__main__':
    app.run(debug=True)
