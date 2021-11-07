import sys, time, glob
import json, csv
import serial

database_filename = 'databases/weather_data.db'


def listSerialPorts() -> list:
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
	serial_ports = listSerialPorts()
	if len(serial_ports) == 0:
		sys.exit('No Serial Ports found. Exiting')

	for index, port in enumerate(serial_ports):
		print(f'{index}. {port}')
	
	selection = int(input('Please select the COM port corresponding to the attached microcontroller device. (Eg: 1, 2, 3 etc)\n'))


	serial_device = serial.Serial(serial_ports[selection], 115200)
	arduino_data = {}
	arduino_data_keys = ['Timestamp', 'Temperature', 'Humidity', 'HeatIndex']
	counter = 0

	file_time_string = time.strftime('%Y-%m-%d_%Hh%Mm%Ss', time.localtime())
	with open('databases/room_climate_' + file_time_string + '.csv', 'w', newline='') as data_file:
		data_writer = csv.DictWriter(data_file, fieldnames=arduino_data_keys)
		data_writer.writeheader()
		
		while True:
			try:
				raw_received_string = serial_device.readline().decode('utf-8')
				current_time_string = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())

				try:
					arduino_data = json.loads(raw_received_string)
					arduino_data['Timestamp'] = int(time.time())
					data_writer.writerow(arduino_data)
				except json.JSONDecodeError:
					print(f'JSON Error at {current_time_string}, probably a serial communication error')
					continue
				
				print(f'At {current_time_string}, the temperature was {arduino_data["Temperature"]} and the humudity was {arduino_data["Humidity"]}')
				
				counter += 1
				if counter % 100 == 0:
					data_file.flush()

			except KeyboardInterrupt:
				break
		
	print('Exiting ... ')
	return


if __name__ == "__main__":
	logSensorData()