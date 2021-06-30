import moviepy.video.io.ImageSequenceClip as Movie_maker
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os


class city_list:
    def __init__(self, city=""):
        self.citys = {
            "Parana_2020": {
                "day initial": "2020-06-03",
                "day final": "2020-09-28",
                "lon": [-61, -60],
                "lat": [-33.5, -32.5],
                "delta": 0.25,
            },
            "Parana_2021": {
                "day initial": "2021-05-01",
                "day final": "2021-06-01",
                "lon": [-60.75, -60],
                "lat": [-33.25, -32.5],
                "delta": 0.25,
            },
            "Parana_2021_Jun": {
                "day initial": "2021-06-10",
                "day final": "2021-06-17",
                "lon": [-60.25, -60.0],
                "lat": [-33.25, -33.0],
                "delta": 0.05,
            },
            "Nuevo_Leon": {
                "day initial": "2021-03-01",
                "day final": "2021-04-30",
                "city": "Nuevo_Leon",
                "lon": [-100.50, -99.50],
                "lat": [24.50, 25.50],
                "delta": 0.25,
            },
        }
        self.parameters = {"path data": "../Data/",
                           "file data": "data.csv",
                           "path graphics": "../Graphics/"}
        self.select_city_parameters(city_name=city)

    def select_city_parameters(self, city_name=""):
        self.parameters.update(self.citys[city_name])


class FIRMS_data:
    def __init__(self, parameters={}, select_nominal_data=True):
        self.parameters = parameters
        self.format_dates()
        # Lectura y formateo de los datos
        self.read_data()
        self.cut_data()
        if select_nominal_data:
            self.select_data_from_confidence_data()

    def format_dates(self):
        self.parameters["day initial"] = pd.to_datetime(
            self.parameters["day initial"])
        self.parameters["day final"] = pd.to_datetime(
            self.parameters["day final"])

    def read_data(self):
        """
        Funcion para la lectura de los datos de FIRMS
        """
        data = pd.read_csv("{}{}".format(self.parameters["path data"],
                                         self.parameters["file data"]),
                           usecols=[0, 1, 5, 9])
        self.data = self.format_date_data(data)

    def format_date_data(self, data=pd.DataFrame()):
        """
        Funcion que crea el formato de las fechas y las asigna al indice
        del dataframe
        """
        data.index = pd.to_datetime(data["acq_date"])
        data = data.drop("acq_date", 1)
        return data

    def cut_data(self):
        # Seleccion de los datos en el periodo introducido
        self.cut_data_from_dates()
        # Selección de los datos de acuerdo a el area a analizar
        self.cut_data_from_location()

    def cut_data_from_dates(self):
        """
        Funcion que corta los datos en un periodo de tiempo
        """
        self.data = self.data[self.data.index >=
                              self.parameters["day initial"]]
        self.data = self.data[self.data.index <= self.parameters["day final"]]

    def cut_data_from_location(self):
        """
        Funcion que corta los datos en un intervalo de longitudes y latitudes
        """
        self.data = self.cut_data_from_positions(data=self.data,
                                                 name_position="longitude",
                                                 positions=self.parameters["lon"])
        self.data = self.cut_data_from_positions(data=self.data,
                                                 name_position="latitude",
                                                 positions=self.parameters["lat"])

    def cut_data_from_positions(self, data=pd.DataFrame(), name_position="", positions=[]):
        """
        Funcion que corta los datos en un intervalo de posiciones
        """
        data = data[data[name_position] >= positions[0]]
        data = data[data[name_position] <= positions[1]]
        return data

    def select_data_from_confidence_data(self):
        """
        Selecciona solo un tipo de dato del FIRMS
        """
        self.data = self.data[self.data["confidence"] == "n"]


