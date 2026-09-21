import streamlit as st

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from random import *
import requests

from utils import *


def render_read_tab_json(json_usuario, lang, sessionsPerf):
    if "s1" in sessionsPerf:

        age_pred = int(json_usuario.get("age_predict", "unknown").get("aprox_age", "Unknown"))
        
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
                st.warning(f'Come back when you have completed session 1')
    else:
        if lang == "es":
            st.warning(f'Vuelve cuando hayas completado la sesión 1')
        else:
            st.warning(f'Come back when you have completed session 1')
