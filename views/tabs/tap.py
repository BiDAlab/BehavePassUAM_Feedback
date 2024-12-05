import streamlit as st

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from utils import *

def calculos_topos(datosTopo):
    #Guardamos los datos que vamos a necesitar
    TimeStamp = datosTopo.iloc[:, 0] # TimeStamp (ns)
    finger_down = datosTopo[(datosTopo.iloc[:, 8] == 0)].index.to_numpy()
    finger_up = datosTopo[(datosTopo.iloc[:, 8] == 1)].index.to_numpy()

    TiemposPulsa=[]
    TiemposReac=[] 

    # Verificación de que hay datos
    if len(finger_down) > 0 and len(finger_up) > 0:

        for i in range(len(finger_down)): 
            # Claculamos el tiempo que tarda en pulsar
            tiem_pul = (TimeStamp[finger_up[i]] - TimeStamp[finger_down[i]]) / 1e6 #De nanosegundos a milisegundos (1e9 para seg)
            TiemposPulsa.append(tiem_pul)

            #Calcualmos los tiempos de reaccion
            if i < len(finger_down)-1:
                tiem_rea = (TimeStamp[finger_down[i+1]] - TimeStamp[finger_up[i]]) / 1e6 #De nanosegundos a milisegundos
                TiemposReac.append(tiem_rea)
    
    # Pasamos las listas a arrays para poder hacer métricas
    TiemposPulsa = np.array(TiemposPulsa)
    TiemposReac = np.array(TiemposReac)

    # Calculamos métricas
    promedio_reaccion = TiemposReac.mean()
    velocidad_reaccion = 1 / promedio_reaccion
    min_reaccion = TiemposReac.min()
    max_reaccion = TiemposReac.max()
    consistencia = TiemposReac.std()

    # Mensaje motivacional
    if promedio_reaccion < 300:
        st.success(" 🏆 ¡Increíble! ¡Tienes un tiempo de reacción excelente! !Tienes una velocidad más rápida que el 90% de las personas!")
    elif 300 < promedio_reaccion < 400:
        st.info(" 🤩 Buen trabajo, tienes un tiempo de reacción muy bueno. ¡Tú velocidad de reacción esta entre el 75% de las personas más rápidas!")
    elif 400 < promedio_reaccion < 500:
        st.info(" 😀 Que bien lo has hecho, sigue practicando para mejorar aún más. !Tienes una velocidad más rápida que el 50% de las personas!")
    else:
        st.info("  😊 ¡Se que puedes dar más de ti! Sigue intentándolo. ¡Tú velocidad de reacción esta entre el 25% de las personas más rápidas!")

    # Mostrar métricas
    st.metric(label="Velocidad de reacción (topos/ms)", value=f"{velocidad_reaccion:.4f}")
    st.metric(label="Tiempo de reacción promedio (ms)", value=f"{promedio_reaccion:.2f}")
    st.metric(label="Reacción más rápida (ms)", value=f"{min_reaccion:.2f}")
    st.metric(label="Reacción más lenta (ms)", value=f"{max_reaccion:.2f}")
    st.metric(label="Consistencia (ms)", value=f"{consistencia:.2f}")

    # Gráfico de tiempos de reacción
    st.subheader("Evolución de tu tiempo de reacción")
    fig, ax = plt.subplots()
    ax.plot(TiemposReac, marker="o", color="blue")
    ax.set_xlabel("Intento")    
    ax.set_ylabel("Tiempo de Reacción (ms)")
    ax.set_title("Evolución de los tiempos de reacción")
    st.pyplot(fig)

    # Histograma
    st.subheader("Distribución de tus tiempos de reacción")
    fig, ax = plt.subplots()
    ax.hist(TiemposReac, bins=5, color="green", alpha=0.7)
    ax.set_xlabel("Tiempo de Reacción (ms)")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)  
    
