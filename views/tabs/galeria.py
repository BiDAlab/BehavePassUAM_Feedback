import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from utils import  *

def memoria_visual(data_trazo, data_respuesta, lang):
    """
        Esta función calcula los movimientos que realiza el usuario a la hora de realizar la 
        tarea de la galería. A partir de estos datos da un feedback al usuario para que sepa que tiene que mejorar.

        Parámetros:
        - data_trazo: Datos de movimiento cuando pulsa, levanta el dedo o lo arrastra.
        - data_respuesta: Respuestas que ha hecho el usuario a las preguntas de las imagenes. 
    """
    # Variables
    pulsar, atras, alante,subir, bajar = 0, 0, 0, 0, 0
    # Índices de eventos
    down_indices = data_trazo[data_trazo.iloc[:, 8] == 0].index
    up_indices = data_trazo[data_trazo.iloc[:, 8] == 1].index

    # Verificación de que hay datos
    if len(down_indices) > 0 and len(up_indices) > 0:
        for i in range(len(down_indices)):
            down_index = down_indices[i]
            up_index = up_indices[i]

            x_ini, y_ini = data_trazo.iloc[down_index, 2], -data_trazo.iloc[down_index, 4]
            x_fin, y_fin = data_trazo.iloc[up_index, 2], -data_trazo.iloc[up_index, 4]

            x_despl = x_fin - x_ini
            y_despl = y_fin - y_ini

            # desplazamiento derecha/izquierda
            if abs(x_despl) > abs(y_despl):
                # Pulsar
                if x_despl == 0:
                    pulsar = pulsar + 1
                # Ir hacia atrás en las fotos
                elif x_despl > 0:
                    atras = atras + 1
                # Ir hacia adelante
                else:
                    alante = alante + 1
            # desplazamientos arriba/abajo
            elif abs(x_despl) < abs(y_despl):
                # Pulsar
                if y_despl == 0:
                    pulsar = pulsar + 1
                # Ir hacia arriba
                elif y_despl < 0:
                    subir = subir + 1
                # Ir hacia abajo
                else:
                    bajar = bajar + 1
            else: 
                pulsar = pulsar + 1
    # Resultados respuestas
    n_correctas = round(data_respuesta[data_respuesta.iloc[:, 12] == 1].shape[0] / 2)
    n_incorrectas = round(data_respuesta[data_respuesta.iloc[:, 12] == 0].shape[0] / 2)
    
    mostrarMet=0
    if mostrarMet==1:    

        st.write(f'Veces hacia atras: {atras}')
        st.write(f'Veces hacia adelante: {alante}')
        st.write(f'Veces hacia abajo: {bajar}')
        st.write(f'Veces hacia arriba: {subir}')
        st.write(f'Veces pulsada: {pulsar}')
        st.write(f'Respuestas correctas {n_correctas}')
        st.write(f'Respuestas incorrectas {n_incorrectas}')

    if lang == "es":
 
        if (atras == 0) & (n_correctas == 4) & (n_incorrectas == 0):
            st.success(f" 🏆 **¡Increíble!**, ¡Tienes una **memoria visual perfecta**! No has tenido **ningún fallo** y **no has tenido que volver hacia atrás** para volver a ver las imágenes.")
        elif (atras == 0) & (n_correctas == 4) & (n_incorrectas > 0):
            st.info(f" 😀 **¡Buena!** Lo has hecho bien. Te has **equivocado alguna vez**. Has tenido **{n_incorrectas} {'fallo' if n_incorrectas == 1 else 'fallos'}**. El número de veces que has **vuleto hacia atrás a ver las imagenes es {atras}.**")
        else:
            st.info(f" ⚠️ **Mejorable** ¡Se que puedes dar más de ti! **Presta más atención a las fotos** la proxima vez. Has tenido **{n_incorrectas} {'fallo' if n_incorrectas == 1 else 'fallos'}** y hemos detectado que has **vuelto {atras} {'vez' if atras == 1 else 'veces'} hacia atrás.**")
    elif lang == "en":
        if (atras == 0) & (n_correctas == 4) & (n_incorrectas == 0):
            st.success(f"🏆 **Amazing!** You have **perfect visual memory**! You didn’t make **any mistakes** and you **didn't need to go back** to see the images again.")
        elif (atras == 0) & (n_correctas == 4) & (n_incorrectas > 0):
            st.info(f"😀 **Good job!** Well done. You made **a few mistakes**. You had **{n_incorrectas} {'incorrect answer' if n_incorrectas == 1 else 'incorrect answers'}**. The number of times you **went back to see the images again is {atras}.**")
        else:
            st.info(f"⚠️ **Room for improvement** You could do better! **Pay more attention to the photos** next time. You had **{n_incorrectas} {'incorrect answer' if n_incorrectas == 1 else 'incorrect answers'}** and we detected that you **went back {atras} {'time' if atras == 1 else 'times'}.**")


