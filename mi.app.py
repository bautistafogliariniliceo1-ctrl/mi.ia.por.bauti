import streamlit as st
from groq import Groq

# Configuración de la página
st.set_page_config(page_title="Bauti IA", page_icon="🤖", layout="centered")

# Inicializar el cliente de Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Encabezado
st.title("🤖 Bauti IA")
st.write("Tu asistente inteligente creado con Groq 🚀")

# Inicializar el historial del chat en session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribí algo..."):
    # Mostrar mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generar respuesta de la IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
    # Guardar respuesta
    st.session_state.messages.append({"role": "assistant", "content": reply})
