from Class_list import city_list
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def obtain_ticks(data=pd.DataFrame(), day_separation=7):
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


def format_data(data=pd.DataFrame()):
    """
    Aplica el formato de fecha a la columna Dates y la agrega al indice del dataframe
    """
    data.index = pd.to_datetime(data["Dates"])
    data = data.drop(columns="Dates")
    return data


parameters = {
    "file data": "NI.csv",
    "graphics file": "Fire_Per_Day.png",
    "City name": "Parana_2022_Ago",
    "Days separation": 6,
    "Y limit": 500,
    "Delta y": 50,
}
# Lectura de los parametros de cada ciudad
city = city_list(city=parameters["City name"])
# Lectura de los datos
data = pd.read_csv("{}{}".format(city.parameters["path data"],
                                 parameters["file data"]))
data = format_data(data)
# Extraccion de las fechas seleccionadas
dates = obtain_ticks(data,
                     parameters["Days separation"])
plt.subplots(figsize=(8, 4))
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
         parameters["Y limit"])
# Etiqueta en el eje y
plt.ylabel("Número de focos de incendios diarios")
# Cambio en las etiquetas de los ejes x y y
plt.xticks(dates,
           rotation=45)
plt.yticks(np.arange(0,
                     parameters["Y limit"]+parameters["Delta y"],
                     parameters["Delta y"]))
# Creación del grid
plt.grid(ls="--",
         color="grey",
         alpha=0.7)
plt.tight_layout()
# Guardado de la grafica
plt.savefig("{}{}".format(city.parameters["path graphics"],
                          parameters["graphics file"]),
            dpi=400)
