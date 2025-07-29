from flask import Flask, request, jsonify, render_template
from model import translate
import json
import os

app = Flask(__name__)
HISTORY_FILE = 'data/translation_history.json'

if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_api():
    data = request.get_json()
    texts = data.get('texts')
    if not texts:
        return jsonify({'error': 'No text provided'}), 400
    results = translate(texts)
    if isinstance(results, dict) and 'error' in results:
        return jsonify(results), 400
    
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        history = json.load(f)
    for original, translated in zip(texts, results):
        history.append({'original': original, 'translated': translated, 'timestamp': str(__import__('datetime').datetime.now())})
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return jsonify({'translated': results})

@app.route('/history', methods=['GET'])
def get_history():
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        history = json.load(f)
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True)