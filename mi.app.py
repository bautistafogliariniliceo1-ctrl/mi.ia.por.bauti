import streamlit as st
from groq import Groq

st.set_page_config(page_title="IA de Bauti", layout="wide")

st.markdown("""
    <style>
    body {background-color: #0e1117; color: white;}
    .chat-bubble-user {
        background-color: #005c4b; padding: 10px 15px; border-radius: 15px;
        margin: 5px; max-width: 70%; align-self: flex-end; color: white;
    }
    .chat-bubble-bot {
        background-color: #202c33; padding: 10px 15px; border-radius: 15px;
        margin: 5px; max-width: 70%; align-self: flex-start; color: white;
    }
    .chat-container {
        display: flex; flex-direction: column; height: 80vh;
        overflow-y: auto; padding: 10px; border-radius: 10px;
    }
    .input-bar {
        position: fixed; bottom: 0; left: 0; right: 0;
        background-color: #0e1117; padding: 10px; border-top: 1px solid #333;
    }
    textarea, input {background-color: #202c33 !important; color: white !important; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# Inicializar sesión y cliente
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "assistant", "content": "Hola Tomás, te he estado esperando... soy la IA de Bauti. El muchacho aunque sea colgado se esforzó bastante para crear todo esto que ves, así que espero que pueda aprobar. ¿Me querés preguntar algo?"}
    ]

# Contenedor del chat
chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.mensajes:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-bot'>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Barra de entrada
with st.container():
    with st.form(key="form", clear_on_submit=True):
        pregunta = st.text_input("Escribí tu mensaje...", key="input_msg")
        enviar = st.form_submit_button("Enviar")

if enviar and pregunta.strip():
    st.session_state.mensajes.append({"role": "user", "content": pregunta})

    st.markdown("<div class='chat-bubble-bot'>La Super IA de Bauti está pensando...</div>", unsafe_allow_html=True)

    respuesta_completa = ""
    placeholder = st.empty()

    with client.chat.completions.stream(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Sos una IA amable, natural y un poco graciosa creada por Bauti."},
            *st.session_state.mensajes,
        ],
    ) as stream:
        for event in stream:
            if event.type == "message.delta" and event.delta.content:
                respuesta_completa += event.delta.content
                placeholder.markdown(f"<div class='chat-bubble-bot'>{respuesta_completa}</div>", unsafe_allow_html=True)

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta_completa})
    st.rerun()
