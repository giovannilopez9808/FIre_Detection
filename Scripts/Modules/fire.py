import moviepy.video.io.ImageSequenceClip as MovieMaker
import matplotlib.pyplot as plt
from datetime import timedelta
from .firms import FIRMSData
from .citys import CityList
from os.path import join
from numpy import (
    flipud,
    arange,
    array,
    zeros,
    shape,
    round,
    size,
    sum,
)
from os import (
    listdir,
    system
)


class FireCount:
    def __init__(
        self,
        city_name: str,
        only_nominal_data: bool,
        color: str
    ) -> None:
        """
        Conteo de los datos de FIRMS en una localización fijada.
        Parameters
        ----------
        # Inputs
        + City_name -> Nombre de la ciudad donde se cargaran los parametros
        + select_nominal_data -> valor para seleccionar solamente los
                                datos de tipo nominal
        + color -> color del numero por imprimir en las graficas
        ---------
        """
        self.lat_division_tras = None
        self.lon_division_tras = None
        self.lon_division = None
        self.lat_division = None
        self.path_movie = None
        self.lon_n = None
        self.lat_n = None
        self.hape = None
        self.fig_x = None
        self.fig_y = None
        self.map = None
        self._get_city_parameters(
            city_name=city_name
        )
        self.FIRMS_data = FIRMSData(
            params=self.params,
            only_nominal_data=only_nominal_data
        )
        self.color = color

    def _get_city_parameters(
        self,
        city_name: str
    ) -> None:
        """
        Selecciona los parametros dependiendo del nombre de la ciudad
        """
        city_parameters = CityList(
            city_name
        )
        self.params = city_parameters.parameters

    def _read_map(self,
                  name: str = "map.png") -> None:
        """
        Lectura del mapa de la region donde se esta realizando el estudio
        """
        # Lectura de la imagen
        filename = join(
            self.params["path graphics"],
            name
        )
        self.map = plt.imread(
            filename
        )
        # Obtener las dimensiones de la imagen en pixeles
        self.fig_y, self.fig_x, _ = shape(
            self.map
        )
        # Reflexion vertical de la imagen
        self.map = flipud(
            self.map
        )
        # Calculo de las grillas de la region por analizar
        self._create_grids()

    def _create_grids(
        self
    ) -> None:
        """
        Funcion que crea las grillas de busqueda y realiza la
        transformacion para el espacio de la imagen
        """
        self.lon_division, self.lon_n = self._delimiter_grids(
            self.params["lon"],
            self.params["delta"]
        )
        self.lat_division, self.lat_n = self._delimiter_grids(
            self.params["lat"],
            self.params["delta"]
        )
        self.lon_division_tras = self._traslation_positions(
            self.lon_division,
            self.params["lon"],
            self.fig_x
        )
        self.lat_division_tras = self._traslation_positions(
            self.lat_division,
            self.params["lat"],
            self.fig_y
        )

    def _delimiter_grids(
        self,
        pos_points: list,
        delta: float = 0.25
    ) -> tuple:
        """
        Funcion para obtener el numero de grillas
        """
        pos = round(
            arange(
                pos_points[0],
                pos_points[1]+delta,
                delta
            ),
            3
        )
        data_size = size(
            pos
        )
        return pos, data_size

    def _traslation_positions(
        self,
        pos_data: list,
        pos_parameter: list,
        resize: int = 500
    ) -> array:
        """
        Funcion para redefinir las posiciones de las longitudes y
        latitudes al espacio de la imagen
        """
        resize = resize/abs(pos_parameter[1]-pos_parameter[0])
        n = size(pos_data)
        pos_data_tras = zeros(n)
        for i in range(n):
            pos_data_tras[i] = (pos_data[i]-pos_parameter[0])*resize
        return pos_data_tras

    def run(self) -> None:
        """
        Funcion que realiza el algoritmo de conteo en los distintos archivos
        e FIRMS y dos formatos de archivos

        NI.csv -----> Conteo de los incencos para distintas fechas
        """
        self._read_map()
        # Dirección donde se creara la animacion
        self.path_movie = join(
            self.params["path graphics"],
            "Movie"
        )
        print(
            "Realizando conteo de incendios"
        )
        # Archivo NI
        filename = join(
            self.params["path data"],
            "NI.csv"
        )
        results_file = open(
            filename,
            "w"
        )
        results_file.write("{},{}\n".format("Dates", "NI"))
        dates = self._get_dates()
        data = self.FIRMS_data.data
        date_i = dates[0].date()
        date_f = dates[-1].date()
        print(
            f"Inicio del conteo del día {date_i} al {date_f}"
        )
        for date in dates:
            # Seleccion de los datos por dia
            daily_data = data[data.index == date]
            filename = f"{date.date()}.csv"
            filename = join(self.params["path data"],
                            "Daily_data",
                            filename)
            daily_data.to_csv(
                filename,
                index=False
            )
            # Conteo de los incendios para cada grilla
            count = self._count_fire(
                daily_data
            )
            # Conteo de los incendios para todo el dia
            daily_sum = sum(count)
            # Escritura de los resultados
            results_file.write(
                "{},{}\n".format(
                    date.date(),
                    daily_sum
                )
            )
            # Lectura de la latitud y longitud
            lat = array(daily_data["latitude"])
            lon = array(daily_data["longitude"])
            # Traslacion de las cordenadas hacia el espacio de la imagen
            lon = self._traslation_positions(
                lon,
                self.params["lon"],
                self.fig_x
            )
            lat = self._traslation_positions(
                lat,
                self.params["lat"],
                self.fig_y
            )
            # Ploteo del numero de incendios por grilla
            self._number_plot(
                self.lon_division_tras,
                self.lat_division_tras,
                count,
                self.color
            )
            # Ploteo de cada incendio
            self._plot_points(lon,
                              lat)
            # Ploteo del mapa
            self._plot_map(
                daily_sum,
                date.date(),
                self.path_movie
            )
        results_file.close()

    def _count_fire(
        self,
        data: array
    ) -> array:
        """
        Algoritmo para el conteo de los incendios en cada grilla
        """
        # Inicializacion del conteo
        count = zeros([self.lon_n,
                       self.lat_n],
                      dtype=int)
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
                data_loc = self.FIRMS_data.get_data_from_positions(
                    data,
                    "longitude",
                    lon_j
                )
                # Localizacion de los datos a partir de su latitud
                data_loc = self.FIRMS_data.get_data_from_positions(
                    data_loc,
                    "latitude",
                    lat_j
                )
                count[lon_i, lat_i] = data_loc["latitude"].count()
        return count

    def _get_dates(self) -> list:
        """
        Obtiene las fechas consecutivas en el periodo
        """
        days = (self.params["day final"] - self.params["day initial"]).days
        dates = list()
        for day in range(days+1):
            date = self.params["day initial"]+timedelta(days=day)
            dates.append(date)
        return dates

    def _plot_points(
        self,
        lon: array,
        lat: array
    ) -> None:
        """
        Funcion para plotear los puntos de cada incendio
        """
        plt.scatter(
            lon,
            lat,
            alpha=1,
            color="#ff0000",
            marker="."
        )

    def _plot_map(
        self,
        sum_number: int,
        name: str,
        path: str
    ) -> None:
        """
        Funcion para plotear el mapa y guardar la grafica
        """
        plt.xlabel(
            "Longitude"
        )
        plt.ylabel(
            "Latitude"
        )
        # Ploteo del mapa
        plt.imshow(self.map)

        plt.title(
            "Date {}\nCounting of active fires: {}".format(
                name,
                sum_number,
            )
        )
        # Cambio en las ticks de cada eje
        plt.xticks(
            self.lon_division_tras,
            self.lon_division
        )
        plt.yticks(
            self.lat_division_tras,
            self.lat_division
        )
        plt.xlim(
            self.lon_division_tras[0],
            self.lon_division_tras[-1]
        )
        plt.ylim(
            self.lat_division_tras[0],
            self.lat_division_tras[-1]
        )
        # Ploteo de el grid
        plt.grid(
            color="black",
            ls="--"
        )
        # Guardado de la imagen
        filename = f"{name}.png"
        filename = join(
            path,
            filename
        )
        plt.savefig(
            filename,
            dpi=400
        )
        plt.clf()
        plt.close()

    def _number_plot(
        self,
        lon_list: list,
        lat_list: list,
        count_list: list,
        color: str = "white"
    ) -> None:
        """
        Funcion para plotear el numero de incendios, si es 0
        no ploteara nada
        """
        lon_n = size(lon_list)
        lat_n = size(lat_list)
        for lon_i, counts in zip(range(lon_n-1),
                                 count_list):
            # Localizacion en x
            r_lon = (lon_list[lon_i+1]+lon_list[lon_i])/2
            for lat_i, count in zip(range(lat_n-1),
                                    counts):
                # Localizacion en y
                r_lat = (lat_list[lat_i+1]+lat_list[lat_i])/2
                if count != 0:
                    # Ploteo del texto
                    plt.text(
                        r_lon,
                        r_lat,
                        str(count),
                        fontsize=12,
                        color=color
                    )

    def create_animation(
        self,
        name: str = "Fire",
        delete: bool = True,
        fps: int = 3
    ) -> None:
        """
        Funcion que ejecuta la creacion de la animacion
        """
        self.path_movie = "../Graphics/Movie"
        filenames = sorted(listdir(self.path_movie))
        filenames = [
            join(
                self.path_movie,
                filename
            )
            for filename in filenames
        ]
        output_file = f"{name}.mp4"
        output_file = join(
            self.params["path graphics"],
            output_file
        )
        movie = MovieMaker.ImageSequenceClip(
            filenames,
            fps=fps,
        )
        movie.write_videofile(
            output_file,
            logger=None
        )
        print(
            "Creación del video en {}".format(
                self.params["path graphics"]
            )
        )
        if delete:
            system("rm {}*.png".format(self.path_movie))
