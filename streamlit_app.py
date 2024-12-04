import json
import time

import streamlit as st
from streamlit_lottie import st_lottie

from utils.enums import TabsEnums

from utils import connect_ftps, list_files, decrypt


# Page configuration
st.set_page_config(page_title='BehavePassUAM', layout='wide', page_icon='📱')

# Conectar al servidor FTPS
ftps = connect_ftps()

# Función para verificar si el participante existe
def participant_exists(participant_id: str) -> bool:
    usuarios = list_files()
    return participant_id in usuarios

# Run once flag
if 'run_once' not in st.session_state:
    st.session_state.run_once = True
    st.session_state.selected_tab_id = TabsEnums.SUMMARY.value

# Display the logo animation at the start of the app
if st.session_state.run_once:
    logo_holder = st.empty()

    with logo_holder.container():

        lottie_path = 'static/logo_bida.json'
        lottie_json = json.load(open(lottie_path))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.markdown("<h1 style='text-align: center; color: #1fa5da; font-family: Arial;'> BehavePassUAM</h1>", unsafe_allow_html=True)
            st_lottie(lottie_json, key='user', loop=False)
        with col3:
            st.write(' ')

        time.sleep(2)

    logo_holder.empty()
    st.session_state.run_once = False

### Start of get params ####
# Sacamos los parametro de la URL participant_id
participant_id_enc = st.query_params.get("feedback")#, [None])[0]


# Verificamos si el ID es válido
if participant_id_enc:
    # Desencriptamos el usuario
        participant_id=decrypt(participant_id_enc)

        if True:
        #if participant_exists(participant_id):
            # Navigation pages definition
            views = {
                'Resources': [
                st.Page('views/dashboard.py', title='BehavePassUAM', icon='📱', default=True),
                ],
            }

            # Start the navigation
            pg = st.navigation(views, expanded=True)
            pg.run()
        else:
            st.error("ID inválido. Verifica el link o contacta con soporte.")
            st.error("Invalid ID. Verify the link.")

else:
    st.error("⚠️ No sé encuentra usuario. Verifica el link o contacta con soporte.")
    st.error(" ⚠️ We could not find the user. Verify the link or contact us.")
    info_message=f"""<p style="text-align:center;"> 🤔 ¿No sábes que es 
            <a href="https://behavepassuam.humanairesearch.com/es" target="_blank" style="text-decoration:none; color: inherit; font-weight: bold;"> BehavePassUAM</a>? </p> 
            <p style="text-align:center;"> 👉 <strong>No te quedes con la duda</strong>, entra en nuestra página web 🌐 (<a href="https://behavepassuam.humanairesearch.com/es" target="_blank" style="text-decoration:none; color: inherit; font-weight: bold;"><u>https://behavepassuam.humanairesearch.com/es</u></a>) y descubre de qué se trata 😊</p>"""
    
    st.markdown(f"""<div style="border: 10px solid #e7f3fe; padding: 10px; border-radius: 15px; font-size: 17px; background-color: transparent;"> {info_message}</div>""",unsafe_allow_html=True)
    st.markdown(' ')
    
    info_message_eng=f"""<p style="text-align:center;"> 🤔 Don't know about
            <a href="https://behavepassuam.humanairesearch.com/es" target="_blank" style="text-decoration:none; color: inherit; font-weight: bold;"> BehavePassUAM</a>? </p> 
            <p style="text-align:center;"> 👉 Visit out website 🌐 (<a href="https://behavepassuam.humanairesearch.com/es" target="_blank" style="text-decoration:none; color: inherit; font-weight: bold;"><u>https://behavepassuam.humanairesearch.com/es</u></a>) and find out what is all about 😊</p>"""
    st.markdown(f"""<div style="border: 10px solid #e7f3fe; padding: 10px; border-radius: 15px; font-size: 17px; background-color: transparent;"> {info_message_eng}</div>""",unsafe_allow_html=True)
    
### End of get params ###
