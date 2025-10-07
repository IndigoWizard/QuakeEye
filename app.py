"""
Original Project Author: IndigoWizard, Feb 18, 2023.
Project Name: QuakeEye
License: GPL-3.0 (See LICENSE file for details)
"""

import streamlit as st
import folium
from folium.plugins import HeatMap
from folium.plugins import GroupedLayerControl
from streamlit_folium import folium_static
import requests
from datetime import datetime, date
import pandas as pd

st.set_page_config(
    page_title="QuakeEye",
    page_icon="https://cdn-icons-png.flaticon.com/512/2377/2377860.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    'Get help': "https://github.com/IndigoWizard/QuakeEye",
    'Report a bug': "https://github.com/IndigoWizard/QuakeEye/issues",
    'About': """
            Original Project Author: IndigoWizard, Feb 18, 2023.
            
            Project Name: QuakeEye.

            License: GPL-3.0 (See LICENSE file for details).
            """
    }
)

### CSS STYLING 
st.markdown(
"""
<style>
    /* Header*/
    /* Dark theme version */
    .st-emotion-cache-h4xjwg, .st-emotion-cache-12fmjuu {
        height: 1rem;
        background: none;
    }
    /*Header banner*/
    .st-emotion-cache-ropwps.egexzqm2 h1#wildfire-burn-severity-analysis {
        font-size: 1.75rem;
    }

    /*Main: Smooth scrolling*/
    .stMain.st-emotion-cache-bm2z3a.eht7o1d1 {
        scroll-behavior: smooth;
    }
    
    /* main app body with less padding*/
    .st-emotion-cache-t1wise.eht7o1d4 {
        padding: 0.2rem 2rem;
    }

    /* main app body with less padding in different screen size*/
    @media (min-width: calc(736px + 8rem)) {
        .st-emotion-cache-t1wise {
            padding: 0.2rem 2rem;
        }
    }

    /* ******* Sidebar ******* */
    /* Main container */
    /*Dark theme - Light theme class names*/
    .stSidebar.st-emotion-cache-1wqrzgl.e1c29vlm0, .stSidebar.st-emotion-cache-vmpjyt.e1c29vlm0 {
        min-width: 280px;
        max-width: fit-content;
    }

    /*Light theme sidbar background color*/
    .stSidebar.st-emotion-cache-vmpjyt, .stSidebar.st-emotion-cache-wgfafi.e1c29vlm0 {
        background-color: rgb(38, 39, 48);
        color: #fafafa;
    }
    /*sidebar light theme mobile view*/

    @media (max-width: 576px) {
        .stSidebar.st-emotion-cache-g8bi16.e1c29vlm0 {
            background-color: rgb(38, 39, 48);
            color: #fafafa;
        }
        .stVerticalBlock.st-emotion-cache-10e86g4.e6rk8up3, .stVerticalBlock.st-emotion-cache-1vn87qs.e6rk8up3 {
            gap: 1.6rem;
        }
    }


    /*Sidebar header*/
    .st-emotion-cache-kgpedg {
        padding: 0;
    }
    .st-emotion-cache-1mi2ry5.eczjsme6 {
        height: 0;
    }

    /* Logo */
    .st-emotion-cache-1kyxreq.e115fcil2 {
        justify-content: center;
    }

    /* Sidebar : inside container */
    .css-ge7e53 {
        width: fit-content;
    }

    /*Sidebar : image*/
    .st-emotion-cache-vew1uq.e6rk8up1 {
        display: flex;
        justify-content: center;
    }

    /*Sidebar : Navigation list*/
    div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) {
        margin: 0;
        padding: 0;
        list-style: none;
    }
    div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li {
        padding: 0;
        margin: 0;
        padding: 0;
        font-weight: 600;
    }
    div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li > a {
        text-decoration: none;
        transition: 0.2s ease-in-out;
        padding-inline: 10px;
    }
    
    div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li > a:hover {
        color: rgb(46, 206, 255);
        transition: 0.2s ease-in-out;
        background: #131720;
        border-radius: 4px;
    }
    
    /* Sidebar: socials*/
    div.css-rklnmr:nth-child(6) > div:nth-child(1) > div:nth-child(1) > p {
        display: flex;
        flex-direction: row;
        gap: 1rem;
    }

    /*Socials flex properties: dark & light theme*/
    .st-emotion-cache-1espb9k p, .st-emotion-cache-1mw54nq p {
        display: flex;
        flex-direction: row;
        justify-content: start;
        gap: 0.8rem;
        padding-inline: 10px;
    }
    
    /* Linkedin logo*/
    .st-emotion-cache-1espb9k.egexzqm0 p a img, .st-emotion-cache-1mw54nq.egexzqm0 p a img {
        width: 32px;
    }

    /*GitHub logo:  Dark Theme - Light Theme*/
    .st-emotion-cache-14j6x93:nth-child(6) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > a:nth-child(2) > img:nth-child(1) {
        background-color: #26273040;
        border-radius: 50%;
    }
    /*GitHub logo:  Dark Theme - Light Theme - Mobile version*/
    div.st-emotion-cache-vew1uq:nth-child(6) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > a:nth-child(2) > img:nth-child(1) {
        background-color: #26273040;
        border-radius: 50%;
    }

    /*Main body Title*/
    .st-emotion-cache-ropwps.egexzqm2 h1#wildfire-burn-severity-analysis, .st-emotion-cache-18netey.egexzqm2 h1#Earthquake-Visualization-Map {
        font-size: 2rem;
        padding: 1.8rem 0 0.5rem;
    }
    

    /* ******* Form Submit ******* */
    /* ***** Generate Map */
    /* Dark theme version */
    .st-emotion-cache-19rxjzo.ef3psqc7 {
        width: 100%;
    }
    /* Light Theme Version */
    .st-emotion-cache-7ym5gk.ef3psqc7 {
        width: 100%;
        background: rgba(0, 3, 172, 0.25);
    }

    /* Buttons */
    /* Light theme verison; hober effect */
    .st-emotion-cache-7ym5gk:hover {
        border-color: rgb(255, 0, 110);
        color: rgb(255, 0, 110);
    }

</style>
""", unsafe_allow_html=True)

