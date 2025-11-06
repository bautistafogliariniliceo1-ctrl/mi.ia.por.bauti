import streamlit as st
import openai

# Configuración general
st.set_page_config(page_title="IA de Bauti", page_icon="🤖", layout="centered")

# --- Estilos visuales tipo ChatGPT ---
st.markdown("""
<style>
body, .main {
    background-color: #121212;
    color: #EAEAEA;
    font-family: 'Inter', sans-serif;
}

.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding-bottom: 120px;
}

.message {
    padding: 12px 18px;
    border-radius: 12px;
    max-width: 80%;
    line-height: 1.5;
    white-space: pre-wrap;
    word-wrap: break-word;
    animation: fadeIn 0.4s ease-in-out;
}

.user {
    align-self: flex-end;
    background: #005C4B;
    color: white;
}

.bot {
    align-self: flex-start;
    background: #1E1E1E;
    color: #EAEAEA;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(5px);}
    to {opacity: 1; transform: translateY(0);}
}

.input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #1E1E1E;
    padding: 15px 20px;
    border-top: 1px solid #2F2F2F;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.stTextInput > div > div > input {
    background-color: #2A2A2A;
    color: white;
    border-radius: 20px;
    border: none;
    padding: 10px 15px;
    width: 100%;
}

.stTextInput > div > div > input:focus {
    outline: none !important;
    border: 1px solid #00A884;
}

.stButton > button {
    background-color: #00A884;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 18px;
    cursor: pointer;
}

.stButton > button:hover {
    background-color: #029E79;
}
</style>
""", unsafe_allow_html=True)

# --- Configuración OpenAI ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Inicializar historial ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"autor": "bot", "texto": "Hola Tomás 👋, soy la IA de Bauti. Me alegra que estés acá, el muchacho se rompió el alma programando esto. ¿Querés charlar conmigo?"}
    ]

# --- Función para generar respuesta ---
def generar_respuesta(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sos la IA de Bauti. Respondé como una IA cercana, amigable y natural, con el estilo de ChatGPT pero más relajada."},
                *[
                    {"role": "user" if m["autor"] == "user" else "assistant", "content": m["texto"]}
                    for m in st.session_state.mensajes
                ],
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ups, hubo un error: {e}"

# --- Mostrar mensajes ---
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.mensajes:
    clase = "user" if msg["autor"] == "user" else "bot"
    st.markdown(f"<div class='message {clase}'>{msg['texto']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Input de mensaje ---
st.markdown('<div class="input-container">', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    mensaje = st.text_input("Escribí algo...", label_visibility="collapsed")
    enviar = st.form_submit_button("Enviar")
    if enviar and mensaje.strip():
        st.session_state.mensajes.append({"autor": "user", "texto": mensaje})
        respuesta = generar_respuesta(mensaje)
        st.session_state.mensajes.append({"autor": "bot", "texto": respuesta})
        st.experimental_rerun()
st.markdown("</div>", unsafe_allow_html=True)
