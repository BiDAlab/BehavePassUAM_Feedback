import streamlit as st

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import StandardScaler
from dtaidistance import dtw

from utils import *

def pintar_firma_analizar(data, lang):
    """
    Esta función representa una firma específica a partir de los daos de un archivo CSV de una 
    sesión anteriormente abierta.

    Parámetros:
    - data: Datos de la firma 
    """        
    data.columns = ['Col0', 'Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6', 'Col7', 'Col8', 'Col9', 'Col10', 'Col11', 'Col12', 'Col13', 'Col14', 'Col15', 'Col16', 'Col17', 'Col18']

    # Filtrar los índices de la primera firma
    first_down_indices = data[(data.iloc[:, 8] == 0) & (data.iloc[:, 16] == 1)].index.to_numpy()
    first_up_indices = data[(data.iloc[:, 8] == 1) & (data.iloc[:, 16] == 1)].index.to_numpy()
        
    # Filtrar los índices de la segunda firma
    second_down_indices = data[(data.iloc[:, 8] == 0) & (data.iloc[:, 16] == 2)].index.to_numpy()
    second_up_indices = data[(data.iloc[:, 8] == 1) & (data.iloc[:, 16] == 2)].index.to_numpy()
    
    # Filtrar los índices de borrado
    delete_indices = data[data.iloc[:, 16] == 0].index.to_numpy()
    
    # Índices de borrado   
    if delete_indices.size > 0:
        # Último índice de la primera firma
        last_first = data[data.iloc[:, 16] == 1].last_valid_index()
    
        # Primer índice de la segunda firma
        first_second=data[data.iloc[:, 16] == 2].first_valid_index()
        
        # Se comprueba en cuál firma se ha producido el borrado
        for d in range(len(delete_indices)):
            if delete_indices[d] > last_first:
                if d == 0:
                    break  # El borrado no se ha producido en la primera firma
                else:
                    # Reajustar índices
                    first_down_indices = first_down_indices[first_down_indices > delete_indices[d - 1]]
                    first_up_indices = first_up_indices[(first_up_indices >= first_down_indices[0]) & (first_up_indices <= last_first)]
                    break
    
        last_delete = delete_indices[-1]
    
        if last_delete > first_second:
            # Reajustar índices
            second_down_indices = second_down_indices[second_down_indices > last_delete]
            second_up_indices = second_up_indices[second_up_indices >= second_down_indices[0]]


    # Verificación de trazado para la primera firma
    if len(first_down_indices) > 0 and len(first_up_indices) > 0:
        
        # Plotear y guardar las firmas de la primera firma
        x_all_move, y_all_move = [], []

        # Variables para calcular complejidad
        num_arriba=len(first_up_indices)
        xTotal, yTotal = [], []
        
        for i in range(0,len(first_up_indices)):  # Asegurarse de recorrer todos los índices disponibles

        
            if (i == 0) and (first_up_indices[0] == first_down_indices[0]-1):
                first_down_indices = np.insert(first_down_indices, 0, 1)
            
            trazo = range(first_down_indices[i], first_up_indices[i]+1)
           
            data_aux2 = data.iloc[:, 2]
            data_aux4 = data.iloc[:, 4]

            # Filtrar los índices directamente usando loc y condiciones
            x_move_aux = data.loc[(data.index.isin(trazo)) & (data['Col8'] == 2) & (data['Col16'] == 1)].index
            x_move = data_aux2[x_move_aux]

            y_move_aux = data.loc[(data.index.isin(trazo)) & (data['Col8'] == 2) & (data['Col16'] == 1)].index
            y_move = data_aux4[y_move_aux]

            x_all_move.extend(x_move)
            y_all_move.extend(y_move)

        y_all_move = [-x for x in y_all_move]

        # Comprobar que hay datos para plotear
        if len(x_all_move) > 0 and len(y_all_move) > 0:
            # Añadimos el trazo total para el análisis de complejidad
            xTotal.extend(x_all_move)
            yTotal.extend(y_all_move)
        else:
            st.error(f'No se pudo trazar la firma')
            return -1, -1

        # Limpiar los vectores acumulativos
        x_all_move.clear()
        y_all_move.clear()


    ### Análisis complejidad ###
    # Datos para el analisis (al final de la función)
    TimeStamp = data.iloc[:, 0]
    Ind1Firma = data[(data.iloc[:, 16] == 1)].index.to_numpy()
    
    # Calculos de distancia completa
    signX = np.array(xTotal)
    signY = np.array(yTotal)
    total_distance = (np.sum(np.sqrt(np.diff(signX)**2 + np.diff(signY)**2))) / 100 # Suponiendo que la distancia es en cm se pasa a metros


    # Cálculos de duración
    indiceIni=Ind1Firma[0]
    indiceFin=Ind1Firma[-1]            
    timeIni=TimeStamp[indiceIni]
    timeFin=TimeStamp[indiceFin] 
    duracion = (timeFin - timeIni)/ 1e9

    # Cálculos de velocidad
    velocidad = total_distance/duracion

    mostrarMet=0
    if mostrarMet==1:
        st.write(f'velocidad: {velocidad} ')
        st.write(f'numero de veces arriba: {num_arriba} ')
        st.write(f'duración: {duracion} s')
        st.write(f'distancia: {total_distance} ')

    if lang == "es":
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
    elif lang == "en":  
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

        
    # Devolvemos la señal x e y para que luego la podamos usar en la consistencia
    return signX, signY

