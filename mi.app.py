import streamlit as st

st.set_page_config(page_title="IA de Bauti", page_icon="🤖", layout="wide")

# --- css oscuro tipo warap ---
st.markdown("""
    <style>
        body, .main {
            background-color: #111B21;
            color: white;
        }
        .chat-box {
            background-color: #0B141A;
            border-radius: 12px;
            padding: 15px;
            max-width: 600px;
            margin: 0 auto;
            height: 80vh;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.4);
        }
        .user-msg {
            background-color: #005C4B;
            color: white;
            padding: 10px 14px;
            border-radius: 10px 10px 0px 10px;
            margin: 5px 0;
            align-self: flex-end;
            max-width: 75%;
            word-wrap: break-word;
        }
        .bot-msg {
            background-color: #202C33;
            color: #E9EDEF;
            padding: 10px 14px;
            border-radius: 10px 10px 10px 0px;
            margin: 5px 0;
            align-self: flex-start;
            max-width: 75%;
            word-wrap: break-word;
        }
        .message-input {
            background-color: #202C33;
            padding: 12px;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
        }
        .stTextInput>div>div>input {
            background-color: #2A3942;
            color: white;
            border-radius: 20px;
            border: none;
            padding: 10px 15px;
        }
        .stTextInput>div>div>input:focus {
            outline: none !important;
            border: 1px solid #00A884;
        }
        .stButton>button {
            background-color: #00A884;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 8px 18px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #029E79;
        }
    </style>
""", unsafe_allow_html=True)

# --- estado inicial ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "autor": "bot",
            "texto": (
                "Hola Tomás, te he estado esperando... soy la IA de Bauti. "
                "El muchacho aunque sea colgado se esforzó bastante para crear todo esto que ves, "
                "así que espero que pueda aprobar. ¿Me querés preguntar algo?"
            )
        }
    ]

# --- funcion para generar respuestas ---
def responder(mensaje):
    msg = mensaje.lower()
    if "hola" in msg:
        return "¡Hola! ¿Cómo estás? 😄"
    elif "como estas" in msg or "cómo estás" in msg:
        return "Estoy bien, gracias por preguntar 😌 ¿y vos?"
    elif "bauti" in msg:
        return "Bauti es mi creador 😎. Un poco colgado, pero con buenas ideas."
    elif "adiós" in msg or "chau" in msg:
        return "¡Chau! Fue un placer charlar con vos 👋"
    else:
        return "Interesante... contame un poco más sobre eso 🤔"

# --- mostrar el chat ---
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
for msg in st.session_state.mensajes:
    if msg["autor"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['texto']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['texto']}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- input y botón ---
st.markdown('<div class="message-input">', unsafe_allow_html=True)
with st.form(key="formulario_chat", clear_on_submit=True):
    mensaje_usuario = st.text_input("Escribí tu mensaje", label_visibility="collapsed")
    enviar = st.form_submit_button("Enviar")

    if enviar and mensaje_usuario.strip():
        st.session_state.mensajes.append({"autor": "user", "texto": mensaje_usuario})
        respuesta = responder(mensaje_usuario)
        st.session_state.mensajes.append({"autor": "bot", "texto": respuesta})
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
