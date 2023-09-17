import os
import PyPDF2
from googletrans import Translator

from flask import Flask, render_template, request, send_file
from fpdf import FPDF

app = Flask(__name__, template_folder='.')

@app.route("/", methods=["POST"])
def index():
    if request.method == "POST":
        input_pdf = request.files["input_pdf"]
        target_language = request.form["target_language"]

        # Ensure the user provided a file
        if input_pdf and input_pdf.filename.endswith('.pdf'):
            # Translate the input PDF
            translated_pdf = translate_pdf(input_pdf, target_language)

            # Serve the translated PDF as a response
            return send_file(
                translated_pdf,
                as_attachment=True,
                download_name="translated_output.pdf",
                mimetype="application/pdf"
            )

    return render_template("index.html")

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf = PyPDF2.PdfReader(pdf_file)

    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        text += page.extract_text()

    return text

def translate_text(text, dest_language):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return "Translation error"
    
def generate_readable_pdf(translated_text):
    # Create a new PDF to store the translated text
    translated_pdf = FPDF()
    translated_pdf.add_page()
    translated_pdf.set_font("Arial", size=12)

     # Encode the translated text as UTF-8
    translated_text_utf8 = translated_text.encode("utf-8")

    # Add translated text to the new PDF
    translated_pdf.multi_cell(0, 10, translated_text)

    # Save the translated PDF to a temporary file
    temp_file = "translated_output.pdf"
    translated_pdf.output(temp_file)
    return temp_file

def translate_pdf(input_pdf, target_language):
        # Extract text from the input PDF
    input_text = extract_text_from_pdf(input_pdf)

    # Translate the extracted text
    translated_text = translate_text(input_text, target_language)

    # Generate a translated PDF with the translated text
    translated_pdf = generate_readable_pdf(translated_text)

    return translated_pdf

if __name__ == "__main__":
    app.run(debug=True)