def fallos_galeria(data_respuesta,lang): 
    """
        Esta función te da los resultados de las preguntas de las fotos a partir del fichero con 
        las respuestas.

        Parámetros:
        - data_respuesta: Respuestas que ha hecho el usuario a las preguntas de las imagenes. 
    """
    # Resultados respuestas
    n_correctas = round(data_respuesta[data_respuesta.iloc[:, 12] == 1].shape[0] / 2)
    n_incorrectas = round(data_respuesta[data_respuesta.iloc[:, 12] == 0].shape[0] / 2)

    TextoFirma=f'El número de aciertos y fallos contestando las preguntas de las imagenes es:'
    #st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)

    if lang == "es":
        st.markdown(f"""
        ### Resultados de las preguntas:
        - <span style="color:green; font-weight:bold;">Aciertos: {n_correctas}</span>
        - <span style="color:red; font-weight:bold;">Fallos: {n_incorrectas}</span>
        """, unsafe_allow_html=True)
    elif lang == "en":
        st.markdown(f"""
        ### Question Results:
        - <span style="color:green; font-weight:bold;">Correct Answers: {n_correctas}</span>
        - <span style="color:red; font-weight:bold;">Incorrect Answers: {n_incorrectas}</span>
        """, unsafe_allow_html=True)



def galeria(data_trazo):
    """
    Esta función representa de una manera gráfica los movimiento que a realizado el usuario 
    al responder las preguntas de la galerías.

    Parámetros:
    - data_trazo: Datos de movimiento cuando pulsa, levanta el dedo o lo arrastra
    """
    # Crear una figura 
    fig=plt.figure(figsize=(10,7.5))
    fig.suptitle(f' Análisis de Trazos por Sesión (Galería)', fontsize=16)

    # Índices de eventos
    down_indices = data_trazo[data_trazo.iloc[:, 8] == 0].index
    up_indices = data_trazo[data_trazo.iloc[:, 8] == 1].index

    # Graficar los trazos, pulsaciones y levantamientos
    for i, up_index in enumerate(up_indices):
        if i < len(down_indices):
            down_index = down_indices[i]
            x_down, y_down = data_trazo.iloc[down_index, 2], -data_trazo.iloc[down_index, 4]
            x_up, y_up = data_trazo.iloc[up_index, 2], -data_trazo.iloc[up_index, 4]
            trazo = range(down_index, up_index + 1)
            x_move = data_trazo.loc[trazo, 2]
            y_move = -data_trazo.loc[trazo, 4]

            plt.plot(x_down, y_down, 'go', markersize=8)
            plt.plot(x_up, y_up, 'ro', markersize=8)
            plt.plot(x_move, y_move, 'b-', linewidth=2)

    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.legend(['Pulsación', 'Levantamiento', 'Movimiento'])
    plt.grid()

    # Ajustar espacio entre subplots
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Representa la imagen en la web
    st.pyplot(fig)

# def render_galeria_tab():
#     usuario_en = st.query_params.feedback
#     usuario = decrypt(usuario_en)
#     usuario_file=f'{usuario}/config.json'
#     edadReal, lang =edad_real(usuario_file)
#     #lang = "en" 
    
#     ## PARTE EN ESPAÑOL ##
#     if lang == "es":
#         st.title('🖼️ Memoria Visual')
#         TextoInicio = """<p style="font-size:20px;">La <strong>memoria visual</strong> es la capacidad que tenemos de <strong>recordar detalles de las imágenes</strong> que observamos. Estos detalles pueden ser colores, formas o incluso la ubicación de los objetos.</p>
#         <p style="font-size:20px;">Esta habilidad es fundamental en muchas actividades diarias, como puede ser a la hora de reconocer rostros de la gente o tomar decisiones rápidas basadas en lo que recordemos.</p>
#         <p style="font-size:20px;">Por estas razones, al finalizar cada sesión haremos un <strong>análisis que evaluará</strong> cómo de bien puedes <strong>retener y recordar detalles visuales</strong> después de observar imágenes.</p>
#         <p style="font-size:20px;">Una vez terminada la sesión 4, te haremos un análisis más detallado de tu memoria visual.</p>"""
#         st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)


