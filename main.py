## Simple Flask app to host an AI model
from flask import Flask, request, jsonify
import os
import detectron_camera as dc
from flask_cors import CORS
import base64
import cv2
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
CORS(app) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/model', methods=['POST'])
def run_model():
    print("doing model stuff")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    print(request.files)
    print(request.form)
    if 'file_field' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file_field']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "img0" + file.filename[-4:])
        file.save(file_path)
        detected, labels = dc.get_classes(file_path)
        print(detected)
        print(labels)
        # _, buffer = cv2.imencode('.jpg', detected)  # or the appropriate image format
        detected_image_base64 = base64.b64encode(detected).decode('utf-8')        
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename, 'labels': labels, 'detected_image': detected_image_base64}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(port=5000, debug=True)