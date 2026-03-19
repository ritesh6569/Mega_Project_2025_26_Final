import os
import json
import numpy as np
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import local modules using the guaranteed naming convention
from core.preprocessor import preprocess_image
from core.feature_extractor import get_extracted_features
from core.verifier import verify_document

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "document-verification-api"})

@app.route('/api/verify', methods=['POST'])
def verify():
    if 'document' not in request.files:
        return jsonify({"status": "error", "message": "No document uploaded"}), 400
    
    file = request.files['document']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    try:
        techniques = json.loads(request.form.get('techniques', '["resizing", "grayscale"]'))
        feature_techniques = json.loads(request.form.get('feature_techniques', '["CNN", "SIFT", "HOG", "LBP", "ORB"]'))
    except:
        techniques = ["resizing", "grayscale"]
        feature_techniques = ["CNN", "SIFT", "HOG", "LBP", "ORB"]

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Preprocessing
        processed_img = preprocess_image(filepath, techniques)
        
        # Feature Extraction
        features = get_extracted_features(processed_img, feature_techniques)
        
        # Verification
        v_res = verify_document(features)
        
        # Final combined report
        final_report = {**features, **v_res}

        return jsonify({
            "status": "success",
            "data": final_report
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"INTERNAL ERROR: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