def calcular_tiempos_reaccion(datosTopo):
    # Guardamos los datos necesarios
    TimeStamp = datosTopo.iloc[:, 0]  # TimeStamp (ns)
    finger_down = datosTopo[(datosTopo.iloc[:, 8] == 0)].index.to_numpy()
    finger_up = datosTopo[(datosTopo.iloc[:, 8] == 1)].index.to_numpy()

    TiemposReac = []

    # Verificación de que hay datos
    if len(finger_down) > 0 and len(finger_up) > 0:
        for i in range(len(finger_down)): 
            # Calcular los tiempos de reacción
            if i < len(finger_down) - 1:
                tiem_rea = (TimeStamp[finger_down[i+1]] - TimeStamp[finger_up[i]]) / 1e6  # De nanosegundos a milisegundos
                TiemposReac.append(tiem_rea)
    
    return np.array(TiemposReac)
    
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
        if velocidad_reaccion is not -1:
            plt.axvline(x=velocidad_reaccion, color='red', linestyle='-', label=f'Tu velocidad: {velocidad_reaccion:.1f} ms')

        # Etiquetas y título
        plt.title('Distribución de los Tiempos de Reacción', fontsize=12)
        plt.xlabel('Tiempo de Reacción (ms)', fontsize=8)
        plt.legend(['Población BehavePass', 'Tu velocidad'], fontsize=6)
    
    else: 
        # Create the plot
        figura = plt.figure(figsize=(5, 3))
        sns.kdeplot(tiempos_reaccion_filtrados, color='blue', label='Probability Distribution')

        # Calculate and draw the line for the user
        user_line = calcular_tiempos_reaccion(topo_user)
        if user_line is not None:
            plt.axvline(x=user_line.mean(), color='red', linestyle='-', label=f'Your speed: {user_line.mean():.1f} ms')

        # Labels and title
        plt.title('Reaction Time Distribution', fontsize=12)
        plt.xlabel('Reaction Time (ms)', fontsize=8)
        plt.legend(['BehavePass Population', 'Your Speed'], fontsize=6)


    # Ocultar el eje vertical
    plt.gca().axes.get_yaxis().set_visible(False)

    # Ajustar diseño y mostrar en Streamlit
    plt.tight_layout()
    st.pyplot(figura)




def render_tap_tab():
    usuario_en = st.query_params.feedback
    usuario = decrypt(usuario_en)
    usuario_file=f'{usuario}/config.json'
    edadReal, lang =edad_real(usuario_file)
    #lang = "en" 
    
    if lang == "es": #Versión español
        st.title('Rendimiento en el juego de los topos 🐭')
        st.header("¡Veamos tu velocidad de reacción 👆 y algunos datos interesantes sobre tu rendimiento!")

        sesiones = ['s1', 's2', 's3', 's4']
        dividers = ['blue', 'green', 'orange', 'red']

        usuario_en = st.query_params.feedback
        usuario = decrypt(usuario_en)

        for sesion in sesiones:

            num_Sesion=int(sesion[-1])
            st.subheader(f'Datos de la sesión {num_Sesion}', divider=dividers[num_Sesion-1])

            #Sacamos los datos de la BBDD
            zip_file=f'{usuario}/{sesion}.zip'
            target_file=f'{sesion}/g/tap/{sesion}_g_touch.csv'
            try:
                df=load_file_from_zip(zip_file, target_file)
            except:
                df = pd.DataFrame()  # DataFrame vacío en caso de error

            # Comprobamos que hay datos para representar
            if not df.empty:
                velocidad_usuario = calcular_tiempos_reaccion(df)
                
                graficar_distribucion_probabilidad(df,lang)
                if velocidad_usuario.mean() < 300.0:
                    TextoVelocidad=f'<b>¡Impresionante!</b> Tu velocidad de reacción en esta sesión ({velocidad_usuario.round()}ms) está muy por encima de la media de los usuarios de BehavePassUAM.'
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                    #st.write(f'¡Impresionante! Tu velocidad de reacción ({velocidad_usuario.mean().round()}ms) está por encima de la media de los usuarios de BehavePassUAM.')
                elif velocidad_usuario.mean() > 300.0 and 600.0 > velocidad_usuario.mean():
                    TextoVelocidad=f'Tu velocidad de reacción en esta sesión ({velocidad_usuario.round()}ms) está en el rango promedio (300ms - 600ms) de los usuarios de BehavePassUAM.'
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                elif 600.0 < velocidad_usuario.mean():
                    TextoVelocidad=f'Tu velocidad de reacción en esta sesión ({velocidad_usuario.round()}ms) está por debajo de la media de los usuarios de BehavePassUAM. '
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                    #st.write(f'Vaya... Tu velocidad de reacción ({velocidad_usuario.mean().round()}ms) está por debajo de la media de los usuarios de BehavePassUAM. ')

                
                #st.dataframe(df)
            else:
                st.warning(f'Vuelve cuando hayas completado la sesión {num_Sesion}')
                
                
                
    elif lang == "en": #Versión inglés
        st.title('Tap the mole 🐭')
        st.header("Let's see your reaction speed 👆 and some interesting facts about your performance!")

        sesiones = ['s1', 's2', 's3', 's4']
        dividers = ['blue', 'green', 'orange', 'red']

        usuario_en = st.query_params.feedback
        usuario = decrypt(usuario_en)

        for sesion in sesiones:

            num_Sesion=int(sesion[-1])
            st.subheader(f'Session number {num_Sesion}', divider=dividers[num_Sesion-1])

            #Sacamos los datos de la BBDD
            zip_file=f'{usuario}/{sesion}.zip'
            target_file=f'{sesion}/g/tap/{sesion}_g_touch.csv'
            try:
                df=load_file_from_zip(zip_file, target_file)
            except:
                df = pd.DataFrame()  # DataFrame vacío en caso de error

            # Comprobamos que hay datos para representar
            if not df.empty:
                velocidad_usuario = calcular_tiempos_reaccion(df)

                graficar_distribucion_probabilidad(df, lang)
                
                if velocidad_usuario.mean() < 300.0:
                    TextoVelocidad = f'<b>Impressive!</b> Your reaction speed in this session ({velocidad_usuario.round()}ms) is well above the average of BehavePassUAM users.'
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                elif 300.0 <= velocidad_usuario.mean() <= 600.0:
                    TextoVelocidad = f'Your reaction speed in this session ({velocidad_usuario.round()}ms) is within the average range (300ms - 600ms) of BehavePassUAM users.'
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                elif velocidad_usuario.mean() > 600.0:
                    TextoVelocidad = f'Your reaction speed in this session ({velocidad_usuario.round()}ms) is below the average of BehavePassUAM users.'
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
            else:
                st.warning(f'Please return after completing session {num_Sesion}.')

                        
