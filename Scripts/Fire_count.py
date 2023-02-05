from Modules.fire import FireCount
inputs = {
    "city_name": "Nuevo_Leon_2022_Mar",
    "only_nominal_data": True,
    "color": "white",
    "plot": True,
}
Fire_algorithm = FireCount(**inputs)
Fire_algorithm.run()
# Fire_algorithm.create_animation(delete=False)
