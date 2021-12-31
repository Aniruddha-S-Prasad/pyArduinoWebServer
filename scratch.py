import numpy as np
import pandas as pd

from bokeh.plotting import figure, show

def main():
	x = np.linspace(0, 2*np.pi*7.5, 10000)
	y = np.sin(x) + np.cos(x)

	weather_data = pd.read_csv('databases/room_weather_2021-12-24.csv')

	weather_data['Timestamp'] = pd.to_datetime(weather_data['Timestamp'], unit='s')

	wave_fig  = figure(title='Room Temperature', 
		x_axis_label='Time',
		x_axis_type='datetime',
		y_axis_label='Temperature',
		plot_width=1400, plot_height=700)
	wave_fig.line(weather_data.Timestamp, weather_data.Temperature, 
		legend_label='Temp', 
		line_width=2)
	show(wave_fig)

if __name__ == "__main__":
	main()
