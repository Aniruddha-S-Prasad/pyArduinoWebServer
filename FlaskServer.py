import threading

from flask import Flask, jsonify, send_file

from readArduinoSerial import SensorData, sensor1

app = Flask(__name__)


@app.route('/')
def hello_world():
    return send_file('index.html')


@app.route('/data')
def get_data():
    return jsonify(sensor1.__dict__)


@app.route('/login')
def password_chk():
    sensorDummy = SensorData(25.0, 70.0)

    return str(sensorDummy)


def start_flask_server():
    app.run(host='127.0.0.1', port='8080')


def start_server_thread():
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.start()
