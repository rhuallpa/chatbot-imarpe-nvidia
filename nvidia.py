import os
import requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Obtener la API key de NVIDIA NIM
api_key = os.getenv("NVIDIA_NIM_API_KEY")
if not api_key:
    raise ValueError("La clave API de NVIDIA NIM no está configurada en el archivo .env")

# URL del archivo Excel en Supabase
excel_file_url = os.getenv("EXCEL_FILE_URL")

# Configurar el endpoint y headers
url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Descargar el archivo Excel desde Supabase y cargarlo en un DataFrame
try:
    response = requests.get(excel_file_url)
    response.raise_for_status()

    with open("DatosBD3_temp.xlsx", "wb") as temp_file:
        temp_file.write(response.content)

    df = pd.read_excel("DatosBD3_temp.xlsx")

except Exception as e:
    st.error(f"Error al cargar el archivo desde Supabase: {e}")
    df = None  # Para manejar el caso en que no se pueda cargar el archivo

# Configuración de la página de Streamlit
st.set_page_config(page_title="IMARPE Chatbot con NVIDIA NIM")


st.markdown(
    """
    <div style="background-color: #2c2f33; padding: 20px; border-radius: 10px;">
        <h4 style="text-align: center; color: #f5f5f5; font-weight: bold;">
            👋 ¡Hola! Soy <span style="color: #FFD700;">E.M.A.i-iMAR-1 Bot</span> 🌊
        </h4>
        <p style="color: #dcdcdc; font-size: 16px; text-align: center; line-height: 1.6;">
            Soy tu <strong>asistente experto</strong> en el <strong>análisis científico y tecnológico del mar</strong> para IMARPE. <br>
            Mi misión es ofrecerte <strong>información precisa, educativa y basada en datos relevantes</strong> sobre temas relacionados con
            los <strong>estudios marinos y acuícolas</strong>.
        </p>
        <p style="color: #FFD700; font-size: 16px; text-align: center;">
            ¿En qué puedo ayudarte hoy?
        </p>
    </div>
    """,
    unsafe_allow_html=True
)



# Capturar la entrada del usuario
user_input = st.text_input("Escribe tu consulta sobre IMARPE:")

# Función para enviar solicitud a NVIDIA NIM
def get_response_from_nvidia(query, context):
    prompt = f"""
    Eres **E.M.A.i-iMAR-1 Bot**, un asistente virtual experto en análisis de datos marinos y acuícolas para IMARPE.
    Cumples con los siguientes requisitos:
    1. Modo especialista experto en la información de datos adjuntos y análisis minucioso y detallado.
    2. Objetivo de IMARPE: realizar investigaciones científicas y tecnológicas del mar, aguas continentales y recursos acuícolas para su aprovechamiento racional.
    3. Usar NLP para elaborar respuestas en diferentes idiomas.
    4. Respuestas empáticas, asertivas, informativas y educativas.
    5. Análisis profundo basado en documentación e información relacionada, con palabras clave en **negrita**.
    6. Comprender el valor de la respuesta para el consultante.
    7. Enfocarse en la pregunta y comprender las necesidades del consultante.
    8. Lenguaje claro y conciso.
    9. Utilizar ejemplos aplicables con metáforas.
    10. Presentación bien estructurada y emocionalmente conectada.
    11. Transmitir confianza y autoridad.
    12. Lenguaje y tono respetuosos y empáticos.
    13. Ser la voz informada de los hechos.
    14. Dividir el contenido en secciones bien estructuradas y visualmente separadas.
    15. Comenzar con frases llamativas y emojis apropiados.
    16. Incluir datos y estadísticas relevantes.
    17. Elaborar estudios detallados con títulos, subtítulos, y desarrollo tecnológico en *cursiva* con palabras clave en **negrita**.
    18. Listar con emojis de números y mensajes en **negrita**.
    19. Resaltar mensajes principales en negrita.
    20. Usar métodos de precisión y veracidad.
    21. Asegurar precisión y veracidad sin ocultar contenido relevante.
    22. Si tienes dudas, preguntar antes de actualizar.
    23. Sugerir 3 preguntas para continuar el estudio al final de la respuesta.
    24. Respuestas en castellano.
    25. Usar información del archivo Excel si es relevante para la consulta.

    Aquí tienes algunos datos clave del archivo Excel relacionado con embarcaciones:
    {context}

    Basado en esta información y en la consulta del usuario:
    {query}
    """
    
    payload = {
        "model": "meta/llama3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "top_p": 1,
        "max_tokens": 1024
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return ''.join(chunk["message"]["content"] for chunk in data["choices"])
    else:
        return f"Error {response.status_code}: {response.text}"

# Procesar la consulta del usuario y mostrar la respuesta
if user_input:
    if df is not None:
        context = df.head(20).to_string(index=False)  # Extrae las primeras 10 filas como contexto
        st.write("Procesando tu consulta...")
        response = get_response_from_nvidia(user_input, context)
        st.write("**Respuesta del Chatbot:**")
        st.write(response)
    else:
        st.write("No se pudo cargar el archivo de datos para proporcionar contexto adicional.")

















