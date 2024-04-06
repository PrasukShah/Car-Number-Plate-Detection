from flask import Flask, render_template, request
import os
import cv2
import easyocr
from werkzeug.utils import secure_filename

app = Flask(_name_)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)  # Ensure GPU is disabled for compatibility

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_ocr(image_path):
    # Perform OCR
    output = reader.readtext(image_path)
    
    # Extracted text
    extracted_text = ""
    for detection in output:
        extracted_text += detection[1] + " "
    
    return extracted_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")
        
        file = request.files['file']
        
        # Check if file is uploaded
        if file.filename == '':
            return render_template('index.html', error="No selected file")
        
        # Check file extension
        if not allowed_file(file.filename):
            return render_template('index.html', error="Unsupported file format")
        
        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Perform OCR
        extracted_text = perform_ocr(file_path)
        
        # Delete the uploaded file after OCR
        os.remove(file_path)
        
        return render_template('index.html', extracted_text=extracted_text)
    
    return render_template('index.html')

if _name_ == "_main_":
    app.run(debug=True)