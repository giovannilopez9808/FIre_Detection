from Modules.params import get_params
from Modules.firms import FIRMSData
import matplotlib.pyplot as plt
from pandas import DataFrame
from os.path import join


def count_data_confidence(data: DataFrame) -> DataFrame:
    """
    Funcion que calcula el porcentaje de valores para cada tipo de dato
    """
    count_confidence = data.groupby("confidence").count()
    total = count_confidence.sum()
    count_confidence = count_confidence/total*100
    count_confidence = count_confidence["latitude"]
    return count_confidence


def autolabel(ax: plt.subplot,
              rects: plt.bar) -> None:
    """
    Funcion que grafica los valores de cada barra
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',)


params = get_params()
params.update({
    "graphics name": "Bar_Confidence_percentage.png",
    "city_name": "Parana_2020",
})
# Lectura de los datos de FIRMS
FIRMS = FIRMSData(params=params,
                  only_nominal_data=False)
# Conteo de datos para cada tipo de dato
count_confidence = count_data_confidence(FIRMS.data)
# Ploteo de cada columna
fig, ax = plt.subplots()
rect = ax.bar(count_confidence.index,
              count_confidence,
              0.75)
autolabel(ax, rect)
rect[0].set_color("#22577a")
rect[1].set_color("#38a3a5")
rect[2].set_color("#57cc99")
ax.set_ylim(0, 100)
ax.set_ylabel("Frecuencia de intervalo de confianza (%)")
ax.set_xlabel("nivel de confianza")
filename = join(params["path graphics"],
                params["graphics name"])
plt.savefig(filename)
