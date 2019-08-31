from FlaskServer import start_server_thread
from readArduinoSerial import start_serial_communication_thing

if __name__ == '__main__':
    start_server_thread()
    start_serial_communication_thing()
