from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'OK'}), 200

def start_flask():
    app.run(host='0.0.0.0', port=8000)
