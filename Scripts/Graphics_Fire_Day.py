import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def obtain_ticks(data, day_separation):
    """
    Función que prepara dos arrays para renombrar las
    etiquetas del eje x de la grafica con las fechas
    """
    # Longitud de datos
    data_len = data["NI"].count()
    # Separación de fechas a imprimir
    loc = np.arange(0,
                    data_len,
                    day_separation)
    # Si no se encuentra la ultima fecha agregarla
    if data.index[loc[-1]] != data.index[data_len-1]:
        loc = np.append(loc, data_len-1)
    # Obtener las fechas seleccionadas
    dates = list(data.index[loc])
    return dates


def format_data(data):
    data.index = pd.to_datetime(data["Dates"]).dt.strftime("%d-%b")
    data = data.drop("Dates", 1)
    return data


inputs = {
    "path data": "../Data/",
    "path graphics": "../Graphics/",
    "file data": "NI.csv",
    "graphics file": "Fire_Per_Day.png",
    "city": "Nuevo_Leon",
    "Days separation": 7,
}
# Lectura de los datos
data = pd.read_csv("{}{}/{}".format(inputs["path data"],
                                    inputs["city"],
                                    inputs["file data"]))
data = format_data(data)
# Extraccion de las fechas seleccionadas
dates = obtain_ticks(data,
                     inputs["Days separation"])
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
plt.ylim(0, 300)
# Etiqueta en el eje y
plt.ylabel("Número de Incendios")
# Cambio en las etiquetas de los ejes x y y
plt.xticks(dates,
           rotation=45)
plt.yticks(np.arange(0,
                     300+25,
                     25))
# Creación del grid
plt.grid(ls="--",
         color="grey",
         alpha=0.7)
# Guardado de la grafica
plt.savefig("{}{}/{}".format(inputs["path graphics"],
                             inputs["city"],
                             inputs["graphics file"]),
            dpi=400)
