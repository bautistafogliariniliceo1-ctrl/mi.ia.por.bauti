import streamlit as st
import openai

st.set_page_config(page_title="IA de Bauti", page_icon="🤖", layout="wide")

# --- estilo tipo warap ---
st.markdown("""
<style>
body, .main {
    background-color: #111B21;
    color: white;
    padding-bottom: 100px; /* espacio para input fijo */
}
.user-msg {
    background-color: #005C4B;
    color: white;
    padding: 10px 14px;
    border-radius: 10px 10px 0 10px;
    margin: 5px 0;
    max-width: 75%;
    align-self: flex-end;
    word-wrap: break-word;
}
.bot-msg {
    background-color: #202C33;
    color: #E9EDEF;
    padding: 10px 14px;
    border-radius: 10px 10px 10px 0;
    margin: 5px 0;
    max-width: 75%;
    align-self: flex-start;
    word-wrap: break-word;
}
.message-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #202C33;
    padding: 12px;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
}
.stTextInput>div>div>input {
    background-color: #2A3942;
    color: white;
    border-radius: 20px;
    border: none;
    padding: 10px 15px;
    width: 80%;
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

# --- API Key OpenAI ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- historial ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"autor": "bot", "texto": "Hola Tomás, te he estado esperando... soy la IA de Bauti. El muchacho aunque sea colgado se esforzó bastante para crear todo esto que ves, así que espero que pueda aprobar. ¿Me querés preguntar algo?"}
    ]

# --- funcion para generar respuesta automática ---
def generar_respuesta(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # o "gpt-4"
            messages=[
                {"role": "system", "content": "Sos la IA de Bauti. Respondé natural, con humor, onda de amigo, no aburrido."},
                *[
                    {"role": "user" if m["autor"]=="user" else "assistant", "content": m["texto"]}
                    for m in st.session_state.mensajes
                ],
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# --- motrar chat ---
for msg in st.session_state.mensajes:
    clase = "user-msg" if msg["autor"] == "user" else "bot-msg"
    st.markdown(f"<div class='{clase}'>{msg['texto']}</div>", unsafe_allow_html=True)

# --- barra de input ---
st.markdown('<div class="message-input">', unsafe_allow_html=True)
with st.form("form_chat", clear_on_submit=True):
    mensaje = st.text_input("Escribí tu mensaje", label_visibility="collapsed")
    enviar = st.form_submit_button("Enviar")
    if enviar and mensaje.strip():
        st.session_state.mensajes.append({"autor": "user", "texto": mensaje})
        respuesta = generar_respuesta(mensaje)
        st.session_state.mensajes.append({"autor": "bot", "texto": respuesta})
        st.experimental_rerun()
st.markdown('</div>', unsafe_allow_html=True)
