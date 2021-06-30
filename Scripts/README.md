### Instrucciones

1. **Introducir los parámetros de la ciudad por analizar**

   Dentro del script `Class_list.py` en la clase `city_list` deberas incluir los siguientes parámetros en un diccionario:

   ```python
   "Identificador de la ciudad": {
               "day initial": "yyyy-mm-dd",
               "day final": "yyyy-mm-dd",
               "lon": [lon_i, lon_f],
               "lat": [lat_i, lat_i],
               "delta": dif_lat_and_lon,
           },
   ```

   donde `lon_i<lon_f` y `lat_i<lat_f`, `"delta"` es cuanto aumentara en longitud y latitud en cada grilla.

2. **`Fire_count.py`**

   Encargado de realizar el conteo de incendios usando las clases declaradas en `Class_list.py`. Su estructura ya esta definida, lo que se tendra que modificar es el identificador de la ciudad.

3. **`Graphics_Bar_confidence.py`**

   Realiza la gráfica de la distribución de datos dependiendo su confiabilidad. Se guarda con el nombre `Bar_Confidence_percentage.png`.

4. **`Graphics_Fire_Day.py`**

   Realiza la gráfica de los incendios reportados por dia. Se guarda con el nombre `Fire_Per_Day.png`.

5. **`Graphics_Fire_Accumulative.py`**

   Realiza la gráfica de los incendios reportados acumulados por día. Se guarda con el nombre `Fire_Accumulative.png`.
