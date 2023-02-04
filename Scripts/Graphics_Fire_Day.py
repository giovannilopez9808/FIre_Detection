from matplotlib import pyplot as plt
from Class_list import city_list
from numpy import (
    arange,
    append,
)
from pandas import (
    to_datetime,
    DataFrame,
    read_csv,
)


def obtain_ticks(data: DataFrame, day_separation: int = 7):
    """
    Función que prepara dos arrays para renombrar las
    etiquetas del eje x de la grafica con las fechas
    """
    # Longitud de datos
    data_len = data["NI"].count()
    # Separación de fechas a imprimir
    loc = arange(0,
                 data_len,
                 day_separation)
    # Si no se encuentra la ultima fecha agregarla
    if data.index[loc[-1]] != data.index[data_len-1]:
        loc = append(loc, data_len-1)
    # Obtener las fechas seleccionadas
    dates = list(data.index[loc])
    dates_str = [
        date.strftime("%m-%d")
        for date in dates
    ]
    return dates, dates_str


def format_data(data: DataFrame):
    """
    Aplica el formato de fecha a la columna Dates y la agrega al
    indice del dataframe
    """
    data.index = to_datetime(data["Dates"])
    data = data.drop(
        columns="Dates"
    )
    return data


parameters = {
    "file data": "NI.csv",
    "graphics file": "Fire_Per_Day.png",
    "City name": "Nuevo_Leon",
    "Days separation": 5,
    "Y limit": 280,
    "Delta y": 20,
}
# Lectura de los parametros de cada ciudad
city = city_list(city=parameters["City name"])
# Lectura de los datos
data = read_csv("{}{}".format(city.parameters["path data"],
                              parameters["file data"]))
data = format_data(data)
data = data[data.index >= "2021-03-11"]
# Extraccion de las fechas seleccionadas
dates, dates_str = obtain_ticks(
    data,
    parameters["Days separation"]
)
plt.subplots(
    figsize=(10, 8)
)
# Ploteo de los datos
plt.plot(
    data["NI"],
    color="#9a031e",
)
plt.scatter(
    data.index,
    data["NI"],
    marker=".",
    c="#9a031e",
)
# Limites de las graficas
plt.xlim(
    dates[0],
    dates[-1]
)
plt.ylim(
    0,
    parameters["Y limit"]
)
# Etiqueta en el eje y
plt.xlabel(
    "Year 2021"
)
plt.ylabel(
    "Number of active fire per day"
)
# Cambio en las etiquetas de los ejes x y y
plt.xticks(
    dates,
    dates_str,
)
plt.yticks(
    arange(0,
           parameters["Y limit"]+parameters["Delta y"],
           parameters["Delta y"])
)
# Creación del grid
plt.grid(
    ls="--",
    color="grey",
    alpha=0.7
)
plt.tight_layout()
# Guardado de la grafica
plt.savefig("{}{}".format(city.parameters["path graphics"],
                          parameters["graphics file"]),
            dpi=400)
