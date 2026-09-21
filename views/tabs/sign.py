import streamlit as st

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import StandardScaler
from dtaidistance import dtw

from utils import *

        
def render_sign_tab_json(json_usuario, lang):
    average_dtw_distance = json_usuario.get("sign", {}).get("consistency", {}).get("avg_dtw_distance", None) #Medida consistencia

    duracion = json_usuario.get("sign", {}).get("complexity", {}).get("duracion", None) #Medida complejidad - duracion
    num_arriba = json_usuario.get("sign", {}).get("complexity", {}).get("num_arriba", None) #Medida complejidad - num_arriba
    total_distance = json_usuario.get("sign", {}).get("complexity", {}).get("total_distance", None) #Medida complejidad - total_distance

    if lang == "es": #Versión Español   
        st.title('✒️ Firma')
        TextoInicio = """<p style="font-size:20px;">En este apartado analizaremos tu firma de dos maneras diferentes a través de la <strong>complejidad</strong> y de la <strong>consistencia</strong>. Estos dos factores son muy importantes a la hora de evaluar su seguridad y autenticidad.</p>
                                    <p style="font-size:20px;">Para que una firma sea segura, debe lograr un equilibrio entre <strong>complejidad</strong> y <strong>consistencia</strong>, siendo compleja de imitar, pero consistente para quien la produce.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

        ### CONSISTENCIA ##
        st.header(f'Consistencia', divider=False)
        TextoConsistencia="""<p style="font-size:18px;"><strong>Análisis de Consistencia:</strong> A partir del análisis de la consistencia, examinaremos la capacidad de reproducir la firma de manera similar en diferentes momentos. La consistencia es clave para la autenticidad, ya que, para que una firma sea segura, debe mantener un estilo y patrones reconocibles.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoConsistencia}</p>', unsafe_allow_html=True)
        
        if average_dtw_distance >= -1:        
            TextoFirma=f'Analizando el parecido de <strong>dos de tus firmas</strong> hemos conseguido sacar los siguientes resultados sobre la <strong>consistencia</strong> de tu firma.'
            st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)

            # Comentarios de consistencia
            if average_dtw_distance < 3:
                st.success("**¡Excelente!** 🎉 Tus firmas son **muy consistentes**, lo que muestra una gran precisión en tus trazos. ¡Sigue así!")
            elif average_dtw_distance < 9:
                st.info("**¡Buen trabajo!** 👍 Tus firmas tienen **pequeñas variaciones**, pero en general muestran una **buena consistencia**. Con un poco de práctica, podrían ser aún más uniformes.")
            else:
                st.warning("Interesante... 🤔 Tus firmas muestran **diferencias notables** entre sesiones. Esto puede indicar cambios en tu trazo o estilo. ¡No te preocupes! Practicar puede ayudarte a lograr una firma más constante.")
        else:
            st.warning(f'La **consistencia** se mostrara cuando hayas acabado la **sesión 2**. Vuelve cuando la hayas acabado.') 
    

        ### COMPLEJIDAD ###
        st.header(f'Complejidad', divider=False)
        TextoComplejidad = """<p style="font-size:18px;"><strong>Análisis de Complejidad:</strong> Con el análisis de la complejidad podemos observar qué elementos hacen que tu firma sea difícil de imitar. Esto incluye la velocidad a la que la realizas, el número de trazos que utilizas, entre otros detalles únicos que la caracterizan. Cuanto más compleja sea tu firma, más difícil será para otra persona replicarla. La complejidad ayuda a que la firma sea un elemento único y distintivo.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoComplejidad}</p>', unsafe_allow_html=True)

        # Comprobamos que hay datos para representar
        if duracion!= -1 and num_arriba != -1 and total_distance != -1:
            TextoFirma=f'A partir de <strong>de las firmas</strong> que realizaste en la <strong>sesión 4</strong> hemos considerado que...'
            st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)


            # Complejidad alata (todo por encima del percentil 75)
            if (duracion >= 4.1617) & (num_arriba >= 5) & (total_distance >= 86.4499):
                st.success("🏆 Tu firma es **muy detallada y compleja**.")
            # Complejidad medio alta (alguno de los parámetros está por encima del percentil 75)
            elif  (duracion >= 4.1617) | (num_arriba >= 5) | (total_distance >= 86.4499):
                st.success("🤩 Tu firma es **bastante detallada y compleja**.")
            # Complejidad medio baja (todo está por encima del percentil 25, pero nada por encima del percentil 75)
            elif (duracion >= 1.4849) & (num_arriba >= 1) & (total_distance >= 41.15161):
                st.info("😀 Tu firma tiene un **balance entre simplicidad y detalle**.")
            # Complejidad baja (todo está por debajo del percentil 25)
            else:
                st.warning("⚠️ Tu firma es **simple**, considera si es suficientemente distintiva.")

        elif duracion== -2 and num_arriba == -2 and total_distance == -2:
                st.warning(f'Vaya! Parece que esta vez no vamos a poder mostrarte un análisis de **complejidad**')

        else:
            st.warning(f'La **complejidad** se mostrara cuando hayas acabado la **sesión 4**. Vuelve cuando la hayas acabado')
    
    elif lang == "en": #Versión inglés   
        st.title('✒️ Signature')
        TextoInicio = """<p style="font-size:20px;">In this section, we will analyze your signature in two different ways: through its <strong>complexity</strong> and <strong>consistency</strong>. These two factors are crucial when evaluating its security and authenticity.</p>
                        <p style="font-size:20px;">For a signature to be secure, it must strike a balance between <strong>complexity</strong> and <strong>consistency</strong>, being difficult to imitate yet consistent for the signer.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

        ### CONSISTENCIA ##
        st.header(f'Consistency', divider=False)
        TextoConsistencia = """<p style="font-size:18px;"><strong>Consistency Analysis:</strong> Through the consistency analysis, we examine your ability to reproduce your signature similarly across different sessions. Consistency is key for authenticity, as a secure signature must maintain recognizable styles and patterns.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoConsistencia}</p>', unsafe_allow_html=True)
        
        if average_dtw_distance >= -1:        
            TextoFirma = f'Analyzing the similarity of <strong>two of your signatures</strong>, we have derived the following results about the <strong>consistency</strong> of your signature.'
            st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)

            # Comentarios de consistencia
            if average_dtw_distance < 3:
                st.success("**Excellent!** 🎉 Your signatures are **very consistent**, showing great precision in your strokes. Keep it up!")
            elif average_dtw_distance < 9:
                st.info("**Good job!** 👍 Your signatures have **small variations**, but overall they show **good consistency**. With a little practice, they could become even more uniform.")
            else:
                st.warning("Interesting... 🤔 Your signatures show **notable differences** between sessions. This could indicate changes in your stroke or style. Don’t worry! Practicing can help you achieve a more consistent signature.")
        else:
            st.warning(f'**Consistency** will be displayed once you complete **session 2**. Please return after finishing it.') 

    

        ### COMPLEJIDAD ###
        st.header(f'Complexity', divider=False)
        TextoComplejidad = """<p style="font-size:18px;"><strong>Complexity Analysis:</strong> Through complexity analysis, we explore what makes your signature difficult to replicate. This includes factors such as the speed of execution, the number of strokes used, and other unique traits. The more complex your signature is, the harder it is for someone else to replicate. Complexity ensures that your signature is unique and distinctive.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoComplejidad}</p>', unsafe_allow_html=True)

        # Comprobamos que hay datos para representar
        if duracion!= -1 and num_arriba != -1 and total_distance != -1:
            TextoFirma = f'Based on the <strong>signatures</strong> you provided during <strong>session 4</strong>, we have determined that...'
            st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)


            # Complejidad alata (todo por encima del percentil 75)
            # High Complexity (all parameters above the 75th percentile)
            if (duracion >= 4.1617) & (num_arriba >= 5) & (total_distance >= 86.4499):
                st.success("🏆 Your signature is **very detailed and complex**.")
            # Medium-High Complexity (at least one parameter above the 75th percentile)
            elif (duracion >= 4.1617) | (num_arriba >= 5) | (total_distance >= 86.4499):
                st.success("🤩 Your signature is **quite detailed and complex**.")
            # Medium-Low Complexity (all parameters above the 25th percentile but none above the 75th)
            elif (duracion >= 1.4849) & (num_arriba >= 1) & (total_distance >= 41.15161):
                st.info("😀 Your signature strikes a **balance between simplicity and detail**.")
            # Low Complexity (all parameters below the 25th percentile)
            else:
                st.warning("⚠️ Your signature is **simple**. Consider whether it’s distinctive enough.")

        elif duracion== -2 and num_arriba == -2 and total_distance == -2:
                st.warning(f'Oh no! It seems that this time we won't be able to show you a **complexity** analysis')

        else:
            st.warning(f'**Complexity** will be displayed once you complete **session 4**. Please return after finishing it.')