class Fire_Count:
    def __init__(self, city_name="", select_nominal_data=True, color="white"):
        """
        Conteo de los datos de FIRMS en una localización fijada.
        Parameters
        ----------
        + City_name: Nombre de la ciudad donde se cargaran los parametros
        + select_nominal_data
        + color
        """
        self.obtain_city_parameters(city_name=city_name)
        self.FIRMS_data = FIRMS_data(parameters=self.parameters,
                                     select_nominal_data=select_nominal_data)
        self.color = color

    def obtain_city_parameters(self, city_name=""):
        city_parameters = city_list(city_name)
        self.parameters = city_parameters.parameters

    def create_grids(self):
        """
        Funcion que crea las grillas de biusqueda y realiza la transformacion para el espacio de la imagen
        """
        self.lon_division, self.lon_n = self.delimiter_grids(self.parameters["lon"],
                                                             self.parameters["delta"])
        self.lat_division, self.lat_n = self.delimiter_grids(self.parameters["lat"],
                                                             self.parameters["delta"])
        self.lon_division_tras = self.traslation_positions(self.lon_division,
                                                           self.parameters["lon"],
                                                           self.fig_x)
        self.lat_division_tras = self.traslation_positions(self.lat_division,
                                                           self.parameters["lat"],
                                                           self.fig_y)

    def delimiter_grids(self, pos_points, delta):
        """
        Funcion para obtener el numero de grillas
        """
        pos = np.round(np.arange(pos_points[0], pos_points[1]+delta, delta), 3)
        size = np.size(pos)
        return pos, size

    def traslation_positions(self, pos_data, pos_parameter, resize):
        """
        Funcion para redefinir las posicioness
        """
        resize = resize/abs(pos_parameter[1]-pos_parameter[0])
        n = np.size(pos_data)
        pos_data_tras = np.zeros(n)
        for i in range(n):
            pos_data_tras[i] = (pos_data[i]-pos_parameter[0])*resize
        return pos_data_tras

    def read_map(self, name="map.png"):
        """
        Lectura del mapa de la zona donde se esta realizando el estudio
        """
        self.map = plt.imread("{}{}".format(self.parameters["path graphics"],
                                            name))
        self.fig_y, self.fig_x, _ = np.shape(self.map)
        self.map = np.flipud(self.map)
        self.create_grids()

    def algorithm(self):
        """
        Funcion que realiza el algoritmo de conteo en los distintos archivos e FIRMS y dos formatos de archivos
        NI.csv -----> Conteo de los incencos para distintas fechas
        """
        # Dirección donde se creara la animacion
        self.path_movie = "{}Movie/".format(self.parameters["path graphics"])
        print("Realizando conteo de incendios")
        # Archivo NI
        results_file = open("{}NI.csv".format(self.parameters["path data"]),
                            "w")
        results_file.write("{},{}\n".format("Dates", "NI"))
        dates = self.obtain_dates()
        print("Inicio del conteo del día {} al {}".format(dates[0].date(),
                                                          dates[-1].date()))
        for date in dates:
            # Seleccion de los datos por dia
            data_per_day = self.FIRMS_data.data[self.FIRMS_data.data.index == date]
            data_per_day.to_csv("{}Dates_data/{}.csv".format(self.parameters["path data"],
                                                             date.date()),
                                index=False)
            # Conteo de los incendios para cada grilla
            self.count_fire(data_per_day)
            # Conteo de los incendios para todo el dia
            daily_sum = np.sum(self.count)
            # Escritura de los resultados
            results_file.write("{},{}\n".format(date.date(),
                                                daily_sum))
            # Lectura de la latitud y longitud
            lat = np.array(data_per_day["latitude"])
            lon = np.array(data_per_day["longitude"])
            # Traslacion de las cordenadas hacia el espacio de la imagen
            lon = self.traslation_positions(lon,
                                            self.parameters["lon"],
                                            self.fig_x)
            lat = self.traslation_positions(lat,
                                            self.parameters["lat"],
                                            self.fig_y)
            # Ploteo del numero de incendios por grilla
            self.number_plot(self.lon_division_tras,
                             self.lat_division_tras,
                             self.count,
                             self.color)
            # Ploteo de cada incendio
            self.plot_points(lon,
                             lat)
            # Ploteo del mapa
            self.plot_map(daily_sum,
                          date.date(),
                          self.path_movie)
        results_file.close()

    def count_fire(self, data):
        """
        Algoritmo para el conteo de los incendios en cada grilla
        """
        # Inicializacion del conteo
        self.count = np.zeros([self.lon_n, self.lat_n], dtype=int)
        # Longitud de los datos
        for lon_i in range(self.lon_n-1):
            # Limites de la grilla en la longitud
            lon_j = [self.lon_division[lon_i],
                     self.lon_division[lon_i+1]]
            for lat_i in range(self.lat_n-1):
                # Limites de la grilla en la latitud
                lat_j = [self.lat_division[lat_i],
                         self.lat_division[lat_i+1]]
                # Localizacion de los datos a partir de su longitud
                data_loc = self.FIRMS_data.cut_data_from_positions(data,
                                                                   "longitude",
                                                                   lon_j)
                # Localizacion de los datos a partir de su latitud
                data_loc = self.FIRMS_data.cut_data_from_positions(data_loc,
                                                                   "latitude",
                                                                   lat_j)
                self.count[lon_i, lat_i] = data_loc["latitude"].count()

    def obtain_dates(self):
        days = (self.parameters["day final"] -
                self.parameters["day initial"]).days
        dates = []
        for day in range(days+1):
            date = self.parameters["day initial"]+datetime.timedelta(days=day)
            dates.append(date)
        return dates

    def plot_points(self, lon, lat):
        """
        Funcion para plotear los puntos de cada incendio
        """
        plt.scatter(lon, lat,
                    alpha=1,
                    color="#ff0000",
                    marker=".")

    def plot_map(self, sum, name, path=""):
        """
        Funcion para plotear el mapa y guardar la grafica
        """
        plt.xlabel("Longitud")
        plt.ylabel("Latitud ")
        # Ploteo del mapa
        plt.imshow(self.map)

        plt.title("Date {}\nTotal de incendios: {}".format(name,
                                                           sum))
        # Ploteo de los puntos
        plt.xticks(self.lon_division_tras,
                   self.lon_division)
        plt.yticks(self.lat_division_tras,
                   self.lat_division)
        plt.xlim(self.lon_division_tras[0],
                 self.lon_division_tras[-1])
        plt.ylim(self.lat_division_tras[0],
                 self.lat_division_tras[-1])
        plt.grid(color="black",
                 ls="--")
        plt.savefig("{}{}.png".format(path,
                                      name))
        plt.clf()

    def number_plot(self, lon_list, lat_list, count_list, color):
        """
        Funcion para plotear el numero de incendios, si este es 0, no ploteara nada
        """
        lon_n = np.size(lon_list)
        lat_n = np.size(lat_list)
        for lon_i, counts in zip(range(lon_n-1), count_list):
            # Localizacion en x
            r_lon = (lon_list[lon_i+1]+lon_list[lon_i])/2
            for lat_i, count in zip(range(lat_n-1), counts):
                # Localizacion en y
                r_lat = (lat_list[lat_i+1]+lat_list[lat_i])/2
                if count != 0:
                    # Ploteo del texto
                    plt.text(r_lon, r_lat, str(count),
                             fontsize=12, color=color)

    def create_animation(self, name="Fire", delete=True, fps=3):
        """
        Funcion que ejecuta la creacion de la animacion
        """
        self.create_movie(self.path_movie,
                          name,
                          delete,
                          fps)

    def create_movie(self, path, name, delete_images, fps):
        """
        Funcion que crea el gif a partir de las graficas diarias
        """
        filenames = sorted(os.listdir(path))
        filenames = [path+filename for filename in filenames]
        output_file = "{}{}.mp4".format(path,
                                        name)
        movie = Movie_maker.ImageSequenceClip(filenames,
                                              fps=fps,)
        movie.write_videofile(output_file,
                              logger=None)
        path_original = path.replace("Movie/", "")
        print("Creación del video en {}".format(path_original))
        os.system("mv {}{}.mp4 {}".format(path,
                                          name,
                                          path_original))
        if delete_images:
            os.system("rm {}*.png".format(path))
