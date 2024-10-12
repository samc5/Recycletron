## Simple Flask app to host an AI model
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/model', methods=['POST'])
def run_model():
    print("doing model stuff")

if __name__ == '__main__':
    app.run(port=5000)