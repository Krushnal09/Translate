from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)
app.template_folder= 'templates'
def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest=target_language)
    return translated_text.text

@app.route('/', methods=['GET', 'POST'])
def index():
    translation = None
    error = None

    if request.method == 'POST':
        text = request.form.get('text', '')
        target_language = request.form.get('language', 'hi')  # Default to Hindi if not selected
        if text.strip():
            translation = translate_text(text, target_language)
        else:
            error = "Please enter text to translate."

    return render_template('index.html', translation=translation, error=error)

if __name__ == "__main__":
    
    app.run(debug=True)
