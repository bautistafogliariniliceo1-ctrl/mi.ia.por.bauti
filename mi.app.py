import streamlit as st

st.set_page_config(page_title="IA de Bauti", page_icon="🤖", layout="wide")

# --- css estilo warap ---
st.markdown("""
    <style>
        body {
            background-color: #ECE5DD;
        }
        .main {
            background-color: #ECE5DD;
        }
        .chat-box {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 15px;
            max-width: 600px;
            margin: 0 auto;
            height: 80vh;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }
        .user-msg {
            background-color: #DCF8C6;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            align-self: flex-end;
            max-width: 80%;
            text-align: right;
        }
        .bot-msg {
            background-color: #F1F0F0;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            align-self: flex-start;
            max-width: 80%;
            text-align: left;
        }
        .message-input {
            background-color: #ffffff;
            padding: 10px;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
            border: 1px solid #ccc;
            padding: 10px 15px;
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
        return "¡Genial! Estoy funcionando correctamente, gracias por preguntar. No tengo sentimientos como los humanos, pero siempre estoy acá para ayudarte. ¿Vos cómo estás?"
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

# --- input y botón de envío ---
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
