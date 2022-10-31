from Modules.params import get_params
import matplotlib.pyplot as plt
from Modules.functions import (
    obtain_ticks,
    format_data,
)
from pandas import read_csv
from os.path import join
from numpy import arange
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
data = read_csv(filename)
data = format_data(data)
# Extraccion de las fechas seleccionadas
dates = obtain_ticks(data,
                     params["Days separation"])
# Limites de las graficas
plt.subplots_adjust(left=0.121,
                    right=0.952,
                    bottom=0.162,
                    top=0.924)
# Ploteo de los datos
plt.plot(list(data.index), list(data["NI"]),
         color="#9a031e",
         alpha=0.5)
plt.scatter(data.index, list(data["NI"]),
            marker=".",
            c="#9a031e",
            alpha=0.5)
# Limites de las graficas
plt.xlim(dates[0],
         dates[-1])
plt.ylim(0,
         params["Y limit"])
# Etiqueta en el eje y
plt.ylabel("Número de Incendios Acumulados")
# Cambio en las etiquetas de los ejes x y y
plt.xticks(dates,
           rotation=45)
plt.yticks(arange(0,
                  params["Y limit"]+params["Delta y"],
                  params["Delta y"]))
# Creación del grid
plt.grid(ls="--",
         color="grey",
         alpha=0.7)
# Guardado de la grafica
filename = join(params["path graphics"],
                params["graphics file"])
plt.savefig(filename,
            dpi=400)
