from os.path import join
from pandas import (
    to_datetime,
    DataFrame,
    read_csv
)


class FIRMSData:
    def __init__(self,
                 params: dict,
                 only_nominal_data: bool) -> None:
        self.data = None
        self.params = params
        self._format_dates()
        # Lectura y formateo de los datos
        self._read_data()
        self._get_data()
        if only_nominal_data:
            self._get_data_by_confidence_level()

    def _format_dates(self) -> None:
        """
        Aplica el formato de fecha a los parametros day initial y day final
        """
        self.params["day initial"] = to_datetime(
            self.params["day initial"]
        )
        self.params["day final"] = to_datetime(
            self.params["day final"]
        )

    def _read_data(self):
        """
        Funcion para la lectura de los datos de FIRMS
        """
        filename = join(self.params["path data"],
                        self.params["file data"])
        data = read_csv(filename)
        self.data = self._format_date_data(data)

    def _format_date_data(self,
                          data=DataFrame) -> DataFrame:
        """
        Funcion que realiza el formato en las fechas y las asigna al indice del
        dataframe
        """
        data.index = to_datetime(data["acq_date"])
        data = data.drop(columns="acq_date")
        return data

    def _get_data(self) -> None:
        """
        Selecciona los datos a partir tomando en cuenta el periodo de
        analisis y la localizacion
        """
        # Seleccion de los datos en el periodo introducido
        self._get_data_from_period()
        # Selección de los datos de acuerdo a el area a analizar
        self._get_data_from_location()
        # get only type 0
        self._get_data_type_0()

    def _get_data_from_period(self) -> None:
        """
        Funcion que selecciona los datos en un periodo de tiempo
        """
        date_i = self.params["day initial"]
        date_f = self.params["day final"]
        self.data = self.data[self.data.index >= date_i]
        self.data = self.data[self.data.index <= date_f]

    def _get_data_from_location(self):
        """
        Funcion que seleciona los datos en un a partir de la localización
        """
        self.data = self.get_data_from_positions(
            data=self.data,
            name_position="longitude",
            positions=self.params["lon"]
        )
        self.data = self.get_data_from_positions(
            data=self.data,
            name_position="latitude",
            positions=self.params["lat"]
        )

    def get_data_from_positions(self,
                                data: DataFrame,
                                name_position: str,
                                positions: list) -> DataFrame:
        """
        Funcion que selecciona los datos en un intervalo de posiciones
        """
        data = data[data[name_position] >= positions[0]]
        data = data[data[name_position] <= positions[1]]
        return data

    def _get_data_by_confidence_level(self) -> None:
        """
        Selecciona solo un tipo de dato del FIRMS dependiendo su
        confiabilidad
        """
        self.data = self.data[self.data["confidence"] == "n"]

    def _get_data_type_0(self) -> None:
        print(self.data)
        self.data = self.data[self.data["type"] == 0]
