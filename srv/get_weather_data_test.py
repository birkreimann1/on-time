import weatherdata.readData as weather

env_data = weather.getDataByCoords(lat=53.867913, long=10.740366)
print(env_data)