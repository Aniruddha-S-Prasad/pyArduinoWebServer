import time
import csv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mdate

def main():
    timestamps = []
    temperature = []
    humidity = []
    heat_index = []

    with open('databases/room_climate_2021-11-02_21h42m46s.csv', 'r') as saved_data:
        data_reader = csv.DictReader(saved_data)
        for row in data_reader:
            timestamps.append(int(row['Timestamp']))
            temperature.append(float(row['Temperature']))
            humidity.append(float(row['Humidity']))
            heat_index.append(float(row['HeatIndex']))

    timestamps = np.array(timestamps[0:42000])
    temperature = np.array(temperature[0:42000])
    humidity = np.array(humidity[0:42000])
    heat_index = np.array(heat_index[0:42000])

    factor = 600
    timestamps = np.mean(timestamps.reshape(-1, factor), axis=1)
    temperature = np.mean(temperature.reshape(-1, factor), axis=1)
    humidity = np.mean(humidity.reshape(-1, factor), axis=1)
    heat_index = np.mean(heat_index.reshape(-1, factor), axis=1)

    mpl_timestamps = mdate.epoch2num(timestamps)
    
    fig, ax = plt.subplots()
    ax.plot_date(mpl_timestamps, temperature, '-b', label='Temperature')
    ax.plot_date(mpl_timestamps, heat_index, '-r', label='Heat Index')
    ax.set_ylim((15, 30))    
    date_format = '%H:%M:%S'
    date_formatter = mdate.DateFormatter(date_format)
    ax.xaxis.set_major_formatter(date_formatter)
    fig.autofmt_xdate()

    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()