def conseguir_signal(data):
    """
    Esta función saca los valores del eje x e y

    Parámetros:
    - data: Datos de la firma 
    """        
    data.columns = ['Col0', 'Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6', 'Col7', 'Col8', 'Col9', 'Col10', 'Col11', 'Col12', 'Col13', 'Col14', 'Col15', 'Col16', 'Col17', 'Col18']

    # Filtrar los índices de la primera firma
    first_down_indices = data[(data.iloc[:, 8] == 0) & (data.iloc[:, 16] == 1)].index.to_numpy()
    first_up_indices = data[(data.iloc[:, 8] == 1) & (data.iloc[:, 16] == 1)].index.to_numpy()
        
    # Filtrar los índices de la segunda firma
    second_down_indices = data[(data.iloc[:, 8] == 0) & (data.iloc[:, 16] == 2)].index.to_numpy()
    second_up_indices = data[(data.iloc[:, 8] == 1) & (data.iloc[:, 16] == 2)].index.to_numpy()
    
    # Filtrar los índices de borrado
    delete_indices = data[data.iloc[:, 16] == 0].index.to_numpy()
    
    # Índices de borrado   
    if delete_indices.size > 0:
        # Último índice de la primera firma
        last_first = data[data.iloc[:, 16] == 1].last_valid_index()
    
        # Primer índice de la segunda firma
        first_second=data[data.iloc[:, 16] == 2].first_valid_index()
        
        # Se comprueba en cuál firma se ha producido el borrado
        for d in range(len(delete_indices)):
            if delete_indices[d] > last_first:
                if d == 0:
                    break  # El borrado no se ha producido en la primera firma
                else:
                    # Reajustar índices
                    first_down_indices = first_down_indices[first_down_indices > delete_indices[d - 1]]
                    first_up_indices = first_up_indices[(first_up_indices >= first_down_indices[0]) & (first_up_indices <= last_first)]
                    break
    
        last_delete = delete_indices[-1]
    
        if last_delete > first_second:
            # Reajustar índices
            second_down_indices = second_down_indices[second_down_indices > last_delete]
            second_up_indices = second_up_indices[second_up_indices >= second_down_indices[0]]


    # Verificación de trazado para la primera firma
    if len(first_down_indices) > 0 and len(first_up_indices) > 0:
        
        # Plotear y guardar las firmas de la primera firma
        x_all_move, y_all_move = [], []

        # Variables para calcular complejidad
        num_arriba=len(first_up_indices)
        xTotal, yTotal = [], []
        
        for i in range(0,len(first_up_indices)):  # Asegurarse de recorrer todos los índices disponibles

        
            if (i == 0) and (first_up_indices[0] == first_down_indices[0]-1):
                first_down_indices = np.insert(first_down_indices, 0, 1)
            
            trazo = range(first_down_indices[i], first_up_indices[i]+1)
           
            data_aux2 = data.iloc[:, 2]
            data_aux4 = data.iloc[:, 4]

            # Filtrar los índices directamente usando loc y condiciones
            x_move_aux = data.loc[(data.index.isin(trazo)) & (data['Col8'] == 2) & (data['Col16'] == 1)].index
            x_move = data_aux2[x_move_aux]

            y_move_aux = data.loc[(data.index.isin(trazo)) & (data['Col8'] == 2) & (data['Col16'] == 1)].index
            y_move = data_aux4[y_move_aux]

            x_all_move.extend(x_move)
            y_all_move.extend(y_move)

        y_all_move = [-x for x in y_all_move]

        # Comprobar que hay datos para plotear
        if len(x_all_move) > 0 and len(y_all_move) > 0:
            # Añadimos el trazo total para el análisis de complejidad
            xTotal.extend(x_all_move)
            yTotal.extend(y_all_move)
        else:
            st.error(f'No se pudo trazar la firma')
            return -1, -1

        # Limpiar los vectores acumulativos
        x_all_move.clear()
        y_all_move.clear()

    # Calculos de distancia completa
    signX = np.array(xTotal)
    signY = np.array(yTotal)

    
    # Devolvemos la señal x e y para que luego la podamos usar en la consistencia
    return signX, signY

