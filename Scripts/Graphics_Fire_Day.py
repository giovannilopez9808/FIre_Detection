from Modules.params import get_params
import matplotlib.pyplot as plt
from Modules.functions import (
    obtain_ticks,
    format_data,
)
from os.path import join
from numpy import arange
from pandas import (
    to_datetime,
    read_csv,
)
params = get_params()
params.update({
    "file data": "NI.csv",
    "graphics file": "Fire_Per_Day.png",
    "City name": "Parana_2021_Jun",
    "Days separation": 1,
    "Y limit": 12,
    "Delta y": 2,
})
# Lectura de los datos
filename = join(params["path data"],
                params["file data"])
data = read_csv(filename,
                index_col=0,
                parse_dates=True)
dates = data.index
years = [date.year
         for date in dates]
years = sorted(list(set(years)))
years.append(
    years[-1]+1
)
dates_tick = [to_datetime(f"{year}-01-01")
              for year in years]
plt.subplots(figsize=(10, 6))
# Ploteo de los datos
plt.plot(dates,
         data["NI"],
         color="#9a031e",
         alpha=0.5)
plt.scatter(dates,
            data["NI"],
            marker=".",
            c="#9a031e",
            alpha=0.5)
plt.xlabel("Año")
# Limites de las graficas
plt.xlim(dates_tick[0],
         dates_tick[-1])
plt.ylim(0,
         500)
plt.xticks(
    dates_tick,
    years
)
# Etiqueta en el eje y
plt.ylabel("Número de Incendios diarios")
# Creación del grid
plt.grid(ls="--",
         color="grey",
         alpha=0.7)
# Guardado de la grafica
filename = join(params["path graphics"],
                params["graphics file"])
plt.tight_layout()
plt.savefig(filename,
            dpi=400)
