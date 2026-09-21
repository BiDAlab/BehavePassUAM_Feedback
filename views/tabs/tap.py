import streamlit as st

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from utils import *

    
def graficar_distribucion_probabilidad(velocidad_reaccion,lang):
    # Leer los tiempos de reacción desde el archivo de texto
    tiempos_reaccion = []
    
    with open('static/analisis_distribucion_topos.txt', 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:  # Saltar la primera línea (encabezado)
            try:
                tiempo = float(line.strip())  # Convertir el valor a float
                tiempos_reaccion.append(tiempo)
            except ValueError:
                continue  # Ignorar líneas que no se pueden convertir a float

    # Convertir la lista de tiempos de reacción a un array de NumPy
    tiempos_reaccion = np.array(tiempos_reaccion)
    tiempos_reaccion_filtrados = tiempos_reaccion[tiempos_reaccion <= 1000]
    tiempos_reaccion_filtrados = tiempos_reaccion_filtrados[0 <= tiempos_reaccion_filtrados]

    if lang == "es":
        # Crear el gráfico
        figura = plt.figure(figsize=(5, 3))
        sns.kdeplot(tiempos_reaccion_filtrados, color='blue', label='Distribución de Probabilidad')

        # Calcular y dibujar la línea para el usuario
        if velocidad_reaccion != -1:
            plt.axvline(x=velocidad_reaccion, color='red', linestyle='-', label=f'Tu velocidad: {velocidad_reaccion:.1f} ms')

        # Etiquetas y título
        plt.title('Distribución de los Tiempos de Reacción', fontsize=12)
        plt.xlabel('Tiempo de Reacción (ms)', fontsize=8)
        plt.legend(['Población BehavePass', 'Tu velocidad'], fontsize=6)
    
    else: 
        # Crear el gráfico
        figura = plt.figure(figsize=(5, 3))
        sns.kdeplot(tiempos_reaccion_filtrados, color='blue', label='Probability Distribution')

        # Calcular y dibujar la línea para el usuario
        if velocidad_reaccion != -1:
            plt.axvline(x=velocidad_reaccion, color='red', linestyle='-', label=f'Your speed: {velocidad_reaccion:.1f} ms')

        # Labels and title
        plt.title('Reaction Time Distribution', fontsize=12)
        plt.xlabel('Reaction Time (ms)', fontsize=8)
        plt.legend(['BehavePass Population', 'Your Speed'], fontsize=6)
    

    # Ocultar el eje vertical
    plt.gca().axes.get_yaxis().set_visible(False)

    # Ajustar diseño y mostrar en Streamlit
    plt.tight_layout()
    st.pyplot(figura)
                        
                    
def render_tap_tab_json(json_usuario, lang, sessionsPerf):
    if lang == "es": #Versión español
                st.title('Rendimiento en el juego de los topos 🐭')
                st.header("¡Veamos tu velocidad de reacción 👆 y algunos datos interesantes sobre tu rendimiento!")

                sesiones = sessionsPerf
                dividers = ['blue', 'green', 'orange', 'red']

                datos_tap = json_usuario.get("tap", "Unknown")


                for sesion in sesiones:

                    num_Sesion=int(sesion[-1])
                    st.subheader(f'Datos de la sesión {num_Sesion}', divider=dividers[num_Sesion-1])
                    
                    velocidad_usuario = datos_tap['reaction_time'][sesion]
                    

                    # Comprobamos que hay datos para representar
                    if velocidad_usuario != -1:                
                        graficar_distribucion_probabilidad(velocidad_usuario,lang)
                        if velocidad_usuario < 300.0:
                            TextoVelocidad=f'<b>¡Impresionante!</b> Tu velocidad de reacción en esta sesión ({round(velocidad_usuario)}ms) está muy por encima de la media de los usuarios de BehavePassUAM.'
                            st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                            #st.write(f'¡Impresionante! Tu velocidad de reacción ({velocidad_usuario.mean().round()}ms) está por encima de la media de los usuarios de BehavePassUAM.')
                        elif velocidad_usuario > 300.0 and 600.0 > velocidad_usuario:
                            TextoVelocidad=f'Tu velocidad de reacción en esta sesión ({round(velocidad_usuario)}ms) está en el rango promedio (300ms - 600ms) de los usuarios de BehavePassUAM.'
                            st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                        elif 600.0 < velocidad_usuario:
                            TextoVelocidad=f'Tu velocidad de reacción en esta sesión ({round(velocidad_usuario)}ms) está por debajo de la media de los usuarios de BehavePassUAM. '
                            st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                            #st.write(f'Vaya... Tu velocidad de reacción ({velocidad_usuario.mean().round()}ms) está por debajo de la media de los usuarios de BehavePassUAM. ')

                        
                        #st.dataframe(df)
                    else:
                        st.warning(f'Vuelve cuando hayas completado la sesión {num_Sesion}')
                        
        
        
                        
    elif lang == "en": #Versión inglés
                st.title('Tap the mole 🐭')
                st.header("Let's see your reaction speed 👆 and some interesting facts about your performance!")
                sesiones = sessionsPerf
                dividers = ['blue', 'green', 'orange', 'red']
                datos_tap = json_usuario.get("tap", "Unknown")
                
                for sesion in sesiones:

                    num_Sesion=int(sesion[-1])
                    st.subheader(f'Session {num_Sesion}', divider=dividers[num_Sesion-1])
                    velocidad_usuario = datos_tap['reaction_time'][sesion]
                # Comprobamos que hay datos para representar
                    if velocidad_usuario != -1:                
                        graficar_distribucion_probabilidad(velocidad_usuario,lang)                
                        if velocidad_usuario < 300.0:
                            TextoVelocidad = f'<b>Impressive!</b> Your reaction speed in this session ({round(velocidad_usuario)}ms) is well above the average of BehavePassUAM users.'
                            st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                        elif 300.0 <= velocidad_usuario <= 600.0:
                            TextoVelocidad = f'Your reaction speed in this session ({round(velocidad_usuario)}ms) is within the average range (300ms - 600ms) of BehavePassUAM users.'
                            st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                        elif velocidad_usuario > 600.0:
                            TextoVelocidad = f'Your reaction speed in this session ({round(velocidad_usuario)}ms) is below the average of BehavePassUAM users.'
                            st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                    else:
                        st.warning(f'Please return after completing session {num_Sesion}.')
            
