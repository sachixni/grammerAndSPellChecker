from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import language_tool_python
import requests
from bs4 import BeautifulSoup

# Initialize the Flask application and CORS
app = Flask(__name__)
CORS(app)

tool = language_tool_python.LanguageTool('en-US')

@app.route('/correct-url', methods=['POST'])
def correct_url():
    data = request.json
    url = data.get('url', '')

    if not url:
        return jsonify({'error': 'No URL provided.'}), 400

    try:
        # Fetch and parse the HTML content from the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Define the tags you are interested in
        tags_to_check = ['p', 'h1', 'h2', 'li']

        # Dictionary to hold the results
        grammar_results = {}

        # Check each tag
        for tag_name in tags_to_check:
            grammar_results[tag_name] = []
            for tag in soup.find_all(tag_name):
                tag_text = tag.get_text(strip=True)
                matches = tool.check(tag_text)
                corrected_text = language_tool_python.utils.correct(tag_text, matches)
                grammar_results[tag_name].append({
                    'original_text': tag_text,
                    'corrected_text': corrected_text,
                    'matches': [str(match) for match in matches]
                })

        return jsonify(grammar_results)

    except requests.RequestException as e:
        return jsonify({'error': 'Error fetching URL content.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
