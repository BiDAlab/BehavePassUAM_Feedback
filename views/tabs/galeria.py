import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from utils import  *



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
