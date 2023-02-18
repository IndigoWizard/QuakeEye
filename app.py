import folium
import webbrowser

m = folium.Map(location=[36.5, 37.5], tiles="openstreetmap", zoom_start=3)

m.save("map.html")
webbrowser.open("map.html")