def analisis_consistencia(xs1, ys1, xs4, ys4, lang):
    
    # Normalizamos los datos (Usando media 0, varianza 1)
    scaler = StandardScaler()

    # Estandarizar las coordenadas x e y
    xs1 = scaler.fit_transform(xs1.reshape(-1, 1)).flatten()
    ys1 = scaler.fit_transform(ys1.reshape(-1, 1)).flatten()
    xs4 = scaler.fit_transform(xs4.reshape(-1, 1)).flatten()
    ys4 = scaler.fit_transform(ys4.reshape(-1, 1)).flatten()


    # Calcular distancia DTW entre las secuencias x e y
    distance_x = dtw.distance(xs1, xs4)
    distance_y = dtw.distance(ys1,  ys4)
    average_dtw_distance = (distance_x + distance_y) / 2

    # Mostrar distancia DTW y consistencia
    #st.subheader("Métricas de Consistencia")
    #st.metric("Distancia DTW Promedio", f"{average_dtw_distance:.2f}")
    
    if lang == "es":

        TextoFirma=f'Analizando el parecido de <strong>dos de tus firmas</strong> hemos conseguido sacar los siguientes resultados sobre la <strong>consistencia</strong> de tu firma.'
        st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)

        # Comentarios de consistencia
        if average_dtw_distance < 3:
            st.success("**¡Excelente!** 🎉 Tus firmas son **muy consistentes**, lo que muestra una gran precisión en tus trazos. ¡Sigue así!")
        elif average_dtw_distance < 9:
            st.info("**¡Buen trabajo!** 👍 Tus firmas tienen **pequeñas variaciones**, pero en general muestran una **buena consistencia**. Con un poco de práctica, podrían ser aún más uniformes.")
        else:
            st.warning("Interesante... 🤔 Tus firmas muestran **diferencias notables** entre sesiones. Esto puede indicar cambios en tu trazo o estilo. ¡No te preocupes! Practicar puede ayudarte a lograr una firma más constante.")
    elif lang == "en":  
        TextoFirma = f'Analyzing the similarity of <strong>two of your signatures</strong>, we have derived the following results about the <strong>consistency</strong> of your signature.'
        st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)

        # Comments on consistency
        if average_dtw_distance < 3:
            st.success("**Excellent!** 🎉 Your signatures are **very consistent**, showing great precision in your strokes. Keep it up!")
        elif average_dtw_distance < 9:
            st.info("**Good job!** 👍 Your signatures have **small variations**, but overall they show **good consistency**. With a little practice, they could become even more uniform.")
        else:
            st.warning("Interesting... 🤔 Your signatures show **notable differences** between sessions. This could indicate changes in your stroke or style. Don’t worry! Practicing can help you achieve a more consistent signature.")




# def render_sign_tab():
#     usuario_en = st.query_params.feedback
#     usuario = decrypt(usuario_en)
#     usuario_file=f'{usuario}/config.json'
#     edadReal, lang =edad_real(usuario_file)
#     #lang = "en" 