#         sesiones = ['s1', 's2', 's3', 's4']
#         dividers = ['blue', 'green', 'orange', 'red']
#         usuario_en = st.query_params.feedback
#         usuario = decrypt(usuario_en)


#         # Comprobamos si la sesión 4 está disponible
#         st.header('Análisis de tu memoria visual')
#         sesion_4 = 's4'  # Nombre esperado para la sesión 4
#         zip_file_4 = f'{usuario}/{sesion_4}.zip'
#         target_file_4 = f'{sesion_4}/g/gallery/{sesion_4}_g_touch.csv'
#         df_sesion_4 = load_file_from_zip(zip_file_4, target_file_4)
#         target_file_answ_4 = f'{sesion_4}/g/gallery/{sesion_4}_g_touch_gallery_answers_events.csv'
#         df_answ_sesion_4 = load_file_from_zip(zip_file_4, target_file_answ_4)

#         # Si la sesión 4 tiene datos, mostramos el contenido inicial
#         if not df_sesion_4.empty:
#             TextoFirma = (
#                 #f'En la sesión 4, hemos analizado tanto el número de aciertos como las veces qque has tenido que volver atrás en las imágenes para fijarte en los detalles. '
#                 f'Basandonos en el <strong>número de respuestas incorrectas</strong> como las veces que ha tenido que <strong>volver atrás<strong> a las imágenes para fijarse en los detalles, hemos considerado que tu <strong>memoria visual</strong> es...'
#             )
#             st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)
#             # Aquí puedes agregar más lógica relacionada con la sesión 4
#             memoria_visual(df_sesion_4, df_answ_sesion_4,lang)
#         else: 
#             st.warning(f'¿Quieres ver un **análisis más completo** de tu memoria visual? ¡**Vuelve cuando acabes la sesión 4**!')

#         # Ahora iteramos las demás sesiones
#         for sesion in sesiones:
#             num_Sesion = int(sesion[-1])
#             st.subheader(f'Datos de la sesión {num_Sesion}', divider=dividers[num_Sesion - 1])

#             # Sacamos los datos de la BBDD
#             zip_file = f'{usuario}/{sesion}.zip'
#             target_file_escr = f'{sesion}/g/gallery/{sesion}_g_touch_gallery_answers_events.csv'
#             df_answ = load_file_from_zip(zip_file, target_file_escr)

#             if not df_answ.empty:
#                 fallos_galeria(df_answ,lang)

#                 if num_Sesion == 4:
#                     # Esta parte ya se cubrió al inicio
#                     continue  # Saltamos para evitar duplicados
#             else:
#                 st.warning(f'Vuelve cuando hayas completado la sesión {num_Sesion}')
                

#     ## PARTE EN INGLÉS ##            
#     elif lang == "en":
#         st.title('🖼️ Visual Memory')
#         TextoInicio = """<p style="font-size:20px;">Visual memory is the ability to <strong>recall details of images</strong> that we observe. These details can include colors, shapes, or even the location of objects.</p>
#         <p style="font-size:20px;">This skill is essential in many daily activities, such as recognizing people's faces or making quick decisions based on what we remember.</p>
#         <p style="font-size:20px;">For these reasons, at the end of each session, we conduct an <strong>analysis to evaluate</strong> how well you can <strong>retain and recall visual details</strong> after observing images.</p>
#         <p style="font-size:20px;">Once session 4 is completed, we will make a more detailed analysis of your visual memory.</p>"""
#         st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

#         sesiones = ['s1', 's2', 's3', 's4']
#         dividers = ['blue', 'green', 'orange', 'red']

#         # User decryption
#         usuario_en = st.query_params.feedback
#         usuario = decrypt(usuario_en)

#         # Check if session 4 is available
#         st.header('Visual memory analysis')
#         sesion_4 = 's4'  # Expected name for session 4
#         zip_file_4 = f'{usuario}/{sesion_4}.zip'
#         target_file_4 = f'{sesion_4}/g/gallery/{sesion_4}_g_touch.csv'
#         df_sesion_4 = load_file_from_zip(zip_file_4, target_file_4)
#         target_file_answ_4 = f'{sesion_4}/g/gallery/{sesion_4}_g_touch_gallery_answers_events.csv'
#         df_answ_sesion_4 = load_file_from_zip(zip_file_4, target_file_answ_4)

