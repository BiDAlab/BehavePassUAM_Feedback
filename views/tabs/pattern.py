import streamlit as st

import pandas as pd
import os
import matplotlib.pyplot as plt

from utils import *

def pintar_patron(datosPatron):
    #Datos necesarios
    finger_down = datosPatron[(datosPatron.iloc[:, 8] == 0)].index.to_numpy()
    finger_up = datosPatron[(datosPatron.iloc[:, 8] == 1)].index.to_numpy()

    # Inicializar vectores para ir acumulando
    x_all_down = []
    y_all_down = []
    x_all_up = []
    y_all_up = []
    x_all_move = []
    y_all_move = []

    # Valores de cada trazo
    x_down = datosPatron.iloc[finger_down, 2].values
    y_down = datosPatron.iloc[finger_down, 4].values

    x_up = datosPatron.iloc[finger_up, 2].values
    y_up = datosPatron.iloc[finger_up, 4].values

    # Para las coordenadas de movimiento, se toman solo las que estén entre los índices down y up
    trazo_indices = range(finger_down[0], finger_up[-1] + 1)

    # Crear una máscara booleana para los índices en el rango deseado y donde el valor de la columna 8 es 2
    mask = (datosPatron.index.isin(trazo_indices)) & (datosPatron.iloc[:, 8] == 2)

    # Seleccionar las columnas deseadas
    x_move = datosPatron.loc[mask, 2].values
    y_move = datosPatron.loc[mask, 4].values

    # Actualizar listas acumulativas
    x_all_down.extend(x_down)
    y_all_down.extend(y_down)
    x_all_up.extend(x_up)
    y_all_up.extend(y_up)
    x_all_move.extend(x_move)
    y_all_move.extend(y_move)

    # Representación
    figura = plt.figure()
    plt.plot(x_all_move, [-y for y in y_all_move], 'b-', linewidth=2)
    plt.plot(x_all_down, [-y for y in y_all_down], 'o', markerfacecolor='g', markersize=8)
    plt.plot(x_all_up, [-y for y in y_all_up], 'o', markerfacecolor='r', markersize=8)

    plt.title(f'Figura Patron')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.legend(['Acción Movimiento', 'Acción Pulsación', 'Acción Levantamiento'])
    plt.grid(True)
    #plt.show()
    st.pyplot(figura)


def dibujar_patron(datosPatron):
    #Datos necesarios
    finger_down = datosPatron[(datosPatron.iloc[:, 8] == 0)].index.to_numpy()[-1]
    finger_up = datosPatron[(datosPatron.iloc[:, 8] == 1)].index.to_numpy()[-1]

    # Inicializar vectores para ir acumulando
    x_all_down = []
    y_all_down = []
    x_all_up = []
    y_all_up = []
    x_all_move = []
    y_all_move = []

    # Valores de cada trazo
    x_down = datosPatron.iloc[finger_down, 2]#.values
    y_down = datosPatron.iloc[finger_down, 4]#.values

    x_up = datosPatron.iloc[finger_up, 2]#.values
    y_up = datosPatron.iloc[finger_up, 4]#.values

    # Para las coordenadas de movimiento, se toman solo las que estén entre los índices down y up
    trazo_indices = range(finger_down, finger_up + 1)

    # Crear una máscara booleana para los índices en el rango deseado y donde el valor de la columna 8 es 2
    mask = (datosPatron.index.isin(trazo_indices)) & (datosPatron.iloc[:, 8] == 2)

    # Seleccionar las columnas deseadas
    x_move = datosPatron.loc[mask, 2].values
    y_move = datosPatron.loc[mask, 4].values

    # Actualizar listas acumulativas
    x_all_down.append(x_down)
    y_all_down.append(y_down)
    x_all_up.append(x_up)
    y_all_up.append(y_up)
    x_all_move.extend(x_move)
    y_all_move.extend(y_move)

    # Representación
    figura = plt.figure()
    plt.plot(x_all_move, [-y for y in y_all_move], 'b-', linewidth=2)
    plt.plot(x_all_down, [-y for y in y_all_down], 'o', markerfacecolor='g', markersize=8)
    plt.plot(x_all_up, [-y for y in y_all_up], 'o', markerfacecolor='r', markersize=8)

    plt.title(f'Representación de tu Patrón')
    #plt.xlabel('Coordenada X')
    #plt.ylabel('Coordenada Y')
    plt.legend(['Deslizamiento', 'Inicio', 'Fin'])
    plt.grid(True)
    plt.xticks([])  # Elimina valores en el eje x
    plt.yticks([])
    #plt.show()
    st.pyplot(figura)
    
    
