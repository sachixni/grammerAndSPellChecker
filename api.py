from flask import Flask, request, jsonify
from flask_cors import CORS
import language_tool_python

# Initialize the Flask application and CORS
app = Flask(__name__)
CORS(app)

tool = language_tool_python.LanguageTool('en-US')

@app.route('/correct-text', methods=['POST'])
def correct_text():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided.'}), 400

    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return jsonify({
        'original_text': text,
        'corrected_text': corrected_text,
        'matches': [str(match) for match in matches]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
