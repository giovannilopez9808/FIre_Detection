from Modules.fire import FireCount
inputs = {
    "city_name": "Parana_2020",
    "only_nominal_data": True,
    "color": "white",
}
Fire_algorithm = FireCount(**inputs)
# Fire_algorithm.run()
Fire_algorithm.create_animation(delete=False)
