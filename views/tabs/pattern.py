import streamlit as st

import pandas as pd
import os
import matplotlib.pyplot as plt

from utils import *

def render_pattern_tab_json(json_usuario, lang, sessionsPerf):
    pattern = int(json_usuario.get("pattern", "unknown").get("match_pattern", "Unknown")) #-1 no existe, 0 no match, 1 match (sí es de los comunes)

    if lang == "es":
        st.title('Patrón de desbloqueo 🔓')
        st.header('¿Sabías que...?')
        TextoInicio = """<p style="font-size:20px;"> Los patrones de desbloqueo son uno de los métodos de seguridad más populares en dispositivos móviles.</p>
        <p style="font-size:20px;">La mayoría de los patrones de desbloqueo tienden a seguir formas comunes o secuencias repetitivas, lo que los hace fáciles de recordar, pero también más predecibles y, por lo tanto, menos seguros si no se eligen cuidadosamente.</p>
        <p style="font-size:20px;">En la imagen a continuación, te mostramos algunos de los más comunes.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)
        st.image('static/images/patrones_comunes.jpg', use_column_width=True, clamp=True)

        if pattern == -1:
            if "s3" in sessionsPerf:
                st.warning(f'¡Lo sentimos! En esta ocasión no vamos a poder analizar tu patrón de desbloqueo. Echa un ojo al resto de tareas, tienes mucha información interesante disponible.')
            else:
                st.warning(f'Los resultados del **patrón** se mostrarán cuando hayas acabado la **sesión 3**. Vuelve cuando la hayas acabado.')

        elif pattern == 1:
            TextoInicio2 = """<p style="font-size:20px;"> ¿Te atreves a analizar el tuyo?</p>"""
            st.markdown(f'<p style="font-size:20px;">{TextoInicio2}</p>', unsafe_allow_html=True)   
            TextoPattern=f'<b>¡Vaya!</b> Parece que tu patrón es uno de los más comunes 🔓. Deberías tener cuidado porque puede ser fácil de adivinar'
            st.markdown(f'<p style="font-size:18px;">{TextoPattern}</p>', unsafe_allow_html=True)
        elif pattern == 0:
            TextoInicio2 = """<p style="font-size:20px;"> ¿Te atreves a analizar el tuyo?</p>"""
            st.markdown(f'<p style="font-size:20px;">{TextoInicio2}</p>', unsafe_allow_html=True)   
            TextoPattern=f'<b>¡Genial!</b> Tu patrón de desbloqueo no es de los más comunes, parece muy seguro 🔒. ¡Se nota que te tomas en serio la ciberseguridad, sigue así!'
            st.markdown(f'<p style="font-size:18px;">{TextoPattern}</p>', unsafe_allow_html=True)

    elif lang == "en":
        st.title('Unlock Pattern 🔓')
        st.header('Did you know...?')
        TextoInicio = """<p style="font-size:20px;">Unlock patterns are one of the most popular security methods on mobile devices.</p>
        <p style="font-size:20px;">Most unlock patterns tend to follow common shapes or repetitive sequences, making them easy to remember but also more predictable, and therefore less secure if not carefully chosen.</p>
        <p style="font-size:20px;">In the image below, we show you some of the most common patterns.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)
        st.image('static/images/patrones_comunes.jpg', use_column_width=True, clamp=True)

        if pattern == -1:
            if "s3" in sessionsPerf:
                st.warning(f'Sorry! This time we won’t be able to analyze your unlock pattern. Check out the rest of the tasks, there’s plenty of interesting information available.')
            else:
                st.warning(f'Pattern results will be shown once you complete session 3. Come back when you have finished.')

        elif pattern == 1:
            TextoInicio2 = """<p style="font-size:20px;"> Dare to analyze yours?</p>"""
            st.markdown(f'<p style="font-size:20px;">{TextoInicio2}</p>', unsafe_allow_html=True)   
            TextoPattern = f'<b>Oops!</b> It seems that your unlock pattern is one of the most common 🔓. You should be careful because it might be easy to guess.'
            st.markdown(f'<p style="font-size:18px;">{TextoPattern}</p>', unsafe_allow_html=True)
        elif pattern == 0:
            TextoInicio2 = """<p style="font-size:20px;"> Dare to analyze yours?</p>"""
            st.markdown(f'<p style="font-size:20px;">{TextoInicio2}</p>', unsafe_allow_html=True)   
            TextoPattern = f'<b>Great!</b> Your unlock pattern is not one of the most common, it seems very secure 🔒. It shows that you take cybersecurity seriously, keep it up!'
            st.markdown(f'<p style="font-size:18px;">{TextoPattern}</p>', unsafe_allow_html=True)

            
            
