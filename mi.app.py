import streamlit as st
from groq import Groq

st.set_page_config(page_title="IA Bauti Talentotech", page_icon="🤖", layout="wide")
st.title("🤖 IA Bauti Talentotech")

api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# historial de la sesión y mensaje inicial de la IA
if "historial" not in st.session_state:
    st.session_state.historial = [
        {"rol": "assistant", "mensaje": "Hola Tomás, te he estado esperando... soy la IA de Bauti. El muchacho aunque sea colgado se esforzó bastante para crear todo esto que ves, así que espero que pueda aprobar. ¿Me querés preguntar algo?"}
    ]

# estilos tipo warap
st.markdown("""
<style>
.chat-contenedor {
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
}
.burbuja-yo {
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
.burbuja-ia {
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
.input-contenedor {
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

# mostrar historial arriba de la barra
st.markdown('<div class="chat-contenedor">', unsafe_allow_html=True)
for chat in st.session_state.historial:
    if chat["rol"] == "user":
        st.markdown(f'<div class="burbuja-yo">{chat["mensaje"]}</div>', unsafe_allow_html=True)
    else:
        mensaje_limpio = chat["mensaje"].strip("*")
        st.markdown(f'<div class="burbuja-ia">{mensaje_limpio}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# barra de chat (input limpio cada vez)
st.markdown('<div class="input-contenedor">', unsafe_allow_html=True)
mensaje_input = st.text_input("", key="mensaje_input", placeholder="Escribí tu mensaje y presioná Enter", value="")
enviar = st.button("Enviar")
st.markdown('</div>', unsafe_allow_html=True)

# procesar mensaje del usuario
if mensaje_input:
    st.session_state.historial.append({"rol": "user", "mensaje": mensaje_input})
    
    placeholder = st.empty()
    placeholder.markdown('<div class="burbuja-ia">💬 La super IA de Bauti está pensando...</div>', unsafe_allow_html=True)

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Sos buena onda y útil."}] +
                     [{"role": h["rol"], "content": h["mensaje"]} for h in st.session_state.historial]
        )
        ia_msg = resp.choices[0].message.content.strip("*")
        st.session_state.historial.append({"rol": "assistant", "mensaje": ia_msg})
        placeholder.markdown(f'<div class="burbuja-ia">{ia_msg}</div>', unsafe_allow_html=True)
    except Exception as e:
        placeholder.error(f"Error: {e}")

    # el input se limpia usando value="" al recargar
    st.experimental_rerun()  # esta es segura aquí porque ya terminó el ciclo
