import matplotlib.pyplot as plt
from pandas import read_csv
params = {
    "day initial": "2022-08-01",
    "day final": "2022-08-31",
    "lon": [-60.25, -60.0],
    "lat": [-33.25, -33.0],
    "delta": 0.05,
}

data = read_csv(
    "data.csv",
    index_col="acq_date",
    parse_dates=True,
    low_memory=False,
)
daily_data = data.loc["2022-08-19"]
daily_data = daily_data[daily_data["latitude"] >= params["lat"][0]]
daily_data = daily_data[daily_data["latitude"] <= params["lat"][1]]
daily_data = daily_data[daily_data["longitude"] >= params["lon"][0]]
daily_data = daily_data[daily_data["longitude"] <= params["lon"][1]]
daily_data = daily_data[daily_data["type"] == 0]
plt.scatter(
    daily_data["longitude"],
    daily_data["latitude"],
)
plt.show()
print(daily_data)
