import streamlit as st
import folium
from streamlit_folium import st_folium

def operation_maps():
    st.header("Карта Silo")
    st.caption("Автономный гео-мониторинг городской среды и фиксация точек кликами")

    if "target_points" not in st.session_state:
        st.session_state.target_points = []
    if "last_processed_click" not in st.session_state:
        st.session_state.last_processed_click = None

    if st.button("Очистить карту и сбросить точки", type="secondary", use_container_width=True):
        st.session_state.target_points = []
        st.session_state.last_processed_click = None
        st.rerun()

    center_lat, center_lon = 56.838926, 60.605702
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, control_scale=True)

    for idx, pt in enumerate(st.session_state.target_points):
        color = "green" if idx == 0 else "red"
        popup_text = "<b>Точка А (Старт)</b>" if idx == 0 else "<b>Точка Б (Финиш)</b>"
        folium.Marker(
            pt, 
            popup=popup_text, 
            tooltip=f"Маркер {idx + 1}",
            icon=folium.Icon(color=color, icon="location-arrow" if idx == 0 else "flag")
        ).add_to(m)

    # Вывод подсказок пользователю
    if len(st.session_state.target_points) == 0:
        st.info("Кликните на карту, чтобы установить Точку А (Старт).")
    elif len(st.session_state.target_points) == 1:
        st.warning("Точка А зафиксирована. Кликните на карту еще раз, чтобы установить Точку Б (Финиш).")
    elif len(st.session_state.target_points) == 2:
        st.success("Обе точки успешно установлены!")

    map_output = st_folium(m, key="tactical_autonomous_clean_map", use_container_width=True, height=600)

    if map_output and map_output.get("last_clicked"):
        current_click = map_output["last_clicked"]
        click_id = f"{current_click['lat']}_{current_click['lng']}"
        
        if click_id != st.session_state.last_processed_click:
            st.session_state.last_processed_click = click_id
            
            if len(st.session_state.target_points) < 2:
                new_point = [current_click["lat"], current_click["lng"]]
                st.session_state.target_points.append(new_point)
                st.rerun()
