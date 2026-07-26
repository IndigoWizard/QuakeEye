"""
Original Project Author: IndigoWizard, Feb 18, 2023.
Project Name: QuakeEye
License: GPL-3.0 (See LICENSE file for details)
"""

import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from branca.element import Template, MacroElement, Figure, Element
from folium.utilities import escape_backticks
import requests
from datetime import datetime, timedelta, date
import pandas as pd

st.set_page_config(
    page_title="QuakeEye",
    page_icon="https://cdn-icons-png.flaticon.com/512/2377/2377860.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    'About':
        """
        Original Project Author: IndigoWizard, Feb 18, 2023.
        
        Project Name: QuakeEye.

        License: GPL-3.0 (See LICENSE file for details).

        Description: Real-Time Earthquake Data Visualization.
        """,
    "Get Help": "mailto:tro56f5j6@mozmail.com",
    'Report a bug': "https://github.com/IndigoWizard/QuakeEye/issues",
    }
)


# custom css styling
custom_css = """
    <style>

    /*---- header ----*/
    .stAppHeader {
        height: 2rem;
        min-height: 2rem;
    }

    /* Fork + Github icon */
    .st-emotion-cache-1p1m4ay {
    display: none;
    }

    /*---- sidebar ----*/
    /*space above title*/
    .st-emotion-cache-10p9htt {
        margin-bottom: 0;
        height: 2.5rem;
    }

    /*title*/
    .st-emotion-cache-u1kubd h1, .st-emotion-cache-1ix68xf h1{
        display: flex;
        justify-content: center;
        letter-spacing: 0.24rem;
    }

    /*image*/
    .st-emotion-cache-uwwqev.e1xxut3m0 {
        display: flex;
        justify-content: center;
    }

    /*navigation list*/
    .st-emotion-cache-u1kubd > ul, .st-emotion-cache-1ix68xf > ul {
        font-size: 1.25rem;
        list-style: none;
        padding: 0px;
        transition: 0.2s ease-in-out;
    }

    /*nav list: li*/
    .st-emotion-cache-u1kubd li, .st-emotion-cache-1ix68xf li {
        margin: 0px;
        padding: 0px;
    }

    /*nav list: a url*/
    .st-emotion-cache-u1kubd a, .st-emotion-cache-1ix68xf a {
        text-decoration: none;
        font-weight: 600;
        transition: 0.15s ease-in-out;
    }

    .st-emotion-cache-u1kubd ul li a:hover, .st-emotion-cache-1ix68xf ul li a:hover {
        background-color: rgba(61, 157, 243, 0.15);
        padding-inline: 0.3rem;
        border-radius: 0.2rem;
    }

    /*contact - socials*/
    .st-emotion-cache-u1kubd h3, .st-emotion-cache-1ix68xf h3{
        font-size: 1.4rem;
        padding: 0.75rem 0px 0.5rem;
    }

    .social-links {
        display: flex;
        flex-direction: row;
        justify-content: start;
        gap: 1rem;
        margin-top: 0.5rem;
    }

    .social-links a {
        transition: color 0.2s;
    }

    .social-links svg {
        width: 1.4rem;
        height: 1.4rem;
    }


    /*---- body ----*/
    .st-emotion-cache-zy6yx3 {
        padding: 0.25rem;
    }

    .stMain.st-emotion-cache-4rsbii.e15ve43o1 {
        scroll-behavior: smooth;
    }

    @media (min-width: calc(736px + 8rem)) {
        .st-emotion-cache-zy6yx3 {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }

    @media (max-width: 863px) {
        .st-emotion-cache-zy6yx3 {
            padding: 0 1rem;
        }
    }

    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

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
        st.title("Quake Eye")
        st.logo(image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQIW2NgAAIAAAUAAR4f7BQAAAAASUVORK5CYII=", link=None, icon_image="https://cdn-icons-png.flaticon.com/512/2377/2377860.png")
        st.image("https://cdn-icons-png.flaticon.com/512/2377/2377860.png", width=100)
        st.markdown("---")
        st.markdown(
            """
                - [Earthquake Map](#quake-eye-earthquake-visualization)
                - [Stats Report](#summary-data-statistics)
            """
        )
        st.markdown("### Contact")
        contact_socials = """
            <div class="social-links">
                <a href="https://lnkd.in/dT3VAPAB" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" xml:space="preserve"><path d="M22.262 0H1.809C.831 0 0 .774 0 1.727v20.545C0 23.226.545 24 1.523 24h20.453c.979 0 2.024-.774 2.024-1.728V1.727A1.72 1.72 0 0 0 22.262 0" style="fill:none"/><path d="M22.262 0H1.809C.831 0 0 .774 0 1.727v20.545C0 23.226.545 24 1.523 24h20.453c.979 0 2.024-.774 2.024-1.728V1.727A1.72 1.72 0 0 0 22.262 0M9.143 9.143h3.231v1.647h.035C12.902 9.902 14.357 9 16.155 9c3.453 0 4.416 1.833 4.416 5.229v6.343h-3.429v-5.718c0-1.52-.607-2.854-2.026-2.854-1.723 0-2.545 1.167-2.545 3.082v5.489H9.143zM3.429 20.571h3.429V9.143H3.429zM7.286 5.143a2.142 2.142 0 1 1-4.285.001 2.142 2.142 0 0 1 4.285-.001" style="fill-rule:evenodd;clip-rule:evenodd;fill:#0a66c2"/></svg>
                </a>
                <a href="https://medium.com/@Indigo.Wizard" target="_blank" rel="noopener noreferrer" aria-label="Medium">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" xml:space="preserve"><path d="M2.667 23.999h18.666A2.667 2.667 0 0 0 24 21.332V2.667A2.667 2.667 0 0 0 21.333 0H2.667A2.667 2.667 0 0 0 0 2.667v18.666a2.665 2.665 0 0 0 2.667 2.666" style="fill-rule:evenodd;clip-rule:evenodd"/><path d="M5.859 8.109c0-.188-.094-.422-.234-.516L4.172 5.812v-.281h4.594l3.516 7.781 3.141-7.781h4.359v.281l-1.266 1.219c-.094.047-.141.188-.141.328v8.906c0 .141.047.281.141.375l1.266 1.172v.281h-6.235v-.281l1.266-1.219c.141-.141.141-.188.141-.375V9.047l-3.563 9h-.469l-4.125-9v6.047c-.047.234.047.516.234.703l1.641 2.016v.234H3.984v-.234l1.641-2.016c.188-.188.281-.469.234-.703z" style="fill-rule:evenodd;clip-rule:evenodd;fill:#fff"/></svg>
                </a>
                <a href="https://github.com/IndigoWizard/QuakeEye" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" xml:space="preserve"><path d="M12 0C5.368 0 0 5.813 0 12.464-.012 17.452 3.089 22.286 7.758 24h.314c.603 0 1.178-.264 1.178-.861v-2.11a2.9 2.9 0 0 1-1.067.221c-1.467 0-2.333-.797-2.955-2.282-.245-.599-.511-.953-1.022-1.019-.266-.022-.356-.133-.356-.266 0-.266.445-.465.889-.465.645 0 1.2.399 1.778 1.219.445.642.911.931 1.467.931s.911-.2 1.422-.709c.377-.377.666-.709.932-.931-2.934-.355-5-2.459-5-5.184 0-1.107.4-2.304 1.067-3.102-.289-.732-.244-2.283.089-2.925.888-.111 2.089.355 2.8.997.845-.266 1.733-.399 2.823-.399s1.978.133 2.778.376c.689-.62 1.911-1.086 2.8-.975.311.599.356 2.149.066 2.902.711.842 1.089 1.972 1.089 3.124 0 2.725-2.067 4.785-5.044 5.162.756.487 1.267 1.551 1.267 2.769v2.665c0 .665.515.861 1.222.861h.135C20.672 22.38 24 17.728 24 12.464 24 5.813 18.632 0 12 0"/><path d="M15.072 23.139v-2.665c0-1.218-.511-2.282-1.267-2.769 2.977-.377 5.044-2.437 5.044-5.162 0-1.152-.377-2.282-1.089-3.124.289-.754.245-2.304-.066-2.902-.888-.111-2.111.355-2.8.975-.8-.243-1.689-.376-2.778-.376s-1.978.133-2.823.399c-.711-.642-1.911-1.107-2.8-.997-.332.641-.377 2.192-.088 2.923-.667.798-1.067 1.994-1.067 3.102 0 2.725 2.066 4.83 5 5.184-.266.221-.555.553-.932.931-.511.51-.867.709-1.422.709s-1.022-.288-1.467-.931c-.577-.82-1.133-1.219-1.778-1.219-.445 0-.889.2-.889.465 0 .132.089.244.356.266.511.066.777.421 1.022 1.019.622 1.485 1.489 2.282 2.955 2.282.356 0 .756-.088 1.067-.221v2.11c0 .598-.575.862-1.178.862h8.222c-.706 0-1.222-.197-1.222-.861" style="fill:#fff"/></svg>
                </a>
                <a href="mailto:tro56f5j6@mozmail.com" target="_blank" rel="noopener noreferrer" aria-label="Email">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="21" viewBox="0 0 24 21" xml:space="preserve"><path d="M2.653 0h18.695C23.111 0 24 .731 24 2.217v16.567C24 20.257 23.111 21 21.347 21H2.653C.889 21 0 20.257 0 18.783V2.217C0 .731.889 0 2.653 0m8.705 13.12a1 1 0 0 0 1.269.001l8.875-7.286c.339-.282.606-.932.184-1.511-.409-.579-1.157-.593-1.651-.24l-7.417 5.948a1 1 0 0 1-1.252-.001L3.965 4.084c-.494-.353-1.242-.339-1.651.24-.424.578-.155 1.228.183 1.51z" style="fill:#969baa"/></svg>
                </a>
                <a href="https://indigowizard.github.io/portfolio/" target="_blank" rel="noopener noreferrer" aria-label="Website">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" xml:space="preserve"><path d="M14.667 2.667a1.333 1.333 0 0 1 0-2.667h8C23.403 0 24 .597 24 1.333v8a1.333 1.333 0 0 1-2.666 0v-4.8l-8.915 8.97c-.59.441-1.331.251-1.753-.17-.402-.402-.468-1.223-.114-1.697l8.915-8.97zM0 5.333a2.667 2.667 0 0 1 2.667-2.667h6.667a1.334 1.334 0 0 1-.001 2.667H2.667v16h16v-6.667a1.333 1.333 0 0 1 2.666 0v6.667A2.667 2.667 0 0 1 18.666 24h-16A2.667 2.667 0 0 1 0 21.333z" style="fill:#969baa"/></svg>
                </a>
            </div>
        """
        st.markdown(contact_socials, unsafe_allow_html=True)

    st.title("Quake Eye - Earthquake Visualization")
    st.markdown("Real-Time Earthquake Data Visualization through USGS data.")

    # Fetch data
    data = fetch_earthquake_data()
    if not data:
        return

    # map section
    with st.container():
        # --- Layout ---
        col1, col2 = st.columns([3,1])

        with col2:            
            st.info("Magnitude.")
            magnitude_limit = st.slider("Magnitude", min_value=0, max_value=10, value=5, step=1, label_visibility="collapsed")

            # time range
            today = datetime.today()
            last_month = today - timedelta(days=30)

            st.warning("Start Date.")
            start_date = st.date_input("Start Date", last_month, label_visibility="collapsed")
            
            st.success("End Date.")
            end_date = st.date_input("End Date", today, label_visibility="collapsed")

        with col1:
            # --- map initialization ---
            m = folium.Map(location=[36.60, 16.00], zoom_start=3, tiles=None, control_scale=True, attributionControl=0)

            # basemaps
            basemap0 = folium.TileLayer("openstreetmap", name="Open Street Map", attr="OSM").add_to(m)
            basemap1 = folium.TileLayer("cartodbdark_matter", name="Dark Theme Basemap", attr="CARTO").add_to(m)

            # custom attribution textbox
            class MyCustomAttribution(MacroElement):
                _template = Template("""
                    {% macro script(this, kwargs) %}

                    L.Control.MyCustomAttribution = L.Control.extend({
                        onAdd: function(map) {
                            let div = L.DomUtil.create('div', 'map-credit-box');
                            div.innerHTML = `{{ this.injectedHtml }}`;
                            L.DomEvent.disableClickPropagation(div);
                            return div;
                        }
                    });

                    L.control.myCustomAttribution = function(opts) {
                        return new L.Control.MyCustomAttribution(opts);
                    };

                    L.control.myCustomAttribution({
                        position: "{{ this.position }}"
                    }).addTo({{ this._parent.get_name() }});

                    {% endmacro %}
                """)

                def __init__(self, injectedHtml, position="bottomright"):
                    super().__init__()
                    self.injectedHtml = escape_backticks(injectedHtml)
                    self.position = position

            credit_html = """
                <style>
                    .map-credit-box.leaflet-control {
                        bottom: -10px;
                        right: -10px;
                        z-index: 9999;
                        background: rgba(255, 255, 255, 0.85);
                        color: #333;
                        padding: 2px 2px;
                        border-radius: 4px;
                        font-size: 0.9rem;
                        font-weight: 600;
                        font-family: "Segoe UI", "Noto Sans", sans-serif;
                        line-height: 1.2;
                        max-width: 90vw;
                        white-space: normal;
                    }

                    .map-credit-box.leaflet-control a {
                        color: #0078A8;
                        text-decoration: none;
                    }
                    
                    .leaflet-bottom .leaflet-control-scale{
                        font-weight: 600;
                        font-family: "Source Sans Pro", sans-serif;
                        margin-bottom: 0;
                    }

                    /* Mobile adjustments */

                    @media (max-width: 825px) {
                        .leaflet-bottom .leaflet-control-scale{
                            margin-bottom: 25px;
                        }
                    }
                    @media (max-width: 815px) {
                        .map-credit-box.leaflet-control {
                            max-width: 100%;
                            width: 100%;
                        }
                        .leaflet-bottom .leaflet-control-scale{
                            margin-bottom: 45px;
                        }
                    }
                    @media (max-width: 610px) {
                        .map-credit-box.leaflet-control {
                            font-size: 0.8rem;
                            max-width: 100%;
                            text-align: center;
                        }
                        .leaflet-bottom .leaflet-control-scale{
                            margin-bottom: 45px;
                        }
                    }
                    @media (max-width: 550px) {
                        .map-credit-box.leaflet-control {
                            width: 100%;
                            text-align: center;
                        }
                        .leaflet-bottom .leaflet-control-scale{
                            margin-bottom: 45px;
                        }
                    }
                </style>

                🇵🇸 Terrain Viewer by <a href="https://github.com/IndigoWizard/QuakeEye" target="_blank" rel="noopener noreferrer">@IndigoWizard</a> | Map Data: <a href="https://leafletjs.com/" target="_blank" rel="noopener noreferrer">Leaflet</a>, <a href="https://www.openstreetmap.org/about" target="_blank" rel="noopener noreferrer">OSM</a>, <a href="https://www.mapbox.com/about/maps" target="_blank" rel="noopener noreferrer">Mapbox</a>, <a href="https://www.usgs.gov/" target="_blank" rel="noopener noreferrer">USGS</a>
            """

            # add attribution control
            MyCustomAttribution(credit_html, position="bottomright").add_to(m)


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

            # Add Markers based on filters
            for place, mag, time_ms, lat, lon in zip(places, magnitudes, times, lats, longs):
                if mag is None:
                    continue
                event_dt = datetime.fromtimestamp(time_ms / 1000)
                event_date = event_dt.date()

                if start_date <= event_date <= end_date and mag <= magnitude_limit:
                    date_str = event_dt.strftime("%Y-%m-%d")
                    time_str = event_dt.strftime("%H:%M:%S")

                    popup_info = f"<div class='popinfo' style='width: max-content;'><h5><b>Earthquake Information</b></h5><b>Magnitude:</b> <span>{mag}</span><br><b>Date:</b> <span>{date_str}</span><br><b>Time:</b> <span>{time_str}</span><br><b>Location:</b> <span>{place}</span><br><b>Coordinates:</b> <span>{lat} , {lon}</span></div>"

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
            

            # folium useeful plugins
            ## fullscreen
            folium.plugins.Fullscreen(position="bottomright", title="Full Screen", title_cancel="Exit", force_separate_button=True).add_to(m)

            ## layer control
            folium.LayerControl(collapsed=True).add_to(m)

            # Display the map
            st_folium(m, width="stretch", height="600")

    st.divider()

    # stats section
    with st.container():
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


if __name__ == "__main__":
    main()
