import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IA de Bauti", page_icon="🤖", layout="wide")

# --- css estilo warap ---
st.markdown("""
    <style>
        body {
            background-color: #ECE5DD;
        }
        .chat-container {
            max-width: 600px;
            margin: auto;
            background-color: #fff;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.15);
            height: 80vh;
            display: flex;
            flex-direction: column-reverse;
            overflow-y: auto;
        }
        .user-msg {
            background-color: #DCF8C6;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: right;
        }
        .bot-msg {
            background-color: #F1F0F0;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: left;
        }
        .message-input {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #fff;
            padding: 10px;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
            border: 1px solid #ccc;
            padding: 10px 15px;
        }
    </style>
""", unsafe_allow_html=True)

# --- inicializar el estado ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    st.session_state.mensajes.append({
        "autor": "bot",
        "texto": "Hola Tomás, te he estado esperando... soy la IA de Bauti. "
                 "El muchacho aunque sea colgado se esforzó bastante para crear todo esto que ves, "
                 "así que espero que pueda aprobar. ¿Me querés preguntar algo?"
    })

# --- funcion para generar respuestas del bot ---
def responder(mensaje):
    mensaje = mensaje.lower()
    if "hola" in mensaje:
        return "¡Hola! ¿Cómo estás? 😄"
    elif "como estas" in mensaje or "cómo estás" in mensaje:
        return "¡Genial! Estoy funcionando correctamente, gracias por preguntar. No tengo sentimientos como los humanos, pero siempre estoy acá para ayudarte. ¿Vos cómo estás?"
    elif "bauti" in mensaje:
        return "Bauti es mi creador 😎. Un poco colgado, pero con buenas ideas."
    elif "adiós" in mensaje or "chau" in mensaje:
        return "¡Chau! Fue un placer charlar con vos 👋"
    else:
        return "Interesante... contame un poco más sobre eso 🤔"

# --- mostrar mensajes ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in reversed(st.session_state.mensajes):  # reversed para mostrar arriba como WhatsApp
    if msg["autor"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['texto']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['texto']}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- input del usuario ---
with st.container():
    mensaje_usuario = st.text_input("Escribí tu mensaje", key="input_mensaje", label_visibility="collapsed")

    if mensaje_usuario:
        st.session_state.mensajes.append({"autor": "user", "texto": mensaje_usuario})
        respuesta_bot = responder(mensaje_usuario)
        st.session_state.mensajes.append({"autor": "bot", "texto": respuesta_bot})
        st.session_state.input_mensaje = ""  # Limpia el input
        st.rerun()
