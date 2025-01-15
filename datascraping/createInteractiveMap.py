import matplotlib.pyplot as plt
import json
import folium
from folium import FeatureGroup
import os.path
import webbrowser

# Load data from JSON file
with open('stationData\\station.json', 'r', encoding='utf-8') as file:
    stations_data = json.load(file)

# Group stations by the lines they share
line_groups = {}

# Loop through the stations and group them by their lines
for station_name, station_info in stations_data.items():
    for line in station_info["lines"]:
        if line not in line_groups:
            line_groups[line] = []
        line_groups[line].append((float(station_info["coords"]["lat"]), float(station_info["coords"]["long"]), station_name))

# Define a color palette for the lines
line_colors = {
    "3": "blue",
    "4": "green",
    "7": "red",
    "9": "purple",
    "12": "orange",
    "17": "cyan",
    "21": "magenta",
    "15": "yellow",
    "31": "brown",
    "34": "pink",
}

# Ensure all lines have a color (if a line is missing, assign it a default color)
default_color = "gray"
for station_name, station_info in stations_data.items():
    for line in station_info["lines"]:
        if line not in line_colors:
            line_colors[line] = default_color  # Assign gray color if line is missing from the palette

# Create a folium map centered around the middle of the coordinates
center_lat = (53.75 + 54) / 2  # Average latitude
center_long = (10.55 + 10.95) / 2  # Average longitude

# Create a folium map centered at the average coordinates
m = folium.Map(location=[center_lat, center_long], zoom_start=10)

# Optionally, add a rectangle to visualize the bounding area
folium.Rectangle(
    bounds=[[53.75, 10.55], [54, 10.95]],  # Bottom-left and top-right coordinates
    color="blue",
    weight=2,
    fill=True,
    fill_color="blue",
    fill_opacity=0.1
).add_to(m)

# Create feature groups for each bus line to allow toggling visibility
line_feature_groups = {}

# Add markers for each station, color-coded by all lines the station belongs to
for station_name, station_info in stations_data.items():
    lat = float(station_info["coords"]["lat"])
    lon = float(station_info["coords"]["long"])

    # Get the list of bus lines for the station
    lines_str = ', '.join(station_info["lines"])  # Join the lines with commas (e.g., "3, 7, 9")

    # Loop through each line the station belongs to and add a marker for each line with the respective color
    for line in station_info["lines"]:
        line_color = line_colors.get(line, default_color)  # Default to gray if no color for the line
        
        # Create a FeatureGroup for each line if not already created
        if line not in line_feature_groups:
            line_feature_groups[line] = FeatureGroup(name=f"Line {line}")
        
        # Add a marker for each line
        folium.Marker(
            [lat, lon], 
            popup=f"{station_name}<br>Lines: {lines_str}",  # Show all the lines the station belongs to in the popup
            icon=folium.Icon(color=line_color)
        ).add_to(line_feature_groups[line])

# Add all feature groups to the map
for line_group in line_feature_groups.values():
    line_group.add_to(m)

# Add a layer control to toggle the visibility of lines
folium.LayerControl().add_to(m)

# Save the map as an HTML file
folder = "maps"
os.makedirs(folder, exist_ok=True)
file = os.path.join(folder, "map_colored_all_lines_with_toggle.html")
m.save(file)
webbrowser.open(file)

# Output message indicating that the map has been saved
print("The color-coded map with toggleable bus lines has been saved to 'map_colored_all_lines_with_toggle.html'. You can open it in your browser to view the interactive map.")
