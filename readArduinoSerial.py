import sys
import glob
import threading

import serial


class SensorData:
    def __str__(self) -> str:
        tempStr = 'Temperature: ' + str(self.temperature) + ' Humidity: ' + str(self.humidity)
        return tempStr

    def __init__(self, temperature=0.0, humidity=0.0):
        self.temperature = temperature
        self.humidity = humidity


def listSerialPorts():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def listenSensorData(sensorObj):
    serialPorts = listSerialPorts()
    if len(serialPorts) == 0:
        sys.exit('No Serial Ports found. Exiting')

    print(serialPorts)
    arduinoSerialDevice = serial.Serial(serialPorts[0], 9600)
    arduinoString = 'Error, No Data'

    while True:
        try:
            arduinoStringRaw = arduinoSerialDevice.readline().decode('utf-8')
            arduinoString = arduinoStringRaw.split(',')
            for i in range(len(arduinoString)):
                if arduinoString[i] == 'H':
                    sensorObj.humidity = float(arduinoString[i + 1])
                elif arduinoString[i] == 'T':
                    sensorObj.temperature = float(arduinoString[i + 1])
            print('Temperature: ' + str(sensorObj.temperature) + ' Humidity: ' + str(sensorObj.humidity))
        except KeyboardInterrupt:
            print('Exiting ... ')
            sys.exit(0)


sensor1 = SensorData()


def start_serial_communication_thing():
    arduino_thread = threading.Thread(target=listenSensorData, args=(sensor1,))
    arduino_thread.start()


if __name__ == '__main__':
    sensor1 = SensorData()
    listenSensorData(sensor1)
    pass
