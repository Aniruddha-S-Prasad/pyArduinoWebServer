import pandas as pd
from pytz import timezone
from matplotlib import pyplot as plt
from matplotlib import dates as mdates

def main():
	weather_data = pd.read_csv('room_weather_2021-12-24.csv')

	weather_data['Timestamp'] = pd.to_datetime(weather_data['Timestamp'], unit='s')

	fig, ax = plt.subplots(figsize=(10,7))
	ax.plot_date(weather_data.Timestamp, weather_data.Temperature, '-b', label='Temperature')
	# ax.plot_date(weather_data.Timestamp, weather_data.HeatIndex, '-r', label='Feels Like')

	timestamp_locator = mdates.AutoDateLocator(minticks=4, maxticks=10)
	timestamp_format = mdates.ConciseDateFormatter(timestamp_locator, tz=timezone('CET'))

	ax.xaxis.set_major_locator(timestamp_locator)
	ax.xaxis.set_major_formatter(timestamp_format)

	plt.ylim((15, 35))

	plt.legend()
	plt.grid(True)
	plt.tight_layout()
	plt.show()


if __name__ == "__main__":
	main()