def render_tap_tab_json(json_usuario, lang):
    if lang == "es": #Versión español
        st.title('Rendimiento en el juego de los topos 🐭')
        st.header("¡Veamos tu velocidad de reacción 👆 y algunos datos interesantes sobre tu rendimiento!")

        sesiones = ['s1', 's2', 's3', 's4']
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
                    TextoVelocidad=f'<b>¡Impresionante!</b> Tu velocidad de reacción en esta sesión ({velocidad_usuario.round()}ms) está muy por encima de la media de los usuarios de BehavePassUAM.'
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                    #st.write(f'¡Impresionante! Tu velocidad de reacción ({velocidad_usuario.mean().round()}ms) está por encima de la media de los usuarios de BehavePassUAM.')
                elif velocidad_usuario > 300.0 and 600.0 > velocidad_usuario:
                    TextoVelocidad=f'Tu velocidad de reacción en esta sesión ({velocidad_usuario.round()}ms) está en el rango promedio (300ms - 600ms) de los usuarios de BehavePassUAM.'
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                elif 600.0 < velocidad_usuario:
                    TextoVelocidad=f'Tu velocidad de reacción en esta sesión ({velocidad_usuario..round()}ms) está por debajo de la media de los usuarios de BehavePassUAM. '
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                    #st.write(f'Vaya... Tu velocidad de reacción ({velocidad_usuario.mean().round()}ms) está por debajo de la media de los usuarios de BehavePassUAM. ')

                
                #st.dataframe(df)
            else:
                st.warning(f'Vuelve cuando hayas completado la sesión {num_Sesion}')
                
                
                
    elif lang == "en": #Versión inglés
        st.title('Tap the mole 🐭')
        st.header("Let's see your reaction speed 👆 and some interesting facts about your performance!")

        sesiones = ['s1', 's2', 's3', 's4']
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
                    TextoVelocidad = f'<b>Impressive!</b> Your reaction speed in this session ({velocidad_usuario.mean().round()}ms) is well above the average of BehavePassUAM users.'
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                elif 300.0 <= velocidad_usuario <= 600.0:
                    TextoVelocidad = f'Your reaction speed in this session ({velocidad_usuario.mean().round()}ms) is within the average range (300ms - 600ms) of BehavePassUAM users.'
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
                elif velocidad_usuario > 600.0:
                    TextoVelocidad = f'Your reaction speed in this session ({velocidad_usuario.mean().round()}ms) is below the average of BehavePassUAM users.'
                    st.markdown(f'<p style="font-size:18px;">{TextoVelocidad}</p>', unsafe_allow_html=True)
            else:
                st.warning(f'Please return after completing session {num_Sesion}.')