#     if lang == "es": #Versión Español   
#         st.title('✒️ Firma')
#         TextoInicio = """<p style="font-size:20px;">En este apartado analizaremos tu firma de dos maneras diferentes a través de la <strong>complejidad</strong> y de la <strong>consistencia</strong>. Estos dos factores son muy importantes a la hora de evaluar su seguridad y autenticidad.</p>
#                                     <p style="font-size:20px;">Para que una firma sea segura, debe lograr un equilibrio entre <strong>complejidad</strong> y <strong>consistencia</strong>, siendo compleja de imitar, pero consistente para quien la produce.</p>"""
#         st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

#         usuario_en = st.query_params.feedback
#         usuario = decrypt(usuario_en)
#         consistencia = 0 # Cuando sea 2 se calculara la consistencia entre s1 y s4
#         X_firmasS1S4, Y_firmasS1S4 = [], []

#         ### CONSISTENCIA ###
#         sesiones = ['s1', 's2']
#         st.header(f'Consistencia', divider=False)
#         TextoConsistencia="""<p style="font-size:18px;"><strong>Análisis de Consistencia:</strong> A partir del análisis de la consistencia, examinaremos la capacidad de reproducir la firma de manera similar en diferentes momentos. La consistencia es clave para la autenticidad, ya que, para que una firma sea segura, debe mantener un estilo y patrones reconocibles.</p>"""
#         st.markdown(f'<p style="font-size:20px;">{TextoConsistencia}</p>', unsafe_allow_html=True)
#         for sesion in sesiones:
#             num_Sesion=int(sesion[-1])
#             zip_file=f'{usuario}/{sesion}.zip'
#             target_file=f'{sesion}/g/sign/{sesion}_g_touch.csv'
#             df=load_file_from_zip(zip_file, target_file)

#             # Comprobamos que hay datos para representar
#             if not df.empty:
#                 # Sacamos las señales
#                 signX, signY =   conseguir_signal(df)
                
#                 # Guardamos las señales para cosistencia
#                 if  (sesion == 's1') or (sesion == 's2'):
#                     X_firmasS1S4.extend([signX])
#                     Y_firmasS1S4.extend([signY])
#                     consistencia=consistencia+1
        
#         if consistencia == 2:        
#             analisis_consistencia(X_firmasS1S4[0], Y_firmasS1S4[0], X_firmasS1S4[1], Y_firmasS1S4[1], lang)
#         else:
#             st.warning(f'La **consistencia** se mostrara cuando hayas acabado la **sesión 2**. Vuelve cuando la hayas acabado.') 
    

#         ### COMPLEJIDAD ###
#         st.header(f'Complejidad', divider=False)
#         TextoComplejidad = """<p style="font-size:18px;"><strong>Análisis de Complejidad:</strong> Con el análisis de la complejidad podemos observar qué elementos hacen que tu firma sea difícil de imitar. Esto incluye la velocidad a la que la realizas, el número de trazos que utilizas, entre otros detalles únicos que la caracterizan. Cuanto más compleja sea tu firma, más difícil será para otra persona replicarla. La complejidad ayuda a que la firma sea un elemento único y distintivo.</p>"""
#         st.markdown(f'<p style="font-size:20px;">{TextoComplejidad}</p>', unsafe_allow_html=True)
        
#         #Sacamos los datos de la BBDD
#         zip_file=f'{usuario}/s4.zip'
#         target_file=f's4/g/sign/s4_g_touch.csv'
#         df=load_file_from_zip(zip_file, target_file)

#         # Comprobamos que hay datos para representar
#         if not df.empty:
#             TextoFirma=f'A partir de <strong>de las firmas</strong> que realizaste en la <strong>sesión 4</strong> hemos considerado que...'
#             st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)
#             #st.dataframe(df)
#             signX, signY=pintar_firma_analizar(df,lang) 


#         else:
#             st.warning(f'La **complejidad** se mostrara cuando hayas acabado la **sesión 4**. Vuelve cuando la hayas acabado')
    
#     elif lang == "en":
#         st.title('✒️ Signature')
#         TextoInicio = """<p style="font-size:20px;">In this section, we will analyze your signature in two different ways: through its <strong>complexity</strong> and <strong>consistency</strong>. These two factors are crucial when evaluating its security and authenticity.</p>
#                         <p style="font-size:20px;">For a signature to be secure, it must strike a balance between <strong>complexity</strong> and <strong>consistency</strong>, being difficult to imitate yet consistent for the signer.</p>"""
#         st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

