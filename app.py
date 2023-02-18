import folium
import requests
import webbrowser

# Earthquake data GeoJSON URL:
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
# opting for weekly results to test the api for now


# Getting the earthquake data
try:
    responnse = requests.get(url)
    responnse.raise_for_status()
    data = responnse.json()
except requests.exceptions.RequestException as expt:
    print("Error: Could not retrieve data from API")
    print("details: ", expt)
    exit(1)

# Extracting main information (location (latitde & longitude), magnitude)

longs = [feature["geometry"]["coordinates"][0] for feature in data ["features"]]
lats = [feature["geometry"]["coordinates"][1] for feature in data ["features"]]
magnitudes = [feature["properties"]["mag"] for feature in data ["features"]]

# Making a coordinates list
coords = [[lat, lon, mag] for lat, lon, mag in zip(lats, longs, magnitudes)]

# Main project folium map
m = folium.Map(location=[36.5, 37.5], tiles=None, zoom_start=3)

#Primary basemaps
basemap0 = folium.TileLayer("cartodbdark_matter", name="Dark Theme Basemap").add_to(m)
basemap1 = folium.TileLayer("openstreetmap", name="Open Street Map").add_to(m)

m.save("map.html")
webbrowser.open("map.html")