def compare_patterns(datos_comp_pattern, lang):
    # Seleccionar solo las columnas pares y asignar nombres a las columnas
    datos_comp_pattern = datos_comp_pattern.iloc[:, ::2]
    datos_comp_pattern.columns = ['timestamp', 'x', 'y', 'position', 'previous', 'rect']
    
    # Convertir la columna 'position' en una lista de valores, ignorando el encabezado si es necesario
    pattern_list = datos_comp_pattern['position'][1:].astype(int).tolist()  # Ignorar la primera fila si es el nombre de columna
    
    # Listas predeterminadas para comparar
    predefined_lists = [
        [0,1,2,5,8],
        [8,5,2,1,0],
        [6,3,0,1,2,5,8],
        [0,3,6,7,8,5,2],
        [0,3,6,7,8],
        [8,7,6,3,0],
        [2,1,0,3,6,7,8],
        [0,1,2,5,8,7,6],
        [2,1,0,3,4,5,8,7,6],
        [6,7,8,5,4,3,0,2,1],
        [0,3,6,7,8,5,2,1],
        [0,1,2,5,8,7,6,3],
        [6,3,0,4,2,5,8],
        [6,3,0,4,8,5,2],
        [0,1,2,4,6,7,8],
    ]
    
    # Comprobar si 'position_list' coincide con alguna de las listas predeterminadas
    is_match = pattern_list in predefined_lists
    
    if lang == "es":
        if is_match:
            TextoPattern=f'<b>¡Vaya!</b> Parece que tu patrón es uno de los más comunes 🔓. Deberías tener cuidado porque puede ser fácil de adivinar'
            st.markdown(f'<p style="font-size:18px;">{TextoPattern}</p>', unsafe_allow_html=True)
        else:
            TextoPattern=f'<b>¡Genial!</b> Tu patrón de desbloqueo no es de los más comunes, parece muy seguro 🔒. ¡Se nota que te tomas en serio la ciberseguridad, sigue así!'
            st.markdown(f'<p style="font-size:18px;">{TextoPattern}</p>', unsafe_allow_html=True)
    elif lang == "en":
        if is_match:
            TextoPattern = f'<b>Oops!</b> It seems that your unlock pattern is one of the most common 🔓. You should be careful because it might be easy to guess.'
            st.markdown(f'<p style="font-size:18px;">{TextoPattern}</p>', unsafe_allow_html=True)
        else:
            TextoPattern = f'<b>Great!</b> Your unlock pattern is not one of the most common, it seems very secure 🔒. It shows that you take cybersecurity seriously, keep it up!'
            st.markdown(f'<p style="font-size:18px;">{TextoPattern}</p>', unsafe_allow_html=True)
        
    

# def render_pattern_tab():
#     usuario_en = st.query_params.feedback
#     usuario = decrypt(usuario_en)
#     usuario_file=f'{usuario}/config.json'
#     edadReal, lang =edad_real(usuario_file)
#     #lang = "en" 
    
