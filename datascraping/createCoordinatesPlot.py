import matplotlib.pyplot as plt
import json

# Sample data structure with station names, lines, and coordinates

with open('datascraping\\stationData\\station.json', 'r') as file:
    stations_data = json.load(file)

# Group stations by the lines they share
line_groups = {}

# Loop through the stations and group them by their lines
for station_name, station_info in stations_data.items():
    for line in station_info["lines"]:
        if line not in line_groups:
            line_groups[line] = []
        line_groups[line].append((float(station_info["coords"]["lat"]), float(station_info["coords"]["long"]), station_name))

# Create plot
plt.figure(figsize=(10, 8))

# Loop through each line group and plot the points and lines
for line, stations in line_groups.items():
    # Extract latitudes, longitudes, and names
    latitudes = [station[0] for station in stations]
    longitudes = [station[1] for station in stations]
    names = [station[2] for station in stations]
    
    # Plot the points for each line
    plt.scatter(longitudes, latitudes, label=f"Line {line}", marker='o', s=6)


plt.title('Lübecker Busnetz')

plt.xlim(10.55, 10.95)
plt.ylim(53.75, 54.05)

plt.xlabel('Breitengrad')
plt.ylabel('Längengrad')

plt.gca().set_aspect('equal', adjustable='box')

plt.legend()
plt.grid(True)
plt.show()