#         # If session 4 has data, display the initial content
#         if not df_sesion_4.empty:
#             TextoFirma = (
#                 f'Based on the <strong>number of incorrect answers</strong> as well as the number of times you <strong>revisited</strong> the images to look at the details, we’ve determined that your <strong>visual memory</strong> is...'
#             )
#             st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)
#             # Add more logic related to session 4 here
#             memoria_visual(df_sesion_4, df_answ_sesion_4,lang)
#         else: 
#             st.warning(
#                 f'Do you want to see a **more complete analysis** of your visual memory? **Come back after completing session 4**!'
#             )

#         # Now iterate through the other sessions
#         for sesion in sesiones:
#             num_Sesion = int(sesion[-1])
#             st.subheader(f'Session {num_Sesion}', divider=dividers[num_Sesion - 1])

#             # Retrieve data from the database
#             zip_file = f'{usuario}/{sesion}.zip'
#             target_file_escr = f'{sesion}/g/gallery/{sesion}_g_touch_gallery_answers_events.csv'
#             df_answ = load_file_from_zip(zip_file, target_file_escr)

#             if not df_answ.empty:
#                 fallos_galeria(df_answ,lang)

#                 if num_Sesion == 4:
#                     # This part was already covered above
#                     continue  # Skip to avoid duplication
#             else:
#                 st.warning(f'Come back after completing session {num_Sesion}')


