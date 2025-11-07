import streamlit as st
from groq import Groq

# configuración de la página
st.set_page_config(page_title="Bauti IA", page_icon="🤖", layout="centered")

# inicializar el cliente de Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# encabezado
st.title("🤖 Bauti IA")
st.markdown("Tu asistente inteligente creado con Groq 🚀")

# inicializar historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hola Tomás, te he estado esperando... soy la IA de Bauti. "
                "El muchacho, aunque sea colgado, se esforzó bastante para crear todo esto que ves, "
                "así que espero que pueda aprobar 😄. ¿Me querés preguntar algo?"
            )
        }
    ]

# mostrar los mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# entrada del usuario
if prompt := st.chat_input("Escribí algo..."):
    # mostrar mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # generar respuesta con Groq
    try:
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    temperature=0.8,
                    max_tokens=512,
                )
                reply = response.choices[0].message.content.strip()
                st.markdown(reply)

        # guardar respuesta
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"⚠️ Error al generar respuesta: {e}")
