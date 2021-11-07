import sys
import glob
import json
import threading

import serial


class SensorData:
	def __str__(self) -> str:
		return 'Temperature: ' + str(self.temperature) + ' Humidity: ' + str(self.humidity)

	def __init__(self, temperature=0.0, humidity=0.0):
		self.temperature = temperature
		self.humidity = humidity


def list_serial_ports():
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


def listen_sensor_data(sensorObj):
	serial_ports = list_serial_ports()
	if len(serial_ports) == 0:
		sys.exit('No Serial Ports found. Exiting')
	
	for index, port in enumerate(serial_ports):
		print(f'{index}. {port}')
	
	selection = int(input('Please select the COM port corresponding to the attached microcontroller device. (Eg: 1, 2, 3 etc)\n'))
	baudrate = int(input('Please input the baudrate of the attached device\n'))

	serial_device = serial.Serial(serial_ports[selection], baudrate)
	raw_string = 'Error, No Data'

	while True:
		try:
			raw_string = serial_device.readline().decode('utf-8')
			data_point = json.loads(raw_string)
			sensorObj.temperature = data_point['Temperature']
			sensorObj.humidity = data_point['Humidity']
			print(sensorObj)
		except KeyboardInterrupt:
			print('Exiting ... ')
			sys.exit(0)

sensor1 = SensorData()
def start_serial_communication_thread():
	
	arduino_thread = threading.Thread(target=listen_sensor_data, args=(sensor1,))
	arduino_thread.start()


if __name__ == '__main__':
	sensor1 = SensorData()
	listen_sensor_data(sensor1)
	pass
