## Simple Flask app to host an AI model
from flask import Flask, request, jsonify, send_from_directory, url_for
import os
import detectron_camera as dc
from flask_cors import CORS
import base64
import cv2
from flask import render_template

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
CORS(app) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/')
def index():
    return render_template('uploads3.html', labels=None, detected_image=None)  # Serve the HTML form

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
        print(f"File saved to: {file_path}")

        detected, labels = dc.get_classes(file_path) # returns a jpeg of detected

        detected_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'detected.jpg')

        print(f"Detected image path: {detected_image_path}")

        # Return the labels and the path to the detected image
        print(url_for('uploaded_file', filename='detected.jpg'))
        return jsonify({'labels': labels, 'detected_image': url_for('uploaded_file', filename='detected.jpg')}), 200

        # detected_path = "./uploads/detected.jpg"

        # with open(detected_path, 'wb') as f:
        #     f.write(detected)

        # detected.save(detected_scaled_path)
        # detected_scaled = dc.resize_image(detected, 500, 400)

        #_, buffer = cv2.imencode('.jpg', detected)  # or the appropriate image format
        #detected_image_base64 = base64.b64encode(detected).decode('utf-8')
        #detected_image_base64 = base64.b64encode(detected_scaled).decode('utf-8')

        # Save the JPEG-encoded image to the file path
        
        # return render_template('index.html', detected_image=detected_image_base64, labels=labels)  
        # return jsonify({'message': 'File uploaded successfully', 'filename': file.filename, 'labels': labels, 'detected_image': detected_image_base64}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/uploads/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(port=5000, debug=True)