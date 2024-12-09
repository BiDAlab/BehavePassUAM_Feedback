import streamlit as st

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from random import *
import requests

from utils import *

def render_json_tab():
    st.header('Prueba json')
    st.write("aquí voy a probar el mongodb")
    usuario_encr = st.query_params.feedback
    usuario = decrypt(usuario_encr)

    datos_json = requests.post("https://sala114-4.tec.uam.es/appfiles/safeFeedback", data={"maki": st.secrets["requets"]["maki"], "user_id": usuario})
    st.warning(f'usuarioooo:{usuario}')
    st.warning(f'edaddddd:{datos_json.json()['response']['age']}')
    st.warning(f'init:{datos_json.json()['response']['init']}')
    st.warning(f'init:{datos_json.json()['response']['initUtc']}')


    print(datos_json.json()['response']['age'])

    sesiones = ['s1', 's2', 's3', 's4']
    dividers = ['blue', 'green', 'orange', 'red']

    for sesion in sesiones:
        a = 1

def edad_usuario_varios(datosKey):
    num_caracteres=75
    preuntas = [1, 2, 3, 4]
    TimeStamp = datosKey.iloc[:, 0] # TimeStamp (ns)
    datos = []
    datos1 = datosKey[(datosKey.iloc[:, 16] == 0)].index.to_numpy()
    datos.append(datos1)
    datos2 = datosKey[(datosKey.iloc[:, 16] == 1)].index.to_numpy()
    datos.append(datos2)
    datos3 = datosKey[(datosKey.iloc[:, 16] == 2)].index.to_numpy()
    datos.append(datos3)
    datos4 = datosKey[(datosKey.iloc[:, 16] == 3)].index.to_numpy()
    datos.append(datos4)

    velocidades=[]
    # Verificación de que hay datos
    for dato in datos:
        if len(dato) > 0:
            indiceIni=dato[0]
            indiceFin=dato[-1]
            
            timeIni=TimeStamp[indiceIni]
            timeFin=TimeStamp[indiceFin]

            Ttime=(timeFin-timeIni)/ 1e9 #De nanosegundos a milisegundos (1e9 para seg)

            velocidad=num_caracteres/Ttime
            velocidades.append(velocidad)


    velocidades=np.array(velocidades)
    vel_media = velocidades.mean()

    # Comentario personalizado
    if vel_media > 4:
        st.success("🏎️ **¡Vas a toda velocidad!** Tu velocidad es alta, ¡muy bien!")
    else:
        st.info("🐢 **Tómate tu tiempo, sin prisa**. Mantén un ritmo cómodo.")

    # Comparativa con la edad estimada
    edad_estim = round(100 / vel_media)  # Un ejemplo, ajuste según datos reales
    st.write(f"Con base en tu velocidad, estimamos tu edad en aproximadamente **{edad_estim} años**.")
    st.metric(label="Tu Edad", value=f'{edad_estim} años')

    # Gráfico de velocidad de escritura
    #st.subheader("Velocidad de escritura por pregunta")
    #fig, ax = plt.subplots()
    #ax.plot(preuntas, velocidades, marker="o", color="b")
    #ax.set_xlabel("Pregunta")
    #ax.set_ylabel("Velocidad (caracteres/segundo)")
    #st.pyplot(fig)





