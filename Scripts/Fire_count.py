from Class_list import *
inputs = {
    "City name": "Parana_2021_Jul",
    "Number color": "white",
    "Select nominal data": True,
}
Fire_algorithm = Fire_Count(city_name=inputs["City name"],
                            select_nominal_data=inputs["Select nominal data"],
                            color=inputs["Number color"])
Fire_algorithm.read_map()
Fire_algorithm.algorithm()
Fire_algorithm.create_animation(delete=False)
