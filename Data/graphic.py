import matplotlib.pyplot as plt
import pandas as pd


def format_data(data):
    data.index = pd.to_datetime(data["Dates"])
    data = data.drop("Dates", 1)
    return data


data = pd.read_csv("NIA.csv")
data = format_data(data)
data_real = pd.read_csv("NI_real.csv")
data_real = format_data(data_real)
data_real["NIA"] = data_real["NI"].cumsum()
plt.plot(data.index, data["NIA"])
plt.plot(data_real.index, data_real["NIA"])
plt.show()
