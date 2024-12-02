import json

import pandas as pd
import streamlit as st
import ftplib
import ssl
from getpass import getpass
import io
import zipfile
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

from .enums import TestFileName


# Firebase bucket connection
@st.cache_resource
def connect_ftps2():
    try:
        # Configura el contexto SSL/TLS
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Asegura que se use TLS
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Desactiva TLS 1.0 y 1.1
        context.check_hostname = False  # Deshabilita la verificación de nombre de host
        context.verify_mode = ssl.CERT_NONE  # Omite la validación del certificado (solo para pruebas)

        # Conecta al servidor FTPS
        ftps = ftplib.FTP_TLS(context=context)
        ftps.encoding = "latin-1"

        # Intenta la conexión
        ftps.connect(st.secrets["ftps"]["host"], st.secrets["ftps"]["port"],timeout = 30)
        ftps.login(st.secrets["ftps"]["user"], st.secrets["ftps"]["password"])
        ftps.sock.settimeout(60)

        ftps.prot_p()  # Habilita la protección de datos
        #ftplib.FTP_TLS.debugging = 2  # Activa el modo de depuración (2 genera detalles completos)
        return ftps

    except Exception as e:
        st.error(f"Error al conectar con el servidor FTPS: {e}")
        return None

@st.cache_resource
def connect_ftps():
 
    # Acceder a los secretos
    host = st.secrets["ftps"]["host"]
    username = st.secrets["ftps"]["user"]
    password = st.secrets["ftps"]["password"]
    port = st.secrets["ftps"]["port"]
 
    # Establece la conexión FTPS usando TLS
    context = ssl.create_default_context()
    ftps = ftplib.FTP_TLS()
    ftps.encoding = "latin-1"
 
    # Conectar al servidor FTPS
    ftps.connect(host, port)
    ftps.login(username, password)
 
    # Forzar la protección de datos (TLS para el canal de datos)
    ftps.prot_p()
    return ftps

@st.cache_data
# Función para listar archivos en el servidor
def list_files():
    #Conectamos con FTPS
    ftps=connect_ftps()
    files = ftps.nlst()
    
    return files

@st.cache_data
# Función de ejemplo para cargar un archivo en un DataFrame
def load_file(ftps, file):
    with io.BytesIO() as data:
        ftps.retrbinary('RETR ' + file, data.write)
        data.seek(0)
        return pd.read_csv(data, sep='\t', header=0)



# Función para cargar un archivo que tenga zip en un DataFrame
@st.cache_data
def load_file_from_zip(zip_file, target_file):
   
    #Conectamos con FTPS
    ftps=connect_ftps()

    if not ftps:
        st.error("No se pudo establecer la conexión FTPS.")
        return pd.DataFrame()  # Retorna un DataFrame vacío si no se pudo conectard
 
    try:
        # Descarga el archivo zip en memoria
        with io.BytesIO() as zip_data:
            ftps.retrbinary('RETR ' + zip_file, zip_data.write)
            zip_data.seek(0)  # Reinicia el puntero al inicio del buffer
           
            # Descomprime el archivo zip en memoria
            with zipfile.ZipFile(zip_data) as z:
                # Verifica si el archivo objetivo existe en el zip
                if target_file in z.namelist():
                    # Si existe, abre el archivo y lo carga en un DataFrame
                    with z.open(target_file) as target_data:
                       
                        return pd.read_csv(target_data, sep='\t', header=None)
                else:
                    # Si no existe, devuelve un mensaje o un DataFrame vacío
                    print(f"El archivo {target_file} no se encontró en el zip.")
                   
                    return pd.DataFrame()  # O puedes devolver None si prefieres
    except FileNotFoundError:
        # Si el archivo zip no se encuentra, devuelve un mensaje o un DataFrame vacío
        print(f"El archivo zip {zip_file} no se encontró en el servidor FTPS.")
       
        return pd.DataFrame()  # O puedes devolver None si prefieres
   
    except zipfile.BadZipFile:
        # Si el archivo descargado no es un zip válido, maneja el error
        print(f"El archivo {zip_file} no es un archivo zip válido.")
       
        return pd.DataFrame()
   
    except Exception as e:
        st.error(f"Ocurrió un error jeje: {e}")
       
        return pd.DataFrame()


    
    

