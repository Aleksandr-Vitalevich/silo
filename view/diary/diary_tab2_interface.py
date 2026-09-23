import streamlit as st 
from db_manager import show_data_to_diary,delete_data_to_diary,show_data_to_diary_user_choise
from time import sleep
from utils.security import decrypt_text
from utils.ai_manager import check_ollama_status,send_message_to_ai

def operation_tab2() :
    '''Функция отвечает за логику работу второй вкладки'''
    st.subheader("Управление дневником")
    ai_ready = check_ollama_status()
    if ai_ready == False:
        st.warning("Нет связи с агентом. Запустите Ollama на ПК")
        st.stop()
    if 'ai_analize' not in st.session_state :
            st.session_state.ai_analize = []
    sub_tab_2_1,sub_tab_2_2,sub_tab_2_3 = st.tabs(["Получить записи","Удалить запись",'Анализ Дневника'])

    with sub_tab_2_1 :
        st.subheader('Меню мои записи')
        try :
            my_notes = show_data_to_diary()
        except Exception :
            st.error('Не удалось загрузить данные')
            my_notes = None
        if my_notes :
            master_pwd = st.session_state.master_password_key
            for note in my_notes :
                id, text, date = note
                decrypted_diary_text = decrypt_text(text,master_pwd)
                with st.chat_message("user", avatar="📝"):
                    st.caption(f"ID {id} Время: {date}")
                    st.write(decrypted_diary_text)

    with sub_tab_2_2 :
        st.subheader("Меню удаления записи")
        user_input = st.number_input('Введите id записи для удаления',step=1,min_value=1,key="delete_diary_record_id_input")
        if st.button("Удалить запись",use_container_width=True,key="delete_diary_button_click") :
            try :
                delete_file = delete_data_to_diary(user_input)
                if delete_file == "success" :
                    st.info(f"Удаление прошло успешно Запись с id = {user_input} удалена")
                    sleep(1.5)
                    st.rerun()
            except Exception :
                st.error('Ошибка при удалении записи')

    with sub_tab_2_3 :
        st.subheader("Анализ дневника")
        for message in st.session_state.ai_analize:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        count_to_analyze = st.number_input("Введите число записей для анализа",min_value=1)
        if st.button("Запустить анализ дневника",use_container_width=True,key="analyze_diary_button") :
            with st.spinner("Ассистент извлекает и анализирует данные") :
                diary_data = show_data_to_diary_user_choise(count_to_analyze)
                if not diary_data :
                    st.info("В вашем дневнике пока нет записей")
                else :
                    decrypted_text = []
                    user_password = st.session_state.master_password_key
                    for row in diary_data :
                        clean_text = decrypt_text(row[0],user_password)
                        decrypted_text.append(f'- {clean_text}')
                    text = '\n'.join(decrypted_text)
                    prompt_instruction = (
                    f"Система, перед тобой {count_to_analyze} последних записей из дневника владельца крепости. "
                    f"Проведи их глубокий анализ: выдели главные темы, отследи изменения в настроении и сформулируй "
                    f"краткие выводы. Отвечай строго на русском языке. Вот записи:\n\n{text}"
                    )
                            
                    st.session_state.ai_analize.append({"role": "user", "content": f"Запрос: Проанализируй мои последние {count_to_analyze} записей в Дневнике."})
                        
                        
                    temp_chat_context = st.session_state.ai_analize.copy()
                    temp_chat_context.append({"role": "user", "content": prompt_instruction})
                        
                        
                    ai_analysis_response = send_message_to_ai(temp_chat_context)
                        
                        
                    st.session_state.ai_analize.append({"role": "assistant", "content": ai_analysis_response})
        
                    st.rerun()