#     if lang == "es":
#         st.title('Patrón de desbloqueo 🔓')
#         st.header('¿Sabías que...?')
#         TextoInicio = """<p style="font-size:20px;"> Los patrones de desbloqueo son uno de los métodos de seguridad más populares en dispositivos móviles.</p>
#         <p style="font-size:20px;">La mayoría de los patrones de desbloqueo tienden a seguir formas comunes o secuencias repetitivas, lo que los hace fáciles de recordar, pero también más predecibles y, por lo tanto, menos seguros si no se eligen cuidadosamente.</p>
#         <p style="font-size:20px;">En la imagen a continuación, te mostramos algunos de los más comunes.</p>"""
#         st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)
#         st.image('static/images/patrones_comunes.jpg', use_column_width=True, clamp=True)

#         usuario_en = st.query_params.feedback
#         usuario = decrypt(usuario_en)

#         #Sacamos los datos de la BBDD
#         zip_file=f'{usuario}/s3.zip'
#         target_file=f's3/g/pattern/s3_g_touch.csv'
#         target_file2=f's3/g/pattern/s3_g_touch_pattern.csv'

#         df_t=load_file_from_zip(zip_file, target_file)
#         if not df_t.empty:
#             df_t_p=load_file_from_zip(zip_file, target_file2)
#             if not df_t_p.empty:
#                 TextoInicio2 = """<p style="font-size:20px;"> ¿Te atreves a analizar el tuyo?</p>"""
#                 st.markdown(f'<p style="font-size:20px;">{TextoInicio2}</p>', unsafe_allow_html=True)   
#                 #st.subheader(f'Datos de la sesión {num_Sesion}', divider=dividers[num_Sesion-1])    
#                 compare_patterns(df_t_p, lang)
#             else:
#                 st.warning(f'¡Lo sentimos! En esta ocasión no vamos a poder analizar tu patrón de desbloqueo. Echa un ojo al resto de tareas, tienes mucha información interesante disponible.')
#         else:
#             st.warning(f'Los resultados del **patrón** se mostrarán cuando hayas acabado la **sesión 3**. Vuelve cuando la hayas acabado.')

#     elif lang == "en":
#         st.title('Unlock Pattern 🔓')
#         st.header('Did you know...?')
#         TextoInicio = """<p style="font-size:20px;">Unlock patterns are one of the most popular security methods on mobile devices.</p>
#         <p style="font-size:20px;">Most unlock patterns tend to follow common shapes or repetitive sequences, making them easy to remember but also more predictable, and therefore less secure if not carefully chosen.</p>
#         <p style="font-size:20px;">In the image below, we show you some of the most common patterns.</p>"""
#         st.markdown(f'<p style="font-size:20px;">{TextoInicio}</p>', unsafe_allow_html=True)
#         st.image('static/images/patrones_comunes.jpg', use_column_width=True, clamp=True)

#         usuario_en = st.query_params.feedback
#         usuario = decrypt(usuario_en)

#         # Fetch data from the database
#         zip_file = f'{usuario}/s3.zip'
#         target_file = f's3/g/pattern/s3_g_touch.csv'
#         target_file2 = f's3/g/pattern/s3_g_touch_pattern.csv'

#         df_t = load_file_from_zip(zip_file, target_file)
#         if not df_t.empty:
#             df_t_p = load_file_from_zip(zip_file, target_file2)
#             if not df_t_p.empty:
#                 TextoInicio2 = """<p style="font-size:20px;"> Dare to analyze yours?</p>"""
#                 st.markdown(f'<p style="font-size:20px;">{TextoInicio2}</p>', unsafe_allow_html=True)   
#                 compare_patterns(df_t_p, lang)
#             else:
#                 st.warning(f'Sorry! This time we won’t be able to analyze your unlock pattern. Check out the rest of the tasks, there’s plenty of interesting information available.')
#         else:
#             st.warning(f'Pattern results will be shown once you complete session 3. Come back when you have finished.')

            

def render_pattern_tab_json(json_usuario, lang):
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

            
            