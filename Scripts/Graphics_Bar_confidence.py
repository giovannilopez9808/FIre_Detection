from Class_list import *


def count_data_confidence(data):
    """
    Funcion que calcula el porcentaje de valores para cada tipo de dato
    """
    count_confidence = data.groupby("confidence").count()
    total = count_confidence.sum()
    count_confidence = count_confidence/total*100
    count_confidence = count_confidence["latitude"]
    return count_confidence


def autolabel(ax, rects):
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


inputs = {
    "graphics name": "Bar_Confidence_percentage.png",
    "City name": "Nuevo Leon",
}
# Lectura de los parametros de cada ciudad
citys = city_list()
parameters = citys.select_city_parameters(inputs["City name"])
# Lectura de los datos de FIRMS
FIRMS = FIRMS_data(parameters["path data"],
                   parameters["file data"],
                   parameters["lon"],
                   parameters["lat"],
                   parameters["day initial"],
                   parameters["day final"])
# Conteo de datos para cada tipo de dato
count_confidence = count_data_confidence(FIRMS.data)
# Ploteo de cada columna
fig, ax = plt.subplots()
rect = ax.bar(count_confidence.index, count_confidence, 0.75)
autolabel(ax, rect)
rect[0].set_color("#22577a")
rect[1].set_color("#38a3a5")
rect[2].set_color("#57cc99")
ax.set_ylim(0, 100)
ax.set_ylabel("Frecuencia de intervalo de confianza (%)")
ax.set_xlabel("nivel de confianza")
plt.savefig("{}{}/{}".format(parameters["path graphics"],
                             parameters["city"],
                             inputs["graphics name"]))
