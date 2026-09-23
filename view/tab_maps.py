import streamlit as st
import folium
from streamlit_folium import st_folium

def operation_maps():
    st.header("Карта Silo")
    st.caption("Автономная карта")

    center_lat, center_lon = 56.838926, 60.605702
    
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=13, 
        control_scale=True  # Удобная линейка масштаба в углу карты
    )

    folium.Marker(
        [center_lat, center_lon],
        popup="<b>Штаб Silo Core</b>",
        tooltip="Точка Альфа",
        icon=folium.Icon(color="green", icon="home")
    ).add_to(m)

    st_folium(m, key="tactical_silo_base_clean_map", use_container_width=True, height=550)
