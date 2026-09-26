import streamlit as st
import folium
from streamlit_folium import st_folium
from db_manager.work_with_personal_map import get_all_points,add_new_point,delete_point,update_point
from utils.security import encrypt_text,decrypt_text

def operation_maps():
    st.header("🗺️ Карта и заметки Silo")
    st.caption("Заметки с привязкой к координатам города.")
    st.info("Выбирай и нажимай на карту. Карта обновится, но метка останется -> при обновлении карта возвращается к центру города. Ты можешь спокойно писать заметки внутри формы. Синим обозначены сохраненные заметки. Зеленным новые")
    password = st.session_state.master_password_key
    # Создаем три внутренние вкладки
    tab_view, tab_edit, tab_delete = st.tabs([
        "📍 Карта и Заметки", 
        "📝 Изменить заметку", 
        "🗑️ Удалить заметку"
    ])

    with tab_view:
        saved_points = get_all_points()

        if "current_click_coords" not in st.session_state:
            st.session_state.current_click_coords = None
        if "last_processed_click" not in st.session_state:
            st.session_state.last_processed_click = None

        center_lat, center_lon = 56.838926, 60.605702
        m = folium.Map(location=[center_lat, center_lon], zoom_start=13, control_scale=True)

        for pt in saved_points:
            pt_id, raw_title, raw_desc, lat, lon, created_at = pt
            title = decrypt_text(raw_title,password)
            desc = decrypt_text(raw_desc,password)
            
            popup_html = f"""
            <div style='font-family: Arial, sans-serif; width: 200px;'>
                <h4 style='margin:0 0 5px 0; color:#0078FF;'>{title}</h4>
                <p style='margin:0 0 8px 0; font-size:12px;'>{desc}</p>
                <hr style='border:0; border-top:1px solid #ccc; margin:5px 0;'>
                <span style='font-size:10px; color:#666;'>Фиксация: {created_at[:16]}</span>
            </div>
            """
            
            folium.Marker(
                [lat, lon],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=title,
                icon=folium.Icon(color="blue", icon="bookmark")
            ).add_to(m)

        if st.session_state.current_click_coords:
            folium.Marker(
                st.session_state.current_click_coords,
                popup="<b>Новая заметка</b>",
                icon=folium.Icon(color="green", icon="plus")
            ).add_to(m)

        map_output = st_folium(m, key="silo_geo_notepad_map", use_container_width=True, height=450)

        if map_output and map_output.get("last_clicked"):
            click_data = map_output["last_clicked"]
            click_id = f"{click_data['lat']}_{click_data['lng']}"
            
            if click_id != st.session_state.last_processed_click:
                st.session_state.last_processed_click = click_id
                st.session_state.current_click_coords = [click_data['lat'], click_data['lng']]
                st.rerun()

        if st.session_state.current_click_coords:
            st.write("---")
            st.subheader("📌 Ваши заметки, мысли в этой точке")
            st.caption(f"Координаты места: Широта {st.session_state.current_click_coords[0]:.5f} | Долгота {st.session_state.current_click_coords[1]:.5f}")
            
            with st.form("add_geo_note_form", clear_on_submit=True):
                note_title = st.text_input("Название гео-заметки (например, Склад Silo, Точка сбора) Обязательное поле")
                note_desc = st.text_area("Содержание оперативной заметки")
                
                submit = st.form_submit_button("Сохранить точку в базу данных", type="primary")
                if submit:
                    if note_title.strip():
                        args = {
                            "title": encrypt_text(note_title,password),
                            "description": encrypt_text(note_desc,password),
                            "latitude": st.session_state.current_click_coords[0],
                            "longitude": st.session_state.current_click_coords[1]
                        }
                        res = add_new_point(args)
                        if res == "success":
                            st.success("✅ Точка успешно зафиксирована в SQLite и зашифрована!")
                            st.session_state.current_click_coords = None  # Сбрасываем временный маркер
                            st.rerun()
                    else:
                        st.error("🚨 Название заметки не может быть пустым.")

    with tab_edit:
        st.subheader("📝 Меню редактирования заметок")
        all_pts = get_all_points()
        
        if not all_pts:
            st.info("База данных заметок пуста. Добавьте первую точку на карте.")
        else:
            note_options = {}
            for pt in all_pts:
                
                pt_id, enc_title, enc_desc, lat, lon, created_at = pt
                
                try:
                    clear_title = decrypt_text(enc_title, password)
                    clear_date = created_at[:16] # Первые 16 символов даты (ГГГГ-ММ-ДД ЧЧ:ММ)
                    
                    menu_label = f"📍 {clear_title} ({clear_date})"
                    
                    note_options[menu_label] = pt
                except Exception:
                    note_options[f"Объект ID {pt_id} (Ошибка расшифровки)"] = pt
            selected_option = st.selectbox("Выберите заметку для изменения:", list(note_options.keys()))
            
            if selected_option:
                target_pt = note_options[selected_option]
                pt_id, raw_title, raw_desc, lat, lon, _ = target_pt
                current_title = decrypt_text(raw_title,password)
                current_desc = decrypt_text(raw_desc,password)
                with st.form("edit_geo_note_form"):
                    new_title = st.text_input("Новое название заметки:", value=current_title)
                    new_desc = st.text_area("Новое содержание:", value=current_desc)
                    
                    update_submit = st.form_submit_button("Сохранить изменения", type="primary")
                    if update_submit:
                        if new_title.strip():
                            args = {
                                "title": encrypt_text(new_title,password),
                                "description": encrypt_text(new_desc,password)
                            }
                            if update_point(pt_id, args) == "success":
                                st.success("✅ Данные заметки успешно обновлены в базе!")
                                import time
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("🚨 Название не может быть пустым.")
    with tab_delete:
        st.subheader("🗑️ Меню удаления заметок")
        all_pts = get_all_points()
        
        if not all_pts:
            st.info("Удалять нечего, на карте нет сохраненных маркеров.")
        else:
            for pt in all_pts:
                pt_id, raw_title, raw_desc, lat, lon, date = pt
                title = decrypt_text(raw_title,password)
                desc = decrypt_text(raw_desc,password)
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"📍 **{title}** <span style='font-size:11px; color:#888;'>({date[:16]})</span>", unsafe_allow_html=True)
                    st.caption(f"Координаты: {lat:.4f}, {lon:.4f} | _{desc}_")
                with col2:
                    if st.button("Удалить", key=f"del_btn_{pt_id}", type="secondary"):
                        if delete_point(pt_id) == "success":
                            st.success(f"🗑️ Точка '{title}' стерта из SQLite!")
                            st.rerun()
                st.write("---")
