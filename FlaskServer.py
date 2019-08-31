import threading

from flask import Flask, jsonify

from readArduinoSerial import SensorData, sensor1

app = Flask(__name__)


@app.route('/')
def hello_world():
    return str(sensor1)

@app.route('/login')
def password_chk():
    sensorDummy = SensorData(25.0, 70.0)

    return str(sensorDummy)

def start_flask_server():
    app.run(host='0.0.0.0', port='80')


def start_server_thread():
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.start()
