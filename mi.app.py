import streamlit as st
import json
import os
from groq import Groq

st.set_page_config(page_title="IA Bauti Talentotech", page_icon="🤖", layout="centered")
st.title("🤖 IA Bauti Talentotech")

# ✅ Cargar API key
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Archivo para persistir el historial
HISTORIAL_FILE = "historial_chat.json"

# Cargar historial si existe
if os.path.exists(HISTORIAL_FILE):
    with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
        historial = json.load(f)
else:
    historial = []

# Función para guardar historial
def guardar_historial():
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

# Input de usuario
st.markdown(
    """
    <style>
    .stTextInput>div>div>input {
        background-color: #2C2C2C;
        color: #FFFFFF;
        border-radius: 20px;
        padding: 10px;
        border: none;
    }
    .stButton>button {
        background-color: #25D366;
        color: white;
        border-radius: 10px;
        width: 100%;
    }
    .bubble-user {
        text-align: right;
        background-color: #075E54;
        color: white;
        padding: 10px;
        border-radius: 15px;
        margin: 5px 0;
    }
    .bubble-ia {
        text-align: left;
        background-color: #262626;
        color: white;
        padding: 10px;
        border-radius: 15px;
        margin: 5px 0;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: scroll;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Barra de chat
mensaje = st.text_input("Escribí tu mensaje y presioná Enter:")

# Botón para borrar historial
if st.button("🗑 Borrar historial"):
    historial = []
    if os.path.exists(HISTORIAL_FILE):
        os.remove(HISTORIAL_FILE)
    st.experimental_rerun()

# Procesar mensaje
if mensaje:
    historial.append({"rol": "user", "mensaje": mensaje})
    guardar_historial()
    
    st.markdown('<div class="bubble-ia">💬 La super IA de Bauti está pensando...</div>', unsafe_allow_html=True)
    st.experimental_rerun()  # Refresca para mostrar "pensando"

# Generar respuesta de la IA
if historial and historial[-1]["rol"] == "user":
    try:
        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Sos una IA amable y útil creada por Bauti."},
                *[
                    {"role": item["rol"], "content": item["mensaje"]}
                    for item in historial
                ]
            ],
        )
        ia_mensaje = respuesta.choices[0].message.content
        historial.append({"rol": "assistant", "mensaje": ia_mensaje})
        guardar_historial()
        st.experimental_rerun()  # Refresca para mostrar respuesta
    except Exception as e:
        st.error(f"❌ Error al generar respuesta: {e}")

# Mostrar historial
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in historial:
    if chat["rol"] == "user":
        st.markdown(f'<div class="bubble-user">{chat["mensaje"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-ia">{chat["mensaje"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