# Función para cargar varios archivos que tenga zip en diferentes DataFrame
@st.cache_data
def load_files_from_zip(zip_file, target_files):
    
    #Conectamos con FTPS
    ftps=connect_ftps()
    arrayDF=[]


    try:
        # Descarga el archivo zip en memoria
        with io.BytesIO() as zip_data:
            ftps.retrbinary('RETR ' + zip_file, zip_data.write)
            zip_data.seek(0)  # Reinicia el puntero al inicio del buffer
                
            # Descomprime el archivo zip en memoria
            with zipfile.ZipFile(zip_data) as z:
                for target_file in target_files:
                    # Verifica si el archivo objetivo existe en el zip
                    if target_file in z.namelist():
                        # Si existe, abre el archivo y lo carga en un DataFrame
                        with z.open(target_file) as target_data:
                            arrayDF.append(pd.read_csv(target_data, sep='\t', header=None))
                            #return pd.read_csv(target_data, sep='\t', header=None)
                    else:
                        # Si no existe, devuelve un mensaje o un DataFrame vacío
                        print(f"El archivo {target_file} no se encontró en el zip.")
                        
                        return pd.DataFrame()  # O puedes devolver None si prefieres
                
                return arrayDF
    except FileNotFoundError:
        # Si el archivo zip no se encuentra, devuelve un mensaje o un DataFrame vacío
        print(f"El archivo zip {zip_file} no se encontró en el servidor FTPS.")
        
        return pd.DataFrame()  # O puedes devolver None si prefieres
        
    except zipfile.BadZipFile:
        # Si el archivo descargado no es un zip válido, maneja el error
        print(f"El archivo {zip_file} no es un archivo zip válido.")
        
        return pd.DataFrame()
        
    except Exception as e:
        #st.error(f"Ocurrió un error: {e}")
        
        return pd.DataFrame()
       
    

# Función para cargar la edad y el lenguaje del usuario
@st.cache_data
def edad_real(usuario_file):
    # Definimos variables
    edad=0
    lang = ""

    #Conectamos con FTPS
    ftps=connect_ftps()
    
    try:
        # Crear un buffer en memoria para almacenar el contenido del archivo
        with io.BytesIO() as data:
            # Descargar el archivo JSON al buffer
            ftps.retrbinary('RETR ' + usuario_file, data.write)
            data.seek(0)  # Volver al inicio del buffer para la lectura

            # Leer el JSON desde el buffer
            json_data = json.load(data)

            # Sacamos la edad real y la devolvemos
            edad = int(json_data["age"])
            lang = str(json_data["lang"])
            
            return edad, lang
            
    except FileNotFoundError:
        st.error("El archivo JSON no se encontró en el servidor FTPS.")
        
        return 30, "en" #Para que no de error si no se carga bien el json
    except json.JSONDecodeError:
        st.error("El archivo JSON tiene un formato inválido.")
        
        return 30, "en" #Para que no de error si no se carga bien el json
    except Exception as e:
        st.error(f"Ocurrió un error al cargar el archivo JSON: {e}")
        
        return 30, "en" #Para que no de error si no se carga bien el json
    

# Función para cargar la última sesión del usuario
@st.cache_data
def ultima_sesion(usuario_file):
    # Definimos las svariables
    seseion=[]
    last_Ses='s1'
    archivo=f'config.json'
  
    #Conectamos con FTPS
    ftps=connect_ftps()

    try:
        # Crear un buffer en memoria para almacenar el contenido del archivo
        with io.BytesIO() as data:
            # Descargar el archivo JSON al buffer
            ftps.retrbinary('RETR ' + usuario_file, data.write)
            data.seek(0)  # Volver al inicio del buffer para la lectura

            # Leer el JSON desde el buffer
            json_data = json.load(data)

            # Sacamos la útlima sesion y la devolvemos
            #edad = int(json_data["age"])
            seseion = json_data["lastSessionsPerformed"]
            last_Ses=seseion[-1]
            
            return last_Ses
            
    except FileNotFoundError:
        st.error("El archivo JSON no se encontró en el servidor FTPS.")
        
        return last_Ses
    except json.JSONDecodeError:
        st.error("El archivo JSON tiene un formato inválido.")
        
        return last_Ses
    except Exception as e:
        st.error(f"Ocurrió un error al cargar el archivo JSON: {e}")
        
        return last_Ses
    
    
# Función para cargar idioma del usuario
@st.cache_data
def get_idioma(usuario_file):
    #Conectamos con FTPS
    ftps=connect_ftps()
    
    try:
        # Crear un buffer en memoria para almacenar el contenido del archivo
        with io.BytesIO() as data:
            # Descargar el archivo JSON al buffer
            ftps.retrbinary('RETR ' + usuario_file, data.write)
            data.seek(0)  # Volver al inicio del buffer para la lectura

            # Leer el JSON desde el buffer
            json_data = json.load(data)

            # Sacamos la edad real y la devolvemos
            idioma = str(json_data["lang"])
            
            
            return idioma
            
    except FileNotFoundError:
        st.error("El archivo JSON no se encontró en el servidor FTPS.")
        
        return None
    except json.JSONDecodeError:
        st.error("El archivo JSON tiene un formato inválido.")
        
        return None
    except Exception as e:
        st.error(f"Ocurrió un error al cargar el archivo JSON: {e}")
        
        return None


# Función para desencriptar el usuario 
def decrypt(ciphertext: str) -> str:

    secret_key = st.secrets["encryption"]["secret_key"]
    try:
        SECRET_KEY=secret_key.encode('utf_8')
        ct = base64.urlsafe_b64decode(ciphertext)
        iv = ct[:AES.block_size]
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct[AES.block_size:]), AES.block_size).decode('utf-8')
        
        return pt
    except Exception as e:
        #st.error(f"Ocurrió un error : {e}")
        return None