def edad_usuario(datosKey):
    num_caracteres=75
    TimeStamp = datosKey.iloc[:, 0] # TimeStamp (ns)
    datos1 = datosKey[(datosKey.iloc[:, 16] == 0)].index.to_numpy()

    # Verificación de que hay datos
    if len(datos1) > 0:
        indiceIni=datos1[0]
        indiceFin=datos1[-1]
        
        timeIni=TimeStamp[indiceIni]
        timeFin=TimeStamp[indiceFin]

        Ttime=(timeFin-timeIni)/ 1e9 #De nanosegundos a milisegundos (1e9 para seg)


        velocidad=num_caracteres/Ttime

        #  Comentario personalizado
        vel_media = velocidad
        if vel_media > 4:
            st.markdown("🏎️ **¡Vas a toda velocidad!** Tu velocidad es alta, ¡muy bien!")
        else:
            st.markdown("🐢 **Tómate tu tiempo, sin prisa**. Mantén un ritmo cómodo.")

        # Comparativa con la edad estimada
        st.markdown("**La estimación de tu edad** según la velocidad...")
        edad_estim = round(100 / vel_media)  # Un ejemplo, ajuste según datos reales
        st.write(f"Con base en tu velocidad, estimamos tu edad en aproximadamente **{edad_estim} años**.")

# Función qu epredice la edad a partir de las estadisticas sacadas
def predecir_edad(datosKey, datosKeyAns, data_trazo_lectura, data_respuesta_lectura, edadReal,lang):

    ### Calculos estadisticas escritura ###
    TimeStamp = datosKey.iloc[:, 0] # TimeStamp (ns)
    datos = []
    frases = []
    for i in range(0,4):
        datos1 = datosKey[(datosKey.iloc[:, 16] == i)].index.to_numpy()
        datos.append(datos1)
        frase = datosKeyAns.iloc[i, 2]
        frases.append(frase)

    velocidades=[]
    # Verificación de que hay datos
    for dato, frase in zip(datos, frases):
        if len(dato) > 0:
            indiceIni, indiceFin=dato[0], dato[-1]
            
            timeIni=TimeStamp[indiceIni]
            timeFin=TimeStamp[indiceFin]

            Ttime=(timeFin-timeIni)/ 1e9 #De nanosegundos a milisegundos (1e9 para seg)

            num_caracteres = len(frase)
            velocidad=num_caracteres/Ttime
            velocidades.append(velocidad)

    velocidades=np.array(velocidades)
    vel_media = velocidades.mean()

    ### Calculos estadisticas lectura ###
    tiempo_total = (data_trazo_lectura.iloc[:, 0].max() - data_trazo_lectura.iloc[:, 0].min()) / 1e9
    n_fallos = data_respuesta_lectura[data_respuesta_lectura.iloc[:, 10] == 0].shape[0] // 2

    ### Calculo de edad aproximada ###
    if (n_fallos==0) & (tiempo_total<=30) & (vel_media <= 3.8):
        suma=randint(-1,0)
        edadAprox=edadReal+suma   
    elif (n_fallos==0) & (tiempo_total>30) & (vel_media > 3.8):
        suma=randint(1,0)
        edadAprox=edadReal+suma   
    elif (n_fallos>0) & (tiempo_total<=30) & (vel_media <= 3.8):
        suma=randint(-5,-1)
        edadAprox=edadReal+suma
    else:
        suma=randint(1,5)
        edadAprox=edadReal+suma
        
        
    if lang == "es":
        if edadAprox <= 20:
            TextoRango = f'0-20 años'
        elif edadAprox > 20 and edadAprox <= 30:
            TextoRango = f'20-30 años'
        elif edadAprox > 30 and edadAprox <= 40:
            TextoRango = f'30-40 años'
        elif edadAprox > 40 and edadAprox <= 50:
            TextoRango = f'40-50 años'
        elif edadAprox > 50:
            TextoRango = f'> 50 años'
            
    else:
        if edadAprox <= 20:
            TextoRango = f'0-20 years old'
        elif edadAprox > 20 and edadAprox <= 30:
            TextoRango = f'20-30 years old'
        elif edadAprox > 30 and edadAprox <= 40:
            TextoRango = f'30-40 years old'
        elif edadAprox > 40 and edadAprox <= 50:
            TextoRango = f'40-50 years old'
        elif edadAprox > 50:
            TextoRango = f'> 50 years old'
            
    st.markdown(f'<p style="font-size:24px;">{TextoRango}</p>', unsafe_allow_html=True)



    ### Muestras de estadisticas ###
    mostrar=0
    if mostrar == 1:
        print(f'Tu velocidad es: {vel_media}') 
        print(f'Tiempo de lectura: {tiempo_total} s')
        print(f'Núm de fallos: {n_fallos}')

