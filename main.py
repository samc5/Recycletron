## Simple Flask app to host an AI model
from flask import Flask, request, jsonify, redirect, url_for
import os

from werkzeug.security import generate_password_hash, check_password_hash

import detectron_camera as dc
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import base64
import sqlite3
import cv2
from flask import render_template

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Create a User model for the login system
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, default=0)

# Create the tables (Run this only once, or when you make a change to the models)
with app.app_context():
    db.create_all()

@app.errorhandler(Exception)
def handle_error(error):
    error_message = str(error)
    return render_template('error.html', error_message=error_message), 500

@app.route('/')
def index():
    return render_template('uploads3.html', labels=None, detected_image=None)  # Serve the HTML form

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user by username
        user = User.query.filter_by(username=username).first()

        # Check if user exists and verify the password
        if user and check_password_hash(user.password, password):
            # Successful login, redirect to home or dashboard
            return render_template('uploads3.html')  # Adjust this to your main page
        else:
            return render_template('error.html', error_message='Invalid username or password. Please try again.'), 500
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return render_template('error.html', error_message='The re-entered password doesn\'t match with the previous one'), 500
        # Hash the password before storing
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))  # Redirect to login after signup
        except Exception as e:
            # Render the error page with the error message
            return render_template('error.html', error_message=str(e)), 500
    return render_template('signup.html')


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
        detected, labels = dc.get_classes(file_path)
        print(detected)
        print(labels)
        # _, buffer = cv2.imencode('.jpg', detected)  # or the appropriate image format

        detected_image_base64 = base64.b64encode(detected).decode('utf-8')      
        return render_template('index.html', detected_image=detected_image_base64, labels=labels)  
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename, 'labels': labels, 'detected_image': detected_image_base64}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # This will drop all tables
        db.create_all()  # This will create the tables again
    app.run(host='0.0.0.0')