#         #usuario_en = st.query_params.feedback
#         #usuario = decrypt(usuario_en)
#         consistencia = 0  # When it's 2, consistency between s1 and s4 will be calculated
#         X_firmasS1S4, Y_firmasS1S4 = [], []

#         ### CONSISTENCY ###
#         sesiones = ['s1', 's2']
#         st.header(f'Consistency', divider=False)
#         TextoConsistencia = """<p style="font-size:18px;"><strong>Consistency Analysis:</strong> Through the consistency analysis, we examine your ability to reproduce your signature similarly across different sessions. Consistency is key for authenticity, as a secure signature must maintain recognizable styles and patterns.</p>"""
#         st.markdown(f'<p style="font-size:20px;">{TextoConsistencia}</p>', unsafe_allow_html=True)

#         for sesion in sesiones:
#             num_Sesion = int(sesion[-1])
#             zip_file = f'{usuario}/{sesion}.zip'
#             target_file = f'{sesion}/g/sign/{sesion}_g_touch.csv'
#             df = load_file_from_zip(zip_file, target_file)

#             # Check if data is available
#             if not df.empty:
#                 # Extract signals
#                 signX, signY = conseguir_signal(df)

#                 # Store signals for consistency
#                 if (sesion == 's1') or (sesion == 's2'):
#                     X_firmasS1S4.extend([signX])
#                     Y_firmasS1S4.extend([signY])
#                     consistencia += 1

#         if consistencia == 2:        
#             analisis_consistencia(X_firmasS1S4[0], Y_firmasS1S4[0], X_firmasS1S4[1], Y_firmasS1S4[1],lang)
#         else:
#             st.warning(f'**Consistency** will be displayed once you complete **session 2**. Please return after finishing it.') 

#         ### COMPLEXITY ###
#         st.header(f'Complexity', divider=False)
#         TextoComplejidad = """<p style="font-size:18px;"><strong>Complexity Analysis:</strong> Through complexity analysis, we explore what makes your signature difficult to replicate. This includes factors such as the speed of execution, the number of strokes used, and other unique traits. The more complex your signature is, the harder it is for someone else to replicate. Complexity ensures that your signature is unique and distinctive.</p>"""
#         st.markdown(f'<p style="font-size:20px;">{TextoComplejidad}</p>', unsafe_allow_html=True)

#         # Retrieve data from the database
#         zip_file = f'{usuario}/s4.zip'
#         target_file = f's4/g/sign/s4_g_touch.csv'
#         df = load_file_from_zip(zip_file, target_file)

