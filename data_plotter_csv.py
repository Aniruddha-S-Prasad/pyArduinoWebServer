import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates

def main():
	weather_data = pd.read_csv('databases/room_weather_2021-12-23.csv')

	timestamps = pd.to_datetime(weather_data['Timestamp'], unit='s')

	fig, ax = plt.subplots(figsize=(10,7))
	ax.plot_date(timestamps, weather_data['Temperature'], '-b', label='Temperature')

	timestamp_locator = mdates.AutoDateLocator(minticks=7, maxticks=10)
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
