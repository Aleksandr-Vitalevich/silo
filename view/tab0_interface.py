import streamlit as st

def operation_tab0() :
    '''Функция отвечает за логику работу пятой вкладки'''
    st.subheader("Выход")

    if st.button("Выход",use_container_width=True) :
            st.session_state.authorization_user = False
            st.rerun()