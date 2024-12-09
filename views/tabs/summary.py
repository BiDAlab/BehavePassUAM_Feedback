import streamlit as st
from utils import *

def render_summary_tab(lang):
    usuario_en = st.query_params.feedback
    usuario = decrypt(usuario_en)
    usuario_file=f'{usuario}/config.json'
    edadReal, lang =edad_real(usuario_file)
    #lang = "en" 

    if lang == "es": #Versión Español
        cols = st.columns([1,3,1], vertical_alignment='center')
        cols[0].write('')
        cols[2].write('')
        with cols[1]:
            st.header('¡Bienvenid@ a tu tablero de resultados de BehavePassUAM!')
            st.subheader('Aquí puedes ver el desempeño de tus sesiones y conocer tus avances')
 
            st.divider()
            # Sacamos la última sesión para personalizar el mensaje
            lastSes=ultima_sesion(usuario_file)
            #lastSes='s3'
            #st.text(f'La ultima sesion es: {lastSes}')
            if lastSes=='s1':
                info_message = """
                <p style="font-size:20px;">Al finalizar cada sesión, recibirás un <strong>enlace personalizado</strong> con información interesante sobre las pruebas que has realizado. Es <b>importante que <u>NO compartas</u> este enlace</b> con nadie para proteger tu privacidad. 🔒</p>
                <hr>
                <p style="font-size:20px;">🔓 Al haber completado la <strong>sesión 1</strong>, en esta página encontrarás la siguiente <b>información</b> sobre las <b><u>tareas realizadas durante la sesión</u></b>:<br><br>
                <b><i>- Tap el Topo</i></b> 🐹: conocerás tu velocidad de reacción en la tarea de pulsar el topo. Además, podrás comparar tu rapidez respecto al resto de usuarios de BehavePassUAM.<br>
                <b><i>- Predicción de Edad</i></b> 🎯: trataremos de estimar tu rango de edad en base a la manera que tienes de interactuar con el dispositivo móvil.<br>
                <b><i>- Galería</i></b> 🖼️: te decimos el número de aciertos y fallos.</p><br>
                <p style="font-size:20px;">🔒 Al <strong>completar</strong> el resto de <strong>sesiones</strong> podrás desbloquear <strong>más información</strong>:<br><br>
                <b><i>- Firma</i></b> ✒️: evaluamos cuánto de segura es tu firma a partir de su complejidad y consistencia.<br>
                <b><i>- Patrón de Desbloqueo</i></b> 🔒: podrás conocer si tu patrón de desbloqueo es uno de los más comunes entre la población.<br>
                <b><i>- Galería</i></b> 🖼️: evaluamos tu nivel de memoria visual a partir de los datos obtenidos en la prueba de la galería.</p>
                <hr>
                <p style="font-size:20px;">Si te ha gustado ♥️ esta información, recuerda <b>compartir la app</b> con tus familiares y amigos para tener más oportunidades de ganar en los sorteos ¡y no olvides <b>seguirnos</b> en nuestras <b>redes sociales</b>! De esta forma nos ayudas a que más gente participe en el estudio de investigación y, además, ¡consigues más puntos en los sorteos que organizamos!<br><br> ¡<b>Muchas gracias por participar </b> en este proyecto de investigación y <b>mucha suerte 🍀</b> en los sorteos!</p>
                <hr>
                <p style="font-size:20px; text-align:center;">Síguenos en nuestras redes sociales:</p>
                <p style="font-size:20px; text-align:center;">
                    <a href="https://x.com/i/flow/login?redirect_after_login=%2Fbehavepassuam" target="_blank" style="text-decoration:none; font-size:20px;">🐦 Twitter</a><br>
                    <a href="https://www.instagram.com/behavepassuam/?igsh=OHk5OXlnZG90cGFv" target="_blank" style="text-decoration:none; font-size:20px;">📸 Instagram</a><br>
                    <a href="https://www.facebook.com/people/Behavepassuam/61567187651116/" target="_blank" style="text-decoration:none; font-size:20px;">📘 Facebook</a><br>
                    <a href="https://behavepassuam.humanairesearch.com/es" target="_blank" style="text-decoration:none; font-size:20px;">💻 Página Web</a>
                </p>
                """
            elif lastSes=='s2':
                info_message = """
                <p style="font-size:20px;">Al finalizar cada sesión, recibirás un <strong>enlace personalizado</strong> con información interesante sobre las pruebas que has realizado. Es <b>importante que <u>NO compartas</u> este enlace</b> con nadie para proteger tu privacidad. 🔒</p>
                <hr>
                <p style="font-size:20px;">🔓 Al haber completado la <strong>sesión 2</strong>, en esta página encontrarás la siguiente <b>información</b> sobre las <b><u>tareas realizadas durante la sesión</u></b>:<br><br>
                <b><i>- Tap el Topo</i></b> 🐹: conocerás tu velocidad de reacción en la tarea de pulsar el topo. Además, podrás comparar tu rapidez respecto al resto de usuarios de BehavePassUAM.<br>
                <b><i>- Predicción de Edad</i></b> 🎯: trataremos de estimar tu rango de edad en base a la manera que tienes de interactuar con el dispositivo móvil.<br>
                <b><i>- Galería</i></b> 🖼️: te decimos el número de aciertos y fallos.<br>
                <b><i>- Firma</i></b> ✒️: evaluamos cuánto de segura es tu firma a partir de su consistencia.</p><br>
                <p style="font-size:20px;">🔒 Al <strong>completar</strong> el resto de <strong>sesiones</strong> podrás desbloquear <strong>más información</strong>:<br><br>
                <b><i>- Firma</i></b> ✒️: evaluamos cuánto de segura es tu firma a partir de su complejidad.<br>
                <b><i>- Patrón de Desbloqueo</i></b> 🔒: podrás conocer si tu patrón de desbloqueo es uno de los más comunes entre la población.<br>
                <b><i>- Galería</i></b> 🖼️: evaluamos tu nivel de memoria visual a partir de los datos obtenidos en la prueba de la galería.</p>
                <hr>
                <p style="font-size:20px;">Si te ha gustado ♥️ esta información, recuerda <b>compartir la app</b> con tus familiares y amigos para tener más oportunidades de ganar en los sorteos ¡y no olvides <b>seguirnos</b> en nuestras <b>redes sociales</b>! De esta forma nos ayudas a que más gente participe en el estudio de investigación y, además, ¡consigues más puntos en los sorteos que organizamos!<br><br> ¡<b>Muchas gracias por participar </b> en este proyecto de investigación y <b>mucha suerte 🍀</b> en los sorteos!</p>
                <hr>
                <p style="font-size:20px; text-align:center;">Síguenos en nuestras redes sociales:</p>
                <p style="font-size:20px; text-align:center;">
                    <a href="https://x.com/i/flow/login?redirect_after_login=%2Fbehavepassuam" target="_blank" style="text-decoration:none; font-size:20px;">🐦 Twitter</a><br>
                    <a href="https://www.instagram.com/behavepassuam/?igsh=OHk5OXlnZG90cGFv" target="_blank" style="text-decoration:none; font-size:20px;">📸 Instagram</a><br>
                    <a href="https://www.facebook.com/people/Behavepassuam/61567187651116/" target="_blank" style="text-decoration:none; font-size:20px;">📘 Facebook</a><br>
                    <a href="https://behavepassuam.humanairesearch.com/es" target="_blank" style="text-decoration:none; font-size:20px;">💻 Página Web</a>
                </p>
                """
            elif lastSes=='s3':
                info_message = """
                <p style="font-size:20px;">Al finalizar cada sesión, recibirás un <strong>enlace personalizado</strong> con información interesante sobre las pruebas que has realizado. Es <b>importante que <u>NO compartas</u> este enlace</b> con nadie para proteger tu privacidad. 🔒</p>
                <hr>
                <p style="font-size:20px;">🔓 Al haber completado la <strong>sesión 3</strong>, en esta página encontrarás la siguiente <b>información</b> sobre las <b><u>tareas realizadas durante la sesión</u></b>:<br><br>
                <b><i>- Tap el Topo</i></b> 🐹: conocerás tu velocidad de reacción en la tarea de pulsar el topo. Además, podrás comparar tu rapidez respecto al resto de usuarios de BehavePassUAM.<br>
                <b><i>- Predicción de Edad</i></b> 🎯: trataremos de estimar tu rango de edad en base a la manera que tienes de interactuar con el dispositivo móvil.<br>
                <b><i>- Galería</i></b> 🖼️: te decimos el número de aciertos y fallos.<br>
                <b><i>- Firma</i></b> ✒️: evaluamos cuánto de segura es tu firma a partir de su consistencia.<br>
                <b><i>- Patrón de Desbloqueo</i></b> 🔒: podrás conocer si tu patrón de desbloqueo es uno de los más comunes entre la población.<br></p><br>
                <p style="font-size:20px;">🔒 Al <strong>completar</strong> la última <strong>sesiones</strong> podrás desbloquear <strong>más información</strong>:<br><br>
                <b><i>- Firma</i></b> ✒️: evaluamos cuánto de segura es tu firma a partir de su complejidad.<br>
                <b><i>- Galería</i></b> 🖼️: evaluamos tu nivel de memoria visual a partir de los datos obtenidos en la prueba de la galería.</p>
                <hr>
                <p style="font-size:20px;">Si te ha gustado ♥️ esta información, recuerda <b>compartir la app</b> con tus familiares y amigos para tener más oportunidades de ganar en los sorteos ¡y no olvides <b>seguirnos</b> en nuestras <b>redes sociales</b>! De esta forma nos ayudas a que más gente participe en el estudio de investigación y, además, ¡consigues más puntos en los sorteos que organizamos!<br><br> ¡<b>Muchas gracias por participar </b> en este proyecto de investigación y <b>mucha suerte 🍀</b> en los sorteos!</p>
                <hr>
                <p style="font-size:20px; text-align:center;">Síguenos en nuestras redes sociales:</p>
                <p style="font-size:20px; text-align:center;">
                    <a href="https://x.com/i/flow/login?redirect_after_login=%2Fbehavepassuam" target="_blank" style="text-decoration:none; font-size:20px;">🐦 Twitter</a><br>
                    <a href="https://www.instagram.com/behavepassuam/?igsh=OHk5OXlnZG90cGFv" target="_blank" style="text-decoration:none; font-size:20px;">📸 Instagram</a><br>
                    <a href="https://www.facebook.com/people/Behavepassuam/61567187651116/" target="_blank" style="text-decoration:none; font-size:20px;">📘 Facebook</a><br>
                    <a href="https://behavepassuam.humanairesearch.com/es" target="_blank" style="text-decoration:none; font-size:20px;">💻 Página Web</a>
                </p>
                """
            else:
                info_message = """
                <p style="font-size:20px;">Al finalizar cada sesión, recibirás un <strong>enlace personalizado</strong> con información interesante sobre las pruebas que has realizado. Es <b>importante que <u>NO compartas</u> este enlace</b> con nadie para proteger tu privacidad. 🔒</p>
                <hr>
                <p style="font-size:20px;">En esta página encontrarás la siguiente <b>información</b> sobre las <b><u>tareas realizadas durante las 4 sesiones</u></b>:<br><br>
                <b><i>- Tap el Topo</i></b> 🐹: conocerás tu velocidad de reacción en la tarea de pulsar el topo. Además, podrás comparar tu rapidez respecto al resto de usuarios de BehavePassUAM.<br>
                <b><i>- Firma</i></b> ✒️: evaluamos cuánto de segura es tu firma a partir de su complejidad y consistencia.<br>
                <b><i>- Patrón de Desbloqueo</i></b> 🔒: podrás conocer si tu patrón de desbloqueo es uno de los más comunes entre la población.<br>
                <b><i>- Predicción de Edad</i></b> 🎯: trataremos de estimar tu rango de edad en base a la manera que tienes de interactuar con el dispositivo móvil.<br>
                <b><i>- Galería</i></b> 🖼️: evaluamos tu nivel de memoria visual a partir de los datos obtenidos en la prueba de la galería.</p>
                <hr>
                <p style="font-size:20px;">Si te ha gustado ♥️ esta información, recuerda <b>compartir la app</b> con tus familiares y amigos para tener más oportunidades de ganar en los sorteos ¡y no olvides <b>seguirnos</b> en nuestras <b>redes sociales</b>! De esta forma nos ayudas a que más gente participe en el estudio de investigación y, además, ¡consigues más puntos en los sorteos que organizamos!<br><br> ¡<b>Muchas gracias por participar </b> en este proyecto de investigación y <b>mucha suerte 🍀</b> en los sorteos!</p>
                <hr>
                <p style="font-size:20px; text-align:center;">Síguenos en nuestras redes sociales:</p>
                <p style="font-size:20px; text-align:center;">
                    <a href="https://x.com/i/flow/login?redirect_after_login=%2Fbehavepassuam" target="_blank" style="text-decoration:none; font-size:20px;">🐦 Twitter</a><br>
                    <a href="https://www.instagram.com/behavepassuam/?igsh=OHk5OXlnZG90cGFv" target="_blank" style="text-decoration:none; font-size:20px;">📸 Instagram</a><br>
                    <a href="https://www.facebook.com/people/Behavepassuam/61567187651116/" target="_blank" style="text-decoration:none; font-size:20px;">📘 Facebook</a><br>
                    <a href="https://behavepassuam.humanairesearch.com/es" target="_blank" style="text-decoration:none; font-size:20px;">💻 Página Web</a>
                </p>
                """


            # Mostrar el mensaje en el recuadro azul
            #st.markdown(f'<div style="background-color: #e7f3fe; padding: 10px; border-radius: 15px; font-size: 17px;">{info_message}</div>', unsafe_allow_html=True)
            st.markdown(f"""<div style="border: 10px solid #e7f3fe; padding: 10px; border-radius: 15px; font-size: 17px; background-color: transparent;"> {info_message}</div>""",unsafe_allow_html=True)
    

    elif lang == "en": #Versión inglés
        cols = st.columns([1,3,1], vertical_alignment='center')
        cols[0].write('')
        cols[2].write('')
        with cols[1]:
            st.header('Welcome to your BehavePassUAM dashboard!')
            st.subheader('We are so happy you are here! This is where you can view the performance of your sessions and see your progress in the app.')
    
            st.divider()
            info_message = """
            <p style="font-size:20px;">At the end of each session, you will receive a <strong>personalized link</strong> with interesting information about the tests you have completed. It is <b>important that you <u>DO NOT share</u> this link</b> with anyone to protect your privacy. 🔒</p>
            <hr>
            <p style="font-size:20px;">On this page, you will find the following <b>information</b> about the <b><u>tasks completed during the 4 sessions</u></b>:<br><br>
            <b><i>- Tap the Mole</i></b> 🐹: you will learn about your reaction speed in the mole tapping task. Additionally, you will be able to compare your speed with other BehavePassUAM users.<br>
            <b><i>- Signature</i></b> ✒️: we assess how secure your signature is based on its complexity and consistency.<br>
            <b><i>- Unlock Pattern</i></b> 🔒: you can find out if your unlock pattern is one of the most common among the population.<br>
            <b><i>- Age Prediction</i></b> 🎯: we try to estimate your age range based on how you interact with the mobile device.<br>
            <b><i>- Gallery</i></b> 🖼️: we evaluate your level of visual memory based on the data collected in the gallery task.</p>
            <hr>
            <p style="font-size:20px;">If you liked ♥️ this information, remember to <b>share the app</b> with your family and friends to get more chances to win in the raffles! And don't forget to <b>follow us</b> on our <b>social media</b>! This way, you help more people join the research study and, on top of that, you earn more points for the raffles we organize!<br><br> Thank you so much for participating <b>in this research project</b> and <b>good luck 🍀</b> in the raffles!</p>
            <hr>
            <p style="font-size:20px; text-align:center;">Follow us on our social media:</p>
            <p style="font-size:20px; text-align:center;">
                <a href="https://x.com/i/flow/login?redirect_after_login=%2Fbehavepassuam" target="_blank" style="text-decoration:none; font-size:20px;">🐦 Twitter</a><br>
                <a href="https://www.instagram.com/behavepassuam/?igsh=OHk5OXlnZG90cGFv" target="_blank" style="text-decoration:none; font-size:20px;">📸 Instagram</a><br>
                <a href="https://www.facebook.com/people/Behavepassuam/61567187651116/" target="_blank" style="text-decoration:none; font-size:20px;">📘 Facebook</a><br>
                <a href="https://behavepassuam.humanairesearch.com/es" target="_blank" style="text-decoration:none; font-size:20px;">💻 Web page</a>
            </p>
            """


            # Mostrar el mensaje en el recuadro azul
            #st.markdown(f'<div style="background-color: #e7f3fe; padding: 10px; border-radius: 15px; font-size: 17px;">{info_message}</div>', unsafe_allow_html=True)
            st.markdown(f"""<div style="border: 10px solid #e7f3fe; padding: 10px; border-radius: 15px; font-size: 17px; background-color: transparent;"> {info_message}</div>""",unsafe_allow_html=True)

