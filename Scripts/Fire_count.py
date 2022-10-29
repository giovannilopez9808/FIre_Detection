from Class_list import Fire_Count
inputs = {
    "city_name": "Parana_2022_Ago",
    "select_nominal_data": True,
    "color": "white",
}
Fire_algorithm = Fire_Count(**inputs)
Fire_algorithm.read_map()
Fire_algorithm.algorithm()
Fire_algorithm.create_animation(delete=False)