#         # Check if data is available
#         if not df.empty:
#             TextoFirma = f'Based on the <strong>signatures</strong> you provided during <strong>session 4</strong>, we have determined that...'
#             st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)
#             # st.dataframe(df)
#             signX, signY = pintar_firma_analizar(df,lang) 
#         else:
#             st.warning(f'**Complexity** will be displayed once you complete **session 4**. Please return after finishing it.')


        
def render_sign_tab_json(json_usuario, lang):
    st.warning("HOLA")
    average_dtw_distance = json_usuario.get("sign", {}).get("consistency", {}).get("avg_dtw_distance", None) #Medida consistencia

    duracion = json_usuario.get("sign", {}).get("complexity", {}).get("duracion", None) #Medida complejidad - duracion
    num_arriba = json_usuario.get("sign", {}).get("complexity", {}).get("num_arriba", None) #Medida complejidad - num_arriba
    total_distance = json_usuario.get("sign", {}).get("complexity", {}).get("total_distance", None) #Medida complejidad - total_distance

    if lang == "es": #Versión Español   
        st.title('✒️ Firma')
        TextoInicio = """<p style="font-size:20px;">En este apartado analizaremos tu firma de dos maneras diferentes a través de la <strong>complejidad</strong> y de la <strong>consistencia</strong>. Estos dos factores son muy importantes a la hora de evaluar su seguridad y autenticidad.</p>
                                    <p style="font-size:20px;">Para que una firma sea segura, debe lograr un equilibrio entre <strong>complejidad</strong> y <strong>consistencia</strong>, siendo compleja de imitar, pero consistente para quien la produce.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

        usuario_en = st.query_params.feedback
        usuario = decrypt(usuario_en)
        consistencia = 0 # Cuando sea 2 se calculara la consistencia entre s1 y s4
        X_firmasS1S4, Y_firmasS1S4 = [], []

        ### CONSISTENCIA ##
        st.header(f'Consistencia', divider=False)
        TextoConsistencia="""<p style="font-size:18px;"><strong>Análisis de Consistencia:</strong> A partir del análisis de la consistencia, examinaremos la capacidad de reproducir la firma de manera similar en diferentes momentos. La consistencia es clave para la autenticidad, ya que, para que una firma sea segura, debe mantener un estilo y patrones reconocibles.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoConsistencia}</p>', unsafe_allow_html=True)
        
        if average_dtw_distance != -1:        
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


        else:
            st.warning(f'La **complejidad** se mostrara cuando hayas acabado la **sesión 4**. Vuelve cuando la hayas acabado')
    
    elif lang == "en":
        st.title('✒️ Signature')
        TextoInicio = """<p style="font-size:20px;">In this section, we will analyze your signature in two different ways: through its <strong>complexity</strong> and <strong>consistency</strong>. These two factors are crucial when evaluating its security and authenticity.</p>
                        <p style="font-size:20px;">For a signature to be secure, it must strike a balance between <strong>complexity</strong> and <strong>consistency</strong>, being difficult to imitate yet consistent for the signer.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)

        #usuario_en = st.query_params.feedback
        #usuario = decrypt(usuario_en)
        consistencia = 0  # When it's 2, consistency between s1 and s4 will be calculated
        X_firmasS1S4, Y_firmasS1S4 = [], []

        ### CONSISTENCY ###
        sesiones = ['s1', 's2']
        st.header(f'Consistency', divider=False)
        TextoConsistencia = """<p style="font-size:18px;"><strong>Consistency Analysis:</strong> Through the consistency analysis, we examine your ability to reproduce your signature similarly across different sessions. Consistency is key for authenticity, as a secure signature must maintain recognizable styles and patterns.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoConsistencia}</p>', unsafe_allow_html=True)

        for sesion in sesiones:
            num_Sesion = int(sesion[-1])
            zip_file = f'{usuario}/{sesion}.zip'
            target_file = f'{sesion}/g/sign/{sesion}_g_touch.csv'
            df = load_file_from_zip(zip_file, target_file)

            # Check if data is available
            if not df.empty:
                # Extract signals
                signX, signY = conseguir_signal(df)

                # Store signals for consistency
                if (sesion == 's1') or (sesion == 's2'):
                    X_firmasS1S4.extend([signX])
                    Y_firmasS1S4.extend([signY])
                    consistencia += 1

        if consistencia == 2:        
            analisis_consistencia(X_firmasS1S4[0], Y_firmasS1S4[0], X_firmasS1S4[1], Y_firmasS1S4[1],lang)
        else:
            st.warning(f'**Consistency** will be displayed once you complete **session 2**. Please return after finishing it.') 

        ### COMPLEXITY ###
        st.header(f'Complexity', divider=False)
        TextoComplejidad = """<p style="font-size:18px;"><strong>Complexity Analysis:</strong> Through complexity analysis, we explore what makes your signature difficult to replicate. This includes factors such as the speed of execution, the number of strokes used, and other unique traits. The more complex your signature is, the harder it is for someone else to replicate. Complexity ensures that your signature is unique and distinctive.</p>"""
        st.markdown(f'<p style="font-size:20px;">{TextoComplejidad}</p>', unsafe_allow_html=True)

        # Retrieve data from the database
        zip_file = f'{usuario}/s4.zip'
        target_file = f's4/g/sign/s4_g_touch.csv'
        df = load_file_from_zip(zip_file, target_file)

        # Check if data is available
        if not df.empty:
            TextoFirma = f'Based on the <strong>signatures</strong> you provided during <strong>session 4</strong>, we have determined that...'
            st.markdown(f'<p style="font-size:18px;">{TextoFirma}</p>', unsafe_allow_html=True)
            # st.dataframe(df)
            signX, signY = pintar_firma_analizar(df,lang) 
        else:
            st.warning(f'**Complexity** will be displayed once you complete **session 4**. Please return after finishing it.')