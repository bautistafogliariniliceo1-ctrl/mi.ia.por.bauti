import streamlit as st
import json
import os
from groq import Groq

st.set_page_config(page_title="IA Bauti Talentotech", page_icon="🤖", layout="wide")
st.title("🤖 IA Bauti Talentotech")

api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

archivo_historial = "historial_chat.json"

if os.path.exists(archivo_historial):
    with open(archivo_historial, "r", encoding="utf-8") as f:
        historial = json.load(f)
else:
    historial = []

def guardar():
    with open(archivo_historial, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

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

st.markdown('<div class="chat-contenedor">', unsafe_allow_html=True)
for chat in historial:
    if chat["rol"] == "user":
        st.markdown(f'<div class="burbuja-yo">{chat["mensaje"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="burbuja-ia">{chat["mensaje"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🗑 Borrar historial"):
    historial = []
    if os.path.exists(archivo_historial):
        os.remove(archivo_historial)
    st.experimental_rerun()

st.markdown('<div class="input-contenedor">', unsafe_allow_html=True)
mensaje = st.text_input("", key="mensaje_input", placeholder="Escribí tu mensaje y presioná Enter")
enviar = st.button("Enviar")
st.markdown('</div>', unsafe_allow_html=True)

if mensaje:
    historial.append({"rol": "user", "mensaje": mensaje})
    guardar()
    
    placeholder = st.empty()
    placeholder.markdown('<div class="burbuja-ia">💬 La super IA de Bauti está pensando...</div>', unsafe_allow_html=True)

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Sos una IA buena onda y útil."}] +
                     [{"role": h["rol"], "content": h["mensaje"]} for h in historial]
        )
        ia_msg = resp.choices[0].message.content
        historial.append({"rol": "assistant", "mensaje": ia_msg})
        guardar()
        placeholder.markdown(f'<div class="burbuja-ia">{ia_msg}</div>', unsafe_allow_html=True)
    except Exception as e:
        placeholder.error(f"Error: {e}")
