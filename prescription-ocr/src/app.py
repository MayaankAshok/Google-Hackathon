from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ocr.processor import extract_prescription_text, find_similar_drugs, medicine_db, extract_drug_name
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        # Read the image file
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        
        # Process the image
        prescription_details = extract_prescription_text(img)
        return jsonify(prescription_details)

@app.route('/similar', methods=['POST'])
def get_similar_drugs():
    data = request.get_json()
    if not data or 'medicine' not in data:
        return jsonify({'error': 'Drug name is required'}), 400
    
    drug_name = extract_drug_name(data['medicine'])
    if drug_name not in medicine_db:
        return jsonify({'error': 'Drug not found in database'}), 404
    
    similar_drugs = find_similar_drugs(medicine_db[drug_name])
    return jsonify({'similar_drugs': similar_drugs})

if __name__ == '__main__':
    app.run(debug=True)