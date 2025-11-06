import streamlit as st
import json
import os
from groq import Groq
import time

st.set_page_config(page_title="IA Bauti Talentotech", page_icon="🤖", layout="centered")
st.title("🤖 IA Bauti Talentotech")

api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

HISTORIAL_FILE = "historial_chat.json"

if os.path.exists(HISTORIAL_FILE):
    with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
        historial = json.load(f)
else:
    historial = []

def guardar_historial():
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

# Barra de chat
mensaje = st.text_input("Escribí tu mensaje y presioná Enter:")

# Botón para borrar historial
if st.button("🗑 Borrar historial"):
    historial = []
    if os.path.exists(HISTORIAL_FILE):
        os.remove(HISTORIAL_FILE)
    st.experimental_rerun()

# Contenedor para la respuesta de la IA
ia_placeholder = st.empty()

# Procesar mensaje del usuario
if mensaje:
    historial.append({"rol": "user", "mensaje": mensaje})
    guardar_historial()
    
    # Mostrar "pensando" temporal
    ia_placeholder.markdown('<div class="bubble-ia">💬 La super IA de Bauti está pensando...</div>', unsafe_allow_html=True)
    st.session_state["ultima_consulta"] = mensaje

    # Generar respuesta de la IA
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

        # Reemplazar el "pensando" por la respuesta final
        ia_placeholder.markdown(f'<div class="bubble-ia">{ia_mensaje}</div>', unsafe_allow_html=True)
    except Exception as e:
        ia_placeholder.error(f"❌ Error al generar respuesta: {e}")

# Mostrar historial completo
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in historial:
    if chat["rol"] == "user":
        st.markdown(f'<div class="bubble-user">{chat["mensaje"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-ia">{chat["mensaje"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
