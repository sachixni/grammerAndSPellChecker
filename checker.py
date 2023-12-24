import language_tool_python

def correct_text(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text, matches

def generate_html_report(original_text, corrected_text, matches):
    html_content = f"""
    <html>
    <head>
        <title>Grammar Check Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2 {{ color: #333; }}
            .section {{ margin-bottom: 20px; }}
            .original-text, .corrected-text {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; }}
            .corrections {{ list-style-type: none; padding: 0; }}
            .correction {{ background-color: #ffdddd; border: 1px solid #ee8888; padding: 10px; margin-bottom: 10px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>Grammar Check Report</h1>
        <div class="section">
            <h2>Original Text:</h2>
            <div class="original-text">{original_text}</div>
        </div>
        <div class="section">
            <h2>Corrected Text:</h2>
            <div class="corrected-text">{corrected_text}</div>
        </div>
        <div class="section">
            <h2>Details of Corrections:</h2>
            <ul class="corrections">
    """

    for match in matches:
        html_content += f'<li class="correction">{match}</li>'

    html_content += """
            </ul>
        </div>
    </body>
    </html>
    """
    return html_content

# The text to be corrected
user_provided_text = "This is the text that needs to be corected. It has a few errrors."

# Correct the user-provided text
corrected_text, matches = correct_text(user_provided_text)

# Generate the HTML report
html_report = generate_html_report(user_provided_text, corrected_text, matches)

# Save the report to an HTML file
with open("grammar_check_report.html", "w", encoding='utf-8') as file:
    file.write(html_report)

print("The HTML report has been generated: grammar_check_report.html")