# USGS earthquake data url
DATA_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson"

# fetch earthquake GeoJSON data from USGS API
def fetch_earthquake_data():
    response = requests.get(DATA_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch earthquake data.")
        return None


def main():
    # sidebar
    with st.sidebar:
        st.logo(image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQIW2NgAAIAAAUAAR4f7BQAAAAASUVORK5CYII=", link=None, icon_image="https://cdn-icons-png.flaticon.com/512/2377/2377860.png")
        st.image("https://cdn-icons-png.flaticon.com/512/2377/2377860.png", width=90)
        st.markdown("#### QuakeEye")
        st.subheader("Navigation:")
        st.markdown(
            """
                - [Earthquake](#earthquake)
                - [Data](#data)
                - [Credit](#credit)
            """)
    
        st.subheader("Contact:")
        st.markdown("[![LinkedIn](https://cdn-icons-png.flaticon.com/512/174/174857.png)](https://linkedin.com/in/ahmed-islem-mokhtari) [![GitHub](https://github.githubassets.com/favicons/favicon-dark.png)](https://github.com/IndigoWizard) [![Medium](https://miro.medium.com/1*m-R_BkNf1Qjr1YbyOIJY2w.png)](https://medium.com/@Indigo.Wizard/mt-chenoua-forest-fires-analysis-with-remote-sensing-614681f468e9)")

    st.subheader("Earthquake Visualization Map")

    # Fetch data
    data = fetch_earthquake_data()
    if not data:
        return

    # --- Layout ---
    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input("Start Date", date(2025, 1, 1))

    with col2:
        end_date = st.date_input("End Date", date.today())

    with col3:
        magnitude_limit = st.slider("Magnitude", min_value=0, max_value=10, value=5, step=1)

    # --- map initialization ---
    m = folium.Map(location=[36.60, 16.00], zoom_start=3, tiles=None)

    # basemaps
    basemap0 = folium.TileLayer("openstreetmap", name="Open Street Map", attr="OSM").add_to(m)
    basemap1 = folium.TileLayer("cartodbdark_matter", name="Dark Theme Basemap", attr="CARTO").add_to(m)

    # Extract main info
    places = [f["properties"]["place"] for f in data["features"]]
    magnitudes = [f["properties"]["mag"] for f in data["features"]]
    times = [f["properties"]["time"] for f in data["features"]]
    longs = [f["geometry"]["coordinates"][0] for f in data["features"]]
    lats = [f["geometry"]["coordinates"][1] for f in data["features"]]

    # Create coordinates list for HeatMap
        # --- Create Dynamic, Magnitude-Weighted HeatMap ---
    # Filter data first (so the heatmap updates based on user input)
    filtered_coords = []
    for mag, time_ms, lat, lon in zip(magnitudes, times, lats, longs):
        if mag is None:
            continue
        event_dt = datetime.fromtimestamp(time_ms / 1000)
        event_date = event_dt.date()
        if start_date <= event_date <= end_date and mag <= magnitude_limit:
            # Use magnitude as weight for intensity
            # Squared magnitude exaggerates stronger quakes visually
            filtered_coords.append([lat, lon, mag ** 2])

    # Define color gradient
    
    colors = {0.2: '#0f0b75', 0.45: '#9e189c', 0.75: '#ed7c50', 1: '#f4ee27'}


    # Only add heatmap if filtered data exists
    if filtered_coords:
        HeatMap(
            data=filtered_coords,
            gradient=colors,
            name="Magnitude-Weighted Heatmap",
            radius=20,
            blur=15,
            min_opacity=0.3,
            max_zoom=6
        ).add_to(m)


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

    # Add Markers based on filters
    for place, mag, time_ms, lat, lon in zip(places, magnitudes, times, lats, longs):
        if mag is None:
            continue
        event_dt = datetime.fromtimestamp(time_ms / 1000)
        event_date = event_dt.date()

        if start_date <= event_date <= end_date and mag <= magnitude_limit:
            date_str = event_dt.strftime("%Y-%m-%d")
            time_str = event_dt.strftime("%H:%M:%S")

            popup_info = f"<div class='popinfo'><h5><b>Earthquake Information</b></h5><b>Magnitude:</b> <span>{mag}</span><br><b>Date:</b> <span>{date_str}</span><br><b>Time:</b> <span>{time_str}</span><br><b>Location:</b> <span>{place}</span><br><b>Coordinates:</b> <span>{lat} , {lon}</span></div>"

            # Color by magnitude
            if mag <= 3.9:
                color = "beige"
            elif mag <= 4.9:
                color = "orange"
            elif mag <= 5.9:
                color = "lightred"
            elif mag <= 6.9:
                color = "red"
            elif mag <= 7.9:
                color = "darkred"
            else:
                color = "black"

            folium.Marker(
                [lat, lon],
                popup=popup_info,
                icon=folium.Icon(color=color)
            ).add_to(main_layer)
    

    folium.plugins.Fullscreen(position="bottomright", title="Expand me", title_cancel="Exit me", force_separate_button=True).add_to(m)

    folium.LayerControl(collapsed=True).add_to(m)

    GroupedLayerControl(
        groups={
        "Earthquake Classes by Magnitude": [minor_layer, light_layer, moderate_layer, strong_layer, major_layer, great_layer]
        },
        exclusive_groups=False,
        collapsed=False
    ).add_to(m)

    # Display the map
    folium_static(m)

    # --- Earthquake Statistics Panel (Lightweight Pandas Block) ---
    # Build dataframe from filtered markers only
    filtered_data = []
    for place, mag, time_ms, lat, lon in zip(places, magnitudes, times, lats, longs):
        if mag is None:
            continue
        event_dt = datetime.fromtimestamp(time_ms / 1000)
        event_date = event_dt.date()
        if start_date <= event_date <= end_date and mag <= magnitude_limit:
            filtered_data.append({
                "place": place,
                "magnitude": mag,
                "time": event_dt,
                "lat": lat,
                "lon": lon
            })

    if filtered_data:
        df = pd.DataFrame(filtered_data)

        total_quakes = len(df)
        avg_mag = round(df["magnitude"].mean(), 2)
        max_mag = df["magnitude"].max()
        strongest = df.loc[df["magnitude"].idxmax()]

        # Display stats in three neat columns
        st.markdown("### Summary Data Statistics")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("##### Total Earthquakes")
            st.markdown(f"#### {total_quakes}")
        with col_b:
            st.markdown("##### Average Magnitude")
            st.markdown(f"#### {avg_mag}")
        with col_c:
            # st.metric("Strongest Event", f"{max_mag} ({strongest['place'][:50] + '...' if len(strongest['place'])>50 else strongest['place']})")
            st.markdown("##### Strongest Recorded Earthquake")
            st.info(
                f"**{strongest['place']}** — Magnitude **{max_mag}**, occurred on "
                f"{strongest['time'].strftime('%Y-%m-%d %H:%M:%S UTC')} "
                f"at coordinates ({strongest['lat']:.2f}, {strongest['lon']:.2f})."
            )
    else:
        st.info("No earthquakes found for the selected range.")

    # --- Histogram of Magnitudes ---
    st.markdown("### Magnitude Distribution")

    # Filtered magnitudes for histogram
    filtered_mags = [
        mag for mag, time_ms in zip(magnitudes, times)
        if mag is not None and start_date <= datetime.fromtimestamp(time_ms / 1000).date() <= end_date and mag <= magnitude_limit
    ]

    if filtered_mags:
        # Create histogram bins (0–10, step=1)
        bins = list(range(0, 11))
        freq = [sum(1 for m in filtered_mags if i <= m < i + 1) for i in bins]

        # Prepare data for st.bar_chart
        chart_data = {"Magnitude": [f"{i}-{i+1}" for i in bins], "Count": freq}
        st.bar_chart(data=chart_data, x="Magnitude", y="Count", use_container_width=True)
    else:
        st.info("No earthquakes match the current filters.")


    # Custom CSS fix
    st.markdown(
    """
    <style>
        /*Map iframe*/
        iframe {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