def render_galeria_tab_json(json_usuario, lang, sessionsPerf, lastSessionPer):
    ## EN ESPAÑOL ##
    if lang == "es":
        st.title('🖼️ Memoria Visual')
        TextoInicio = """<p style="font-size:20px;">La <strong>memoria visual</strong> es la capacidad que tenemos de <strong>recordar detalles de las imágenes</strong> que observamos. Estos detalles pueden ser colores, formas o incluso la ubicación de los objetos.</p>
        <p style="font-size:20px;">Esta habilidad es fundamental en muchas actividades diarias, como puede ser a la hora de reconocer rostros de la gente o tomar decisiones rápidas basadas en lo que recordemos.</p>
        <p style="font-size:20px;">Por estas razones, al finalizar cada sesión haremos un <strong>análisis que evaluará</strong> cómo de bien puedes <strong>retener y recordar detalles visuales</strong> después de observar imágenes.</p>
        <p style="font-size:20px;">Una vez terminada la sesión 4, te haremos un análisis más detallado de tu memoria visual.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

        dividers = ['blue', 'green', 'orange', 'red']

        # Comprobamos si la sesión 4 está disponible
        st.header('Análisis de tu memoria visual')

        # Si la sesión 4 tiene datos, mostramos el contenido inicial
        if lastSessionPer == "s4":
            s4_correct = int(json_usuario.get("visual_memory", "unknown").get("questions", "unknown").get("s4_s4_correct", "Unknown"))
            s4_incorrect = int(json_usuario.get("visual_memory", "unknown").get("questions", "unknown").get("s4_s4_incorrect", "Unknown"))
            atras = int(json_usuario.get("visual_memory", "unknown").get("atras", "unknown").get("atras_s4", "Unknown"))
            TextoFirma = (
                f'Basandonos en el <strong>número de respuestas incorrectas</strong> como las veces que ha tenido que <strong>volver atrás<strong> a las imágenes para fijarse en los detalles, hemos considerado que tu <strong>memoria visual</strong> es...'
            )
            st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)
            if (atras == 0) & (s4_correct == 4) & (s4_incorrect == 0):
                st.success(f" 🏆 **¡Increíble!**, ¡Tienes una **memoria visual perfecta**! No has tenido **ningún fallo** y **no has tenido que volver hacia atrás** para volver a ver las imágenes.")
            elif (atras == 0) & (s4_correct == 4) & (s4_incorrect > 0):
                st.info(f" 😀 **¡Buena!** Lo has hecho bien. Te has **equivocado alguna vez**. Has tenido **{s4_incorrect} {'fallo' if s4_incorrect == 1 else 'fallos'}**. El número de veces que has **vuleto hacia atrás a ver las imagenes es {atras}.**")
            else:
                st.info(f" ⚠️ **Mejorable** ¡Se que puedes dar más de ti! **Presta más atención a las fotos** la proxima vez. Has tenido **{s4_incorrect} {'fallo' if s4_incorrect == 1 else 'fallos'}** y hemos detectado que has **vuelto {atras} {'vez' if atras == 1 else 'veces'} hacia atrás.**")
  
        else: 
            st.warning(f'¿Quieres ver un **análisis más completo** de tu memoria visual? ¡**Vuelve cuando acabes la sesión 4**!')

        # Ahora iteramos las demás sesiones
        for sesion in sessionsPerf:
            num_Sesion = int(sesion[-1])
            st.subheader(f'Datos de la sesión {num_Sesion}', divider=dividers[num_Sesion - 1])
            n_correct = int(json_usuario.get("visual_memory", "unknown").get("questions", "unknown").get(f"s{num_Sesion}_s{num_Sesion}_correct", "Unknown"))
            n_incorrect = int(json_usuario.get("visual_memory", "unknown").get("questions", "unknown").get(f"s{num_Sesion}_s{num_Sesion}_incorrect", "Unknown"))

            if n_correct != -1:
                st.markdown(f"""
                    ### Resultados de las preguntas:
                    - <span style="color:green; font-weight:bold;">Aciertos: {n_correct}</span>
                    - <span style="color:red; font-weight:bold;">Fallos: {n_incorrect}</span>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f'Vuelve cuando hayas completado la sesión {num_Sesion}')
                

    ## PARTE EN INGLÉS ##       
    elif lang == "en":
        st.title('🖼️ Visual Memory')
        TextoInicio = """<p style="font-size:20px;">Visual memory is the ability to <strong>recall details of images</strong> that we observe. These details can include colors, shapes, or even the location of objects.</p>
        <p style="font-size:20px;">This skill is essential in many daily activities, such as recognizing people's faces or making quick decisions based on what we remember.</p>
        <p style="font-size:20px;">For these reasons, at the end of each session, we conduct an <strong>analysis to evaluate</strong> how well you can <strong>retain and recall visual details</strong> after observing images.</p>
        <p style="font-size:20px;">Once session 4 is completed, we will make a more detailed analysis of your visual memory.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

        dividers = ['blue', 'green', 'orange', 'red']

        # Comprobamos si la sesión 4 está disponible
        st.header('Visual memory analysis')

        # Si la sesión 4 tiene datos, mostramos el contenido inicial
        if lastSessionPer == "s4":
            s4_correct = int(json_usuario.get("visual_memory", "unknown").get("questions", "unknown").get("s4_s4_correct", "Unknown"))
            s4_incorrect = int(json_usuario.get("visual_memory", "unknown").get("questions", "unknown").get("s4_s4_incorrect", "Unknown"))
            atras = int(json_usuario.get("visual_memory", "unknown").get("atras", "unknown").get("atras_s4", "Unknown"))
            TextoFirma = (
                f'Based on the <strong>number of incorrect answers</strong> as well as the number of times you <strong>revisited</strong> the images to look at the details, we’ve determined that your <strong>visual memory</strong> is...'
            )
            st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)
            if (atras == 0) & (s4_correct == 4) & (s4_incorrect == 0):
                st.success(f"🏆 **Amazing!** You have **perfect visual memory**! You didn’t make **any mistakes** and you **didn't need to go back** to see the images again.")
            elif (atras == 0) & (s4_correct == 4) & (s4_incorrect > 0):
                st.info(f"😀 **Good job!** Well done. You made **a few mistakes**. You had **{s4_incorrect} {'incorrect answer' if s4_incorrect == 1 else 'incorrect answers'}**. The number of times you **went back to see the images again is {atras}.**")
            else:
                st.info(f"⚠️ **Room for improvement** You could do better! **Pay more attention to the photos** next time. You had **{s4_incorrect} {'incorrect answer' if s4_incorrect == 1 else 'incorrect answers'}** and we detected that you **went back {atras} {'time' if atras == 1 else 'times'}.**")


        else: 
            st.warning(
                f'Do you want to see a **more complete analysis** of your visual memory? **Come back after completing session 4**!'
            )

        # Ahora iteramos las demás sesiones
        for sesion in sessionsPerf:
            num_Sesion = int(sesion[-1])
            st.subheader(f'Session {num_Sesion}', divider=dividers[num_Sesion - 1])
            n_correct = int(json_usuario.get("visual_memory", "unknown").get("questions", "unknown").get(f"s{num_Sesion}_s{num_Sesion}_correct", "Unknown"))
            n_incorrect = int(json_usuario.get("visual_memory", "unknown").get("questions", "unknown").get(f"s{num_Sesion}_s{num_Sesion}_incorrect", "Unknown"))

            if n_correct != -1:
                st.markdown(f"""
                    ### Results:
                    - <span style="color:green; font-weight:bold;">Correct: {n_correct}</span>
                    - <span style="color:red; font-weight:bold;">Incorrect: {n_incorrect}</span>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f'Come back after completing session {num_Sesion}')
