import sys, time, glob, os.path
from datetime import date, timedelta
import pandas as pd
import json
import serial


def listSerialPorts() -> list:
	""" Lists serial port names

		raises: EnvironmentError
			On unsupported or unknown platforms
		returns:
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
			serial_handle = serial.Serial(port)
			serial_handle.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result

def create_new_database_file():
	weather_data_keys = ['Temperature', 'Humidity', 'HeatIndex', 'Timestamp']

	file_date_string = time.strftime('%Y-%m-%d', time.localtime())
	database_filename = 'databases/room_weather_' + file_date_string + '.csv'

	if not os.path.isfile(database_filename):
		weather_dataframe = pd.DataFrame(columns=weather_data_keys)
		weather_dataframe.to_csv(database_filename, mode='w', index=False)
		print('Created new file on ' + file_date_string)


def logSensorData():
	start_day = date.today()

	current_day = date.today()
	previous_day = date.today()

	serial_ports = listSerialPorts()
	if len(serial_ports) == 0:
		sys.exit('No Serial Ports found. Exiting')

	for index, port in enumerate(serial_ports):
		print(f'{index}. {port}')
	
	selection = int(input('Please select the serial port corresponding to the attached microcontroller device. (Eg: 1, 2, 3 etc)\n'))

	serial_device = serial.Serial(serial_ports[selection], 115200)

	file_date_string = time.strftime('%Y-%m-%d', time.localtime())
	database_filename = 'databases/room_weather_' + file_date_string + '.csv'

	create_new_database_file()

	while True:
		current_day = date.today()
		
		if current_day == previous_day:
			pass
		elif (current_day - previous_day) == timedelta(days=1):
			create_new_database_file()
			previous_day = date.today()

		elif (current_day - previous_day) > timedelta(days=1):
			raise RuntimeError('Seems that one day or more has been skipped!!')

		elif (current_day - previous_day) < timedelta(days=0):
			raise RuntimeError('How is this even possible?!, current day is before start day?')

		try:
			weather_data_keys = ['Temperature', 'Humidity', 'HeatIndex', 'Timestamp']
			weather_dataframe = pd.DataFrame(columns=weather_data_keys)
			weather_data = []
			for ctr in range(5):

					serial_device.flushInput()
					raw_received_string = serial_device.readline().decode('utf-8')
					current_time_string = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())

					try:
						weather_datapoint = json.loads(raw_received_string)
						weather_datapoint['Timestamp'] = int(time.time())
						weather_data.append(weather_datapoint)
					except json.JSONDecodeError:
						print(f'JSON Error at {current_time_string}, probably a serial communication error')
						continue
					
					print(f'At {current_time_string}, the temperature was {weather_datapoint["Temperature"]} and the humudity was {weather_datapoint["Humidity"]}')
					# time.sleep(15)
					 
			weather_dataframe = pd.DataFrame(weather_data)
			weather_dataframe.to_csv(database_filename, mode='a', header=False, index=False)
			
			weather_dataframe.drop(weather_dataframe.index, inplace=True)
		except KeyboardInterrupt:
			weather_dataframe = pd.DataFrame(weather_data)
			weather_dataframe.to_csv(database_filename, mode='a', header=False, index=False)
			break
		
	print('Exiting ... ')
	return


if __name__ == "__main__":
	logSensorData()