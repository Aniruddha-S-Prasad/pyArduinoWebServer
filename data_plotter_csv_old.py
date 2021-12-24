import time
import csv
from datetime import datetime
from pytz import timezone
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mdate

def main():
    timestamps = []
    temperature = []
    humidity = []
    heat_index = []

    with open('databases/room_climate_2021-12-09_09h37m09s.csv', 'r') as saved_data:
        data_reader = csv.DictReader(saved_data)
        for row in data_reader:
            timestamps.append(int(row['Timestamp']))
            temperature.append(float(row['Temperature']))
            humidity.append(float(row['Humidity']))
            heat_index.append(float(row['HeatIndex']))

    timestamps = np.array(timestamps)
    temperature = np.array(temperature)
    humidity = np.array(humidity)
    heat_index = np.array(heat_index)

    # factor = 600
    # timestamps = np.mean(timestamps.reshape(-1, factor), axis=1)
    # temperature = np.mean(temperature.reshape(-1, factor), axis=1)
    # humidity = np.mean(humidity.reshape(-1, factor), axis=1)
    # heat_index = np.mean(heat_index.reshape(-1, factor), axis=1)
    mpl_timestamps = mdate.date2num(np.vectorize(datetime.utcfromtimestamp)(timestamps))
    
    fig, ax = plt.subplots()
    ax.plot_date(mpl_timestamps, temperature, '-b', label='Temperature')
    ax.plot_date(mpl_timestamps, heat_index, '-r', label='Heat Index')
    ax.set_ylim((5, 30))    
    date_format = '%Y-%b-%d %H:%M'
    date_formatter = mdate.DateFormatter(date_format, tz=timezone('CET'))
    ax.xaxis.set_major_formatter(date_formatter)
    fig.autofmt_xdate()

    plt.legend()
    plt.grid()

    fig, ax = plt.subplots()
    ax.plot_date(mpl_timestamps, humidity, '-b', label='Humidity')
    # ax.set_ylim((15, 30))    
    date_format = '%Y-%b-%d %H:%M'
    date_formatter = mdate.DateFormatter(date_format)
    ax.xaxis.set_major_formatter(date_formatter)
    fig.autofmt_xdate()

    plt.legend()
    plt.grid()
    plt.show()
    

if __name__ == "__main__":
    main()