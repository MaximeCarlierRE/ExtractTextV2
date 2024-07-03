import fitz  # PyMuPDF
import re
import json
from flask import Flask, request, jsonify
from io import BytesIO

app = Flask(__name__)

def extract_note_from_pdf(file_data):
    # Ouvrir le fichier PDF depuis les données binaires
    document = fitz.open(stream=file_data, filetype='pdf')
    
    # Extraire tout le texte du PDF
    text_content = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text_content += page.get_text()
    
    # Utiliser regex pour trouver la note
    match = re.search(r'\b(\d{1,3}|1000)/1000\b', text_content)
    if match:
        note = int(match.group(1))
        return str(note) + '/1000'
    else:
        return json.dumps({'error': 'Note not found in the document'})

@app.route('/extract_note', methods=['POST'])
def extract_note():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file_data = file.read()  # Lire les données binaires du fichier
    
    result = extract_note_from_pdf(file_data)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
