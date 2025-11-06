import streamlit as st
import json
import os
from groq import Groq
import time

st.set_page_config(page_title="IA Bauti Talentotech", page_icon="🤖", layout="wide")
st.title("🤖 IA Bauti Talentotech")

# ========================
# Configuración del cliente
# ========================
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Archivo para persistir historial
HISTORIAL_FILE = "historial_chat.json"

# Cargar historial
if os.path.exists(HISTORIAL_FILE):
    with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
        historial = json.load(f)
else:
    historial = []

def guardar_historial():
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

# ========================
# Estilos CSS para chat
# ========================
st.markdown("""
<style>
/* Contenedor del chat */
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
}

/* Burbujas */
.bubble-user {
    text-align: right;
    background-color: #075E54;
    color: white;
    padding: 10px;
    border-radius: 15px;
    margin: 5px 0;
    max-width: 70%;
    float: right;
    clear: both;
}
.bubble-ia {
    text-align: left;
    background-color: #262626;
    color: white;
    padding: 10px;
    border-radius: 15px;
    margin: 5px 0;
    max-width: 70%;
    float: left;
    clear: both;
}

/* Barra de chat fija abajo */
.input-container {
    position: fixed;
    bottom: 10px;
    width: 95%;
    display: flex;
}
input[type="text"] {
    flex: 1;
    padding: 10px;
    border-radius: 20px;
    border: none;
    background-color: #2C2C2C;
    color: white;
    margin-right: 10px;
}
button {
    background-color: #25D366;
    color: white;
    border-radius: 15px;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ========================
# Mostrar historial
# ========================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in historial:
    if chat["rol"] == "user":
        st.markdown(f'<div class="bubble-user">{chat["mensaje"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-ia">{chat["mensaje"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ========================
# Botón para borrar historial
# ========================
if st.button("🗑 Borrar historial"):
    historial = []
    if os.path.exists(HISTORIAL_FILE):
        os.remove(HISTORIAL_FILE)
    st.experimental_rerun()

# ========================
# Barra de chat
# ========================
st.markdown('<div class="input-container">', unsafe_allow_html=True)
mensaje = st.text_input("", key="mensaje_input", placeholder="Escribí tu mensaje y presioná Enter")
enviar = st.button("Enviar")
st.markdown('</div>', unsafe_allow_html=True)

# ========================
# Procesar mensaje
# ========================
if mensaje:
    historial.append({"rol": "user", "mensaje": mensaje})
    guardar_historial()
    
    # Contenedor temporal para mostrar "pensando"
    ia_placeholder = st.empty()
    ia_placeholder.markdown('<div class="bubble-ia">💬 La super IA de Bauti está pensando...</div>', unsafe_allow_html=True)
    st.experimental_rerun()  # Esto solo refresca la barra de chat (seguro ahora que está fuera del flujo principal)

# ========================
# Generar respuesta de la IA
# ========================
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
        ia_placeholder.markdown(f'<div class="bubble-ia">{ia_mensaje}</div>', unsafe_allow_html=True)
    except Exception as e:
        ia_placeholder.error(f"❌ Error al generar respuesta: {e}")
