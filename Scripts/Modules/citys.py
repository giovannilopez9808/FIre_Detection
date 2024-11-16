class CityList:
    def __init__(
        self,
        city: str
    ) -> None:
        """
        Contiene los parametros del periodo y zona de análisis de cada región
        ----------------------------
        Inputs:
        + city -> nombre de la ciudad de la cual se cargaran los parámetros

        ----------------------------
        Outouts:
        + self.parameters -> diccionario con los siguientes atributos:
            + day inital -> día inicial del periodo (str)
            + day final -> dia final del periodo (str)
            + lon -> lista con la longitud del área por analizar [float,float]
            + lat -> lista con la latitud del área por analizar [float,float]
            + delta -> divisiones de las grillas del mapa (float)
            + path data -> direccion donde se encuentran los datos
            + file data -> nombre del archivo de datos
            + path graphics -> direccion donde se guardaran las imagenes

        """
        self.parameters = {
            "path data": "../Data/",
            "file data": "data.csv",
            "path graphics": "../Graphics/"
        }
        self.citys = {
            "Parana_2020": {
                "day initial": "2020-06-03",
                "day final": "2020-09-28",
                "lon": [-61, -60],
                "lat": [-33.5, -32.5],
                "delta": 0.25,
            },
            "Parana_2021_May": {
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
            # "Nuevo_Leon_Historic": {
            # "day initial": "2015-01-01",
            # "day final": "2023-12-31",
            # "city": "Nuevo_Leon",
            # "lon": [-100.50, -99.50],
            # "lat": [24.50, 25.50],
            # "delta": 0.25,
            # },
            "Nuevo_Leon_Historic": {
                "day initial": "2012-01-01",
                "day final": "2022-12-31",
                "city": "Nuevo_Leon",
                "lon": [-100.75, -99.50],
                "lat": [24.50, 25.50],
                "delta": 0.25,
            },
        }
        self._get_city_parameters(
            city_name=city
        )

    def _get_city_parameters(
        self,
        city_name: str
    ) -> None:
        """
        Realiza una union del diccionario con las direcciones de los
        datos con el diccionario de los parametros para cada ciudad
        """
        self.parameters.update(
            self.citys[city_name]
        )
