import streamlit as st
from utils.ai_manager import check_ollama_status,send_message_to_ai
def operation_tab5() :
    '''Функция отвечает за логику работу пятой вкладки'''
    ai_ready = check_ollama_status()
    if ai_ready == False:
        st.warning("Нет связи с агентом. Запустите Ollama на ПК")
        st.stop()

    if "ai_talk" not in st.session_state:
        st.session_state.ai_talk = []

    sub_tab5_1, = st.tabs(['Беседа'])

    with sub_tab5_1 :
        st.subheader("Управление агентом")
    
        for message in st.session_state.ai_talk :
            with st.chat_message(message["role"]) :
                st.write(message["content"])
        
        if user_query := st.chat_input("Задайте вопрос ассистенту"):
            with st.chat_message("user"):
                st.write(user_query)
            st.session_state.ai_talk.append({"role": "user", "content": user_query})
            with st.spinner("Бортовой компьютер генерирует ответ..."):
                response = send_message_to_ai(st.session_state.ai_talk)
            st.session_state.ai_talk.append({"role": "assistant", "content": response})
            st.rerun()
        