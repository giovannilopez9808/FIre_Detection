from pandas import (
    to_datetime,
    DataFrame,
)
from numpy import (
    append,
    arange,
)


def obtain_ticks(data: DataFrame,
                 day_separation: int = 7) -> list:
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
    return dates


def format_data(data: DataFrame) -> DataFrame:
    """
    Aplica el formato de fecha a la columna Dates y la agrega al
    indice del dataframe
    """
    data.index = to_datetime(data["Dates"])
    data = data.drop(columns="Dates")
    return data
