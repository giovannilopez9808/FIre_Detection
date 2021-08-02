import pandas as pd
import os


def read_data(path="", file="", column=""):
    data = pd.read_csv("{}{}".format(path,
                                     file))
    data = format_data(data,
                       column)
    return data


def format_data(data=pd.DataFrame(), column=""):
    data.index = pd.to_datetime(data["Time"])
    columns = data.columns
    columns = columns.drop(column)
    data = data.drop(columns, 1)
    return data


def obtain_daily_accumulative(data=pd.DataFrame(), column=""):
    return data[column][data.index[-1]]


parameters = {"path data": "../Data/Precipitation/",
              "path results": "../Data/",
              "column data": "Rainfall Rainfall Event(mm)",
              "file results": "Precipitation_accumulative.csv"}
files = sorted(os.listdir(parameters["path data"]))
results = open("{}{}".format(parameters["path results"],
                             parameters["file results"]),
               "w")
results.write("Date,Precipitation\n")
for file in files:
    date = file.replace(".csv", "")
    data = read_data(parameters["path data"],
                     file,
                     parameters["column data"])
    data = obtain_daily_accumulative(data,
                                     parameters["column data"])
    results.write("{},{}\n".format(date,
                                   data))
results.close()
