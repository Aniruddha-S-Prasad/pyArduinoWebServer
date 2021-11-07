import time
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

def main():
    db_con = sqlite3.connect('databases/weather_data.db')
    db_cur = db_con.cursor()
    db_cur.execute('SELECT Temperature, Humidity FROM data')
    data = np.array(db_cur.fetchall())
    db_cur.execute('SELECT Timestamp FROM data')
    timestamps = np.array(db_cur.fetchall())
    timestamps += 3600 + 3600
    db_con.close()

    mplTimestamps = mdate.epoch2num(timestamps)
    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.plot_date(mplTimestamps, data[:, 0], '-')
    date_format = '%H:%M:%S'
    date_formatter = mdate.DateFormatter(date_format)
    ax1.xaxis.set_major_formatter(date_formatter)
    ax1.set_ylim([10.0, 30.0])

    ax2.plot_date(mplTimestamps, data[:, 1], '-')
    ax2.xaxis.set_major_formatter(date_formatter)
    ax2.set_ylim([20, 60])

    fig.autofmt_xdate()
    ax1.grid(True)
    ax2.grid(True)
    plt.show()

if __name__ == "__main__":
    main()