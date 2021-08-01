import matplotlib.pyplot as plt
import pandas as pd


def read_data(path="", file=""):
    data = pd.read_csv("{}{}".format(path,
                                     file))
    data = format_data(data)
    return data


def format_data(data=pd.DataFrame()):
    data.index = pd.to_datetime(data["Date"])
    data = data.drop("Date", 1)
    return data


def obtain_max_per_hour(data=pd.DataFrame()):
    return data.transpose().max()


def obtain_daily_maximum(data=pd.DataFrame()):
    return data.resample("D").max()


def obtain_xticks(date_i="", date_f="", day_partition=5):

    days = pd.to_datetime(date_f)-pd.to_datetime(date_i)
    days = days.days//day_partition
    xticks = [pd.to_datetime(date_i)]
    for day in range(1, days):
        date = xticks[-1]+pd.Timedelta(days=day_partition)
        xticks.append(date)
    xticks.append(pd.to_datetime(date_f))
    return xticks


parameters = {"path data": "../Data/",
              "file P2.5": "P25_data.csv",
              "file Fire": "NI.csv",
              "date initial": "2021-07-01",
              "date final": "2021-08-01",
              "day partition": 6}

p25_data = read_data(parameters["path data"],
                     parameters["file P2.5"])
p25_data = obtain_max_per_hour(p25_data)
p25_data = obtain_daily_maximum(p25_data)
Fire_data = read_data(parameters["path data"],
                      parameters["file Fire"])
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(p25_data.index, p25_data,
         marker="o",
         label="P$_{2.5}$",
         color="#2a9d8f")
ax1.set_ylim(0)
ax1.set_ylabel("P$_{2.5}$")
ax2.plot(Fire_data.index, Fire_data,
         marker="o",
         label="Incendios",
         color="#d00000")
ax2.set_ylim(0)
ax2.set_ylabel("Número de incendios",
               rotation=-90,
               labelpad=10)
plt.xlim(pd.to_datetime(parameters["date initial"]),
         pd.to_datetime(parameters["date final"]))
xticks = obtain_xticks(parameters["date initial"],
                       parameters["date final"],
                       parameters["day partition"])
plt.xticks(xticks)
fig.legend(frameon=False,
           ncol=2,
           mode="extend",
           #bbox_to_anchor=(0.5, 0., 0.5, 0.5),
           loc='upper center')
plt.show()
