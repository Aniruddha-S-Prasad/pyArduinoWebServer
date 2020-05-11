import sys
import time
import json
import serial
import sqlite3

database_filename = 'databases/weather_data.db'


def listSerialPorts():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
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

    
def logSensorData():
    serialPorts = listSerialPorts()
    if len(serialPorts) == 0:
        sys.exit('No Serial Ports found. Exiting')

    for index, port in enumerate(serialPorts):
        print(f'{index}. {port}')
    
    selection = input('Please select the COM port corresponding to the attached Arduino Uno device. (Eg: 1, 2, 3 etc)\n')
    
    conn = sqlite3.connect(database_filename)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS data(
            Timestamp INTEGER PRIMARY KEY,
            Temperature REAL,
            Humidity REAL
        )
    ''')
    conn.commit()

    arduinoSerialDevice = serial.Serial(serialPorts[int(selection)], 9600)
    arduinoString = 'Error, No Data'
    arduino_data = {}
    counter = 0
    while True:
        try:
            arduinoStringRaw = arduinoSerialDevice.readline().decode('utf-8')
            current_time_string = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())
            try:
                arduino_data = json.loads(arduinoStringRaw)
            except json.JSONDecodeError:
                print(f'JSON Error at {current_time_string}, probably a serial communication error')
                continue
            
            arduino_data['Timestamp'] = int(time.time())
            c.execute('''
                INSERT INTO data VALUES(
                    :Timestamp,
                    :Temperature,
                    :Humidity
                )
            ''', arduino_data)
            counter = counter + 1
            if counter > 20:
                conn.commit()
                counter = 0
            print(f'At {current_time_string}, the temperature was {arduino_data["Temperature"]} and the humudity was {arduino_data["Humidity"]}')
            # sensorObj.temperature = arduino_data['Temperature']
            # sensorObj.humidity = arduino_data['Humidity']
        except KeyboardInterrupt:
            conn.close()
            print('Exiting ... ')
            sys.exit(0)


if __name__ == "__main__":
    logSensorData()