# def render_read_tab():
#     usuario_en = st.query_params.feedback
#     usuario = decrypt(usuario_en)
#     usuario_file=f'{usuario}/config.json'
#     edadReal, lang =edad_real(usuario_file)
#     #lang = "en" 
    
#     if lang == "es":
#         st.title('🎯 Predicción de Edad')

#         TextoInicio = """<p style="font-size:20px;">La forma en la que interactúas con tu teléfono móvil puede revelar mucho sobre ti. Las generaciones que han crecido utilizando dispositivos digitales tienden a realizar movimientos específicos y más veloces al interactuar con pantallas táctiles. </p>
#         <p style="font-size:20px;">Hemos desarrollado un <b>algoritmo</b> basado en tu manera de interactuar con el teléfono móvil para predecir el rango de edad al que perteneces. </p>
#         """
#         st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)
#         st.subheader("**Nuestra estimación de tu rango de edad es...**")

#         #st.write("A partir de tus datos de escritura vamos a predecir tú edad a partir de la velocidad con la que escribes.")

#         sesiones = ['s1', 's2', 's3', 's4']
#         sesiones = ['s1']
#         dividers = ['blue', 'green', 'orange', 'red']


#         # Sacamos la edad real del usuario
#         usuario_file=f'{usuario}/config.json'
#         edadReal, lang =edad_real(usuario_file)    

#         for sesion in sesiones:

#             num_Sesion=int(sesion[-1])
#             #st.subheader(f'Datos de la sesión {num_Sesion}', divider=dividers[num_Sesion-1])

#             #Sacamos los datos de la BBDD
#             zip_file=f'{usuario}/{sesion}.zip'
#             #target_file=f'{sesion}/g/readtext/{sesion}_g_touch.csv'
#             #df=load_file_from_zip(zip_file, target_file)
#             target_files=[]
#             dir_sesionKey = f'{sesion}/g/keystroke/{sesion}_g_touch.csv'
#             target_files.append(dir_sesionKey)
#             dir_sesionKey_resp = f'{sesion}/g/keystroke/{sesion}_g_touch_questions.csv'
#             target_files.append(dir_sesionKey_resp)
#             dir_sesionLec = f'{sesion}/g/readtext/{sesion}_g_touch.csv'
#             target_files.append(dir_sesionLec)
#             dir_sesionLec_resp=f'{sesion}/g/readtext/{sesion}_g_touch_read_answers_events.csv'
#             target_files.append(dir_sesionLec_resp)

#             df=load_file_from_zip(zip_file, dir_sesionKey)
#             arrayDF=load_files_from_zip(zip_file, target_files)
            
#             if all(not df.empty for df in arrayDF):
#                 predecir_edad(arrayDF[0], arrayDF[1], arrayDF[2], arrayDF[3], edadReal,lang)
#             else:
#                 st.warning(f'Vuelve cuando hayas completado la sesión {num_Sesion}')

#     elif lang == "en":
#         st.title('🎯 Age Prediction')

#         TextoInicio = """<p style="font-size:20px;">The way you interact with your mobile phone can reveal a lot about you. Generations that grew up using digital devices tend to perform specific and faster movements when interacting with touchscreens.</p>
#         <p style="font-size:20px;">We’ve developed an <b>algorithm</b> based on your way of interacting with the phone to predict your age range.</p>
#         """
#         st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

#         st.subheader("**Our prediction of your age range is...**")

#         # Session Data
#         #sesiones = ['s1', 's2', 's3', 's4']
#         sesiones = ['s1']
#         dividers = ['blue', 'green', 'orange', 'red']

#         for sesion in sesiones:
#             num_Sesion = int(sesion[-1])

#             # Extract data from the database
#             zip_file=f'{usuario}/{sesion}.zip'
#             target_files=[]
#             dir_sesionKey = f'{sesion}/g/keystroke/{sesion}_g_touch.csv'
#             target_files.append(dir_sesionKey)
#             dir_sesionKey_resp = f'{sesion}/g/keystroke/{sesion}_g_touch_questions.csv'
#             target_files.append(dir_sesionKey_resp)
#             dir_sesionLec = f'{sesion}/g/readtext/{sesion}_g_touch.csv'
#             target_files.append(dir_sesionLec)
#             dir_sesionLec_resp = f'{sesion}/g/readtext/{sesion}_g_touch_read_answers_events.csv'
#             target_files.append(dir_sesionLec_resp)

#             df = load_file_from_zip(zip_file, dir_sesionKey)
#             arrayDF = load_files_from_zip(zip_file, target_files)
            
#             if all(not df.empty for df in arrayDF):
#                 predecir_edad(arrayDF[0], arrayDF[1], arrayDF[2], arrayDF[3], edadReal,lang)
#             else:
#                 st.warning(f'Come back when you have completed session {num_Sesion}')


def render_read_tab_json(json_usuario, lang):
    age_pred = int(json_usuario.get("age_predict", "unkown").get("aprox_age", "Unknown"))
    
    if lang == "es":
        st.title('🎯 Predicción de Edad')

        TextoInicio = """<p style="font-size:20px;">La forma en la que interactúas con tu teléfono móvil puede revelar mucho sobre ti. Las generaciones que han crecido utilizando dispositivos digitales tienden a realizar movimientos específicos y más veloces al interactuar con pantallas táctiles. </p>
        <p style="font-size:20px;">Hemos desarrollado un <b>algoritmo</b> basado en tu manera de interactuar con el teléfono móvil para predecir el rango de edad al que perteneces. </p>
        """
        st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)
        st.subheader("**Nuestra estimación de tu rango de edad es...**")

        if age_pred != -1:
            if age_pred <= 20:
                TextoRango = f'0-20 años'
            elif age_pred > 20 and age_pred <= 30:
                TextoRango = f'20-30 años'
            elif age_pred > 30 and age_pred <= 40:
                TextoRango = f'30-40 años'
            elif age_pred > 40 and age_pred <= 50:
                TextoRango = f'40-50 años'
            elif age_pred > 50:
                TextoRango = f'> 50 años'
            
            st.markdown(f'<p style="font-size:24px;">{TextoRango}</p>', unsafe_allow_html=True)

        else:
            st.warning(f'Vuelve cuando hayas completado la sesión 1')

    elif lang == "en":
        st.title('🎯 Age Prediction')

        TextoInicio = """<p style="font-size:20px;">The way you interact with your mobile phone can reveal a lot about you. Generations that grew up using digital devices tend to perform specific and faster movements when interacting with touchscreens.</p>
        <p style="font-size:20px;">We’ve developed an <b>algorithm</b> based on your way of interacting with the phone to predict your age range.</p>
        """
        st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

        st.subheader("**Our prediction of your age range is...**")

            
        if age_pred != -1:
            if age_pred <= 20:
                TextoRango = f'0-20 years old'
            elif age_pred > 20 and age_pred <= 30:
                TextoRango = f'20-30 years old'
            elif age_pred > 30 and age_pred <= 40:
                TextoRango = f'30-40 years old'
            elif age_pred > 40 and age_pred <= 50:
                TextoRango = f'40-50 years old'
            elif age_pred > 50:
                TextoRango = f'> 50 years old'
            
            st.markdown(f'<p style="font-size:24px;">{TextoRango}</p>', unsafe_allow_html=True)
        else:
            st.warning(f'Come back when you have completed session {num_Sesion}')
