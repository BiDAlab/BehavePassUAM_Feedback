from datetime import datetime

import extra_streamlit_components as stx
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import requests

from utils import *
from utils.enums import TabsEnums
from views.tabs import *


usuario_en = st.query_params.feedback
usuario = decrypt(usuario_en)
usuario_file=f'{usuario}/config.json'
#edadReal, lang =edad_real(usuario_file)
#lang = "en" 
json_usuario = connect_mongodb(usuario)
lang = json_usuario.get("lang", "Unknown")

### Start of Sidebar content ###
with st.sidebar:
    # Set the title and logo
    st.logo('static/images/BPUAM_logo.png', size='large')
    st.sidebar.title('BehavePassUAM')
    if lang == "es":
        info_message = "BehavePassUAM es un proyecto de investigación del grupo BiDA Lab de la Universidad Autónoma de Madrid. El principal objetivo es desarrollar sistemas de reconocimiento biométrico basados en la interacción con el dispositivo móvil."
    else:
        info_message = "BehavePassUAM is a research project from the BiDA Lab group at the Universidad Autónoma de Madrid. The main goal is to develop biometric recognition systems based on interaction with mobile devices."

    st.markdown(f'<div style="padding: 10px; border-radius: 15px  font-size: 17px;">{info_message}</div>', unsafe_allow_html=True)

    # Set a divider
    st.divider()

    #Apartado RRSS
    if lang == "es":
        st.title("Síguenos en nuestras redes")
    else:
        st.title("Follow us on social media")

    # Twitter
    st.markdown('''
        <a href="https://x.com/i/flow/login?redirect_after_login=%2Fbehavepassuam" target="_blank" style="text-decoration:none;">
            🐦 Twitter
        </a>
    ''', unsafe_allow_html=True)

    # Instagram
    st.markdown('''
        <a href="https://www.instagram.com/behavepassuam/?igsh=OHk5OXlnZG90cGFv" target="_blank" style="text-decoration:none;">
            📸 Instagram
        </a>
    ''', unsafe_allow_html=True)

    # Facebook
    st.markdown('''
        <a href="https://www.facebook.com/people/Behavepassuam/61567187651116/" target="_blank" style="text-decoration:none;">
            📘 Facebook
        </a>
    ''', unsafe_allow_html=True)

    # Página Web
    st.markdown('''
        <a href="https://behavepassuam.humanairesearch.com/es" target="_blank" style="text-decoration:none;">
            💻 Web
        </a>
    ''', unsafe_allow_html=True)

    # Set a divider
    st.divider()

    # Set de acknowledgements images
    st.sidebar.image('static/images/logo_bida.png', use_column_width=True, clamp=True)
    st.sidebar.image('static/images/logo_UAM.png', use_column_width=True, clamp=True)

#### End of Sidebar content ####

#### Start of Tabs content ####

# Tabs definition
# Crear los botones para cada sección
col1, col2, col3 = st.columns(3)

if lang == "es":
    with col1:
        if st.button("Información", icon="📊", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.SUMMARY.value
        if st.button("Tap el Topo", icon="🐹", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.TAP.value

    with col2:
        if st.button("Firma",  icon="✒️", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.SIGN.value
        if st.button("Memoria Visual", icon="🖼️", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.GALLERY.value
    with col3:
        if st.button("Patrón",icon="🔒", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.PATTERN.value
        if st.button("Predicción de Edad", icon="🎯", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.READ.value
else:
    with col1:
        if st.button("Summary", icon="📊", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.SUMMARY.value
        if st.button("Tap the Mole", icon="🐹", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.TAP.value

    with col2:
        if st.button("Signature",  icon="✒️", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.SIGN.value
        if st.button("Visual Memory", icon="🖼️", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.GALLERY.value
    with col3:
        if st.button("Pattern",icon="🔒", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.PATTERN.value
        if st.button("Age Prediction", icon="🎯", use_container_width=True):
            st.session_state.selected_tab_id = TabsEnums.READ.value

    
# Renderizar la pestaña seleccionada
if st.session_state.selected_tab_id == TabsEnums.SUMMARY.value:
    render_summary_tab()
elif st.session_state.selected_tab_id == TabsEnums.TAP.value:
    render_summary_tab()
elif st.session_state.selected_tab_id == TabsEnums.READ.value:
    st.warning(f"{json_usuario}")
    #render_tap_tab_json(json_usuario, lang)
elif st.session_state.selected_tab_id == TabsEnums.SIGN.value:
    st.warning(f"{json_usuario}")
    #render_tap_tab_json(json_usuario, lang)
elif st.session_state.selected_tab_id == TabsEnums.PATTERN.value:
    st.warning(f"{json_usuario}")
    #render_tap_tab_json(json_usuario, lang)
elif st.session_state.selected_tab_id == TabsEnums.GALLERY.value:
    st.warning(f"{json_usuario}")
    #render_tap_tab_json(json_usuario, lang)

# if st.session_state.selected_tab_id == TabsEnums.SUMMARY.value:
#     render_summary_tab()
# elif st.session_state.selected_tab_id == TabsEnums.TAP.value:
#     render_tap_tab()
# elif st.session_state.selected_tab_id == TabsEnums.READ.value:
#     render_read_tab()
# elif st.session_state.selected_tab_id == TabsEnums.SIGN.value:
#     render_sign_tab()
# elif st.session_state.selected_tab_id == TabsEnums.PATTERN.value:
#     render_pattern_tab()
# elif st.session_state.selected_tab_id == TabsEnums.GALLERY.value:
#     render_galeria_tab()