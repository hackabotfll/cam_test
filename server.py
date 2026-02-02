from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Store the latest command
latest_command = None

@app.route('/')
def index():
    return send_file('camera_website.html')

@app.route('/api/trigger_alarm_<int:camera_num>', methods=['POST'])
def trigger_alarm(camera_num):
    global latest_command
    if 1 <= camera_num <= 4:
        latest_command = f'trigger_alarm_{camera_num}'
        return jsonify({'status': 'success', 'command': latest_command}), 200
    return jsonify({'status': 'error', 'message': 'Invalid camera number'}), 400

@app.route('/api/clear_alarm_<int:camera_num>', methods=['POST'])
def clear_alarm(camera_num):
    global latest_command
    if 1 <= camera_num <= 4:
        latest_command = f'clear_alarm_{camera_num}'
        return jsonify({'status': 'success', 'command': latest_command}), 200
    return jsonify({'status': 'error', 'message': 'Invalid camera number'}), 400

@app.route('/api/clear_all_alarms', methods=['POST'])
def clear_all_alarms():
    global latest_command
    latest_command = 'clear_all_alarms'
    return jsonify({'status': 'success', 'command': latest_command}), 200

@app.route('/api/commands', methods=['GET'])
def get_commands():
    global latest_command
    command = latest_command
    latest_command = None  # Clear after reading
    return jsonify({'command': command}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
