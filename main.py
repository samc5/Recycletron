## Simple Flask app to host an AI model
from flask import Flask, request, jsonify
import os
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
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

        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename}), 201
    else:
        return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(port=5000, debug=True)