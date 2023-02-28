import streamlit as st
import folium
from folium.plugins import HeatMap
from folium.plugins import GroupedLayerControl
from branca.element import Template, MacroElement
import requests
from datetime import datetime
import webbrowser

# Earthquake data GeoJSON URL:
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson"

# Getting the earthquake data
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as expt:
    st.error("Error: Could not retrieve data from API")
    st.error("details: ", +str(expt))
    st.stop()

st.set_page_config(
    page_title="QuakeEye",
    page_icon="https://cdn-icons-png.flaticon.com/512/2377/2377860.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    'Get help': "https://github.com/IndigoWizard/QuakeEye",
    'Report a bug': "https://github.com/IndigoWizard/QuakeEye/issues",
    'About': "# This is a header. This is an *extremely* cool app!"
    }
)

########### SIDEBAR  MENU ########### 
# Set up the sidebar
st.sidebar.title("Navigation")

# Project summary section
st.sidebar.subheader("Project Summary")
st.sidebar.success("Real-Time Earthquake Data Visualization App.")

# About section
st.sidebar.subheader("About me:")
st.sidebar.caption("Tech & Open Source enthusiast | Geo Environment & Spatial Planning | Remote Sensing & Cartography | Indie Games Dev | House of M.")

# Contact section
st.sidebar.subheader("Find me at:")

## Define columns in the sidebar
c1, c2, c3 = st.sidebar.columns([1, 1, 1])

# Display info in the columns
with c1:
    st.info("[![LinkedIn](https://static.licdn.com/sc/h/8s162nmbcnfkg7a0k8nq9wwqo)](https://linkedin.com/in/ahmed-islem-mokhtari)")
with c2:
    st.info("[![GitHub](https://github.githubassets.com/favicons/favicon-dark.png)](https://github.com/IndigoWizard)")
with c3:
    st.info("[![Medium](https://miro.medium.com/1*m-R_BkNf1Qjr1YbyOIJY2w.png)](https://medium.com/@Indigo.Wizard/mt-chenoua-forest-fires-analysis-with-remote-sensing-614681f468e9)")

# App custom CSS
st.markdown(
    """
    <style>
    /*Main app page*/
    .css-k1ih3n{
        padding: 2rem 1rem 5rem;
    }
    /*Sidebar*/
    .css-1vencpc {
        width: 20vw !important;
    }
    .css-1vq4p4l{
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

########### MAIN PAGE CONTENT ###########
# App title
st.title("QuakeEye Project")

st.write("ʕ •ᴥ•ʔ : Dont forget to star ⭐ this project on [GitHub.com/IndigoWizard/QuakeEye](https://github.com/IndigoWizard/QuakeEye/stargazers)")
# Add a title to your Streamlit app
st.header("Earthquake Data Visualization")

# Add a description of your Streamlit app
st.write("This app visualizes the latest earthquake data from the USGS in real-time. The app retrieves earthquake data from the USGS API and displays the data on a map using the Folium library.")
st.write("Users can filter and explore earthquake data by magnitude, location, and time range.")

st.subheader("Earthquake Map")

########### MAIN APP ###########
# Extracting main information (location (latitde & longitude), magnitude)
places = [feature["properties"]["place"] for feature in data ["features"]]
magnitudes = [feature["properties"]["mag"] for feature in data ["features"]]
times = [feature["properties"]["time"] for feature in data ["features"]] 
longs = [feature["geometry"]["coordinates"][0] for feature in data ["features"]]
lats = [feature["geometry"]["coordinates"][1] for feature in data ["features"]]

# Making a coordinates list
coords = [[lat, lon, mag] for lat, lon, mag in zip(lats, longs, magnitudes)]

# Main project folium map
m = folium.Map(location=[36.5, 37.5], tiles=None, zoom_start=3)

#Primary basemaps
basemap0 = folium.TileLayer("cartodbdark_matter", name="Dark Theme Basemap").add_to(m)
basemap1 = folium.TileLayer("openstreetmap", name="Open Street Map").add_to(m)

# Defning a color ramp for the heat map
colors = {0.2: '#0f0b75', 0.45: '#9e189c', 0.75: '#ed7c50', 1: '#f4ee27'}

# Adding the folium heatmap layer using the HeatMap plugin
heatmap = HeatMap(data=coords, gradient=colors, name="Earthquake Distribution Heatmap").add_to(m)

# Earthquake Marker layers
# Making a main earthquake layers group to enable/disable all the layers at once from the defaul layer panel
main_layer = folium.FeatureGroup("Earthquakes Location").add_to(m)

# Earthquakes are split into categories based on their magnitudes
# micro_layer = folium.FeatureGroup(name="Micro: Less than 2.9").add_to(main_layer)
minor_layer = folium.FeatureGroup(name="Minor: Less than 3.9").add_to(main_layer)
light_layer = folium.FeatureGroup(name="Light: 4.0 - 4.9").add_to(main_layer)
moderate_layer = folium.FeatureGroup(name="Moderate: 5.0 - 5.9").add_to(main_layer)
strong_layer = folium.FeatureGroup(name="Strong: 6.0 - 6.9").add_to(main_layer)
major_layer = folium.FeatureGroup(name="Major: 7.0 - 7.9").add_to(main_layer)
great_layer = folium.FeatureGroup(name="Great: 8.0 and higher").add_to(main_layer)

# Injecting custom css through branca macro elements and template
app_css = """
{% macro html(this, kwargs) %}
    <head>
        <title>QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari</title>
        
        <!-- Global Meta Tags -->
        <meta itemprop="image" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif">
        <meta itemprop="thumbnailUrl" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif">
        <link rel="image_src" href="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif">
        <link rel="shortcut icon" type="image/x-icon" href="https://cdn-icons-png.flaticon.com/512/2377/2377860.png">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer"/>
        <link rel="stylesheet" href="style.css">

        <!-- LinkediI Meta Tags -->
        <meta property="og:url" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif"/>
        <meta property="og:title" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari"/>
        <meta property="og:description" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari"/>
        <meta property="og:image" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif"/>

        <!-- Facebook Meta Tags -->
        <meta property="og:url" content="https://indigowizard.github.io/QuakeEye/map.html">
        <meta property="og:type" content="website">
        <meta property="og:title" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari">
        <meta property="og:description" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari">
        <meta property="og:image" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif">

        <!-- Twitter Meta Tags -->
        <meta name="twitter:card" content="summary_large_image">
        <meta property="twitter:domain" content="https://indigowizard.github.io/QuakeEye/map.html">
        <meta property="twitter:url" content="https://indigowizard.github.io/QuakeEye/map.html">
        <meta name="twitter:title" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari">
        <meta name="twitter:description" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari">
        <meta name="twitter:image" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif">

        <!-- Meta Tags Generated via https://www.opengraph.xyz -->
    </head>
    
    <style>
/* Marker PopUp Box CSS */
        .leaflet-popup-content-wrapper{
            padding: 1px;
            text-align: left;
            border: 4px solid #d7a45d;
            border-radius: 12px;
            /*GLASSMORPHISM EFFECT*/
            background: rgba( 28, 25, 56, 0.25 );
            box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
            backdrop-filter: blur( 4px );
            -webkit-backdrop-filter: blur( 4px );
            border: 4px solid rgba( 215, 164, 93, 0.2 );
        }
        .leaflet-popup-content{
            margin: 13px 24px 13px 20px;
            font-size: 1.2em;
            line-height: 1.3;
            min-height: 1px;
        }
        .popinfo {
            width: max-content;
            border-radius: 5px;
            color: #993200;
        }
        .popinfo h5{
            text-align: center;
        }
        .popinfo span{
            font-weight: bold;
            color: #9d3a00;
        }
        .popinfo b{
            font-weight: 800;
            font-family: bariol;
            font-size: 1.4em;
        }
        .leaflet-popup-tip{
            background: #d7a45d !important;
        }

/* Layer Control Panel CSS */

        .leaflet-control-layers-list {
            width: 14vw;
            min-width: 130px;
            overflow-y: auto;
            overflow-x: hidden;
        }
        .leaflet-control-layers form {
            z-index: 10000;
            overflow-y: auto;
            overflow-x: hidden;
        }
        .leaflet-control-layers-group-label{
            padding: 2px;
            margin: 2px;
            background-color: #d75d5d;
            border: 1px dashed black;
            border-radius: 4px;
            text-align: center;
        }
    </style>

{% endmacro %}
"""
# configuring the style
style = MacroElement()
style._template = Template(app_css)

# Adding style to the map
m.get_root().add_child(style)

# Adding Markers to layers based on earthquake magnitude
for place, mag, time, lat, lon  in zip(places, magnitudes, times, lats, longs):
    
    # converting API earthquake time info from unix time to human-readable time format
    time_date = datetime.fromtimestamp(time/1000.0).strftime("%Y-%m-%d") 
    time_hour = datetime.fromtimestamp(time/1000.0).strftime("%H:%M:%S") 
    # Configure data display in popups when clicking on markers <span></span>
    popup_info = f"<div class='popinfo'><h5><b>Earthquake Information</b></h5><b>Magnitude:</b> <span>{mag}</span><br><b>Date:</b> <span>{time_date}</span><br><b>Time:</b> <span>{time_hour}</span><br><b>Location:</b> <span>{place}</span><br><b>Coordinates:</b> <span>{lat} , {lon}</span></div>"

    if mag <= 3.9: #2.9:
        # folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="lightgreen")).add_to(micro_layer)
    # elif mag <= 3.9:
        folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="beige")).add_to(minor_layer)
    elif mag <= 4.9:
        folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="orange")).add_to(light_layer)
    elif mag <= 5.9:
        folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="lightred")).add_to(moderate_layer)
    elif mag <= 6.9:
        folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="red")).add_to(strong_layer)
    elif mag <= 7.9:
        folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="darkred")).add_to(major_layer)
    else:
        folium.Marker([lat, lon], popup=popup_info, icon=folium.Icon(color="black")).add_to(great_layer)
    

# Adding the layer control
folium.LayerControl(collapsed=False).add_to(m)

# Ctreating multiple magnitude layers based on Richter classification
# Using GroupedLayerControl to stack the new layers under a one category and make them individually interactive
GroupedLayerControl(
    groups={
    "Earthquake Classes by Magnitude": [minor_layer, light_layer, moderate_layer, strong_layer, major_layer, great_layer]
    },
    exclusive_groups=False,
    collapsed=False
).add_to(m)

# Display the map using streamlit-folium
html_string = m._repr_html_()

# Display the HTML string using Streamlit
st.components.v1.html(html_string, width=1000, height=600)
