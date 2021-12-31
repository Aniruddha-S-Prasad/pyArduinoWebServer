import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import dates as mdates

def main():
	weather_data = np.genfromtxt('room_weather_2021-12-31.csv', delimiter=',', names=True)
	timestamps = [datetime.fromtimestamp(i) for i in weather_data['Timestamp']]

	fig, ax = plt.subplots(figsize=(10,7))
	ax.plot(timestamps, weather_data['Temperature'], '-b', label='Temperature')
	ax.plot(timestamps, weather_data['HeatIndex'], '-r', label='Feels Like')

	timestamp_locator = mdates.AutoDateLocator(minticks=4, maxticks=10)
	timestamp_format = mdates.ConciseDateFormatter(timestamp_locator)

	ax.xaxis.set_major_locator(timestamp_locator)
	ax.xaxis.set_major_formatter(timestamp_format)

	plt.ylim((15, 35))

	plt.legend()
	plt.grid(True)
	plt.tight_layout()
	plt.show()


if __name__ == "__main__":
	main()
