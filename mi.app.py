import streamlit as st
from groq import Groq

st.title("🤖 IA Bauti Talentotech")

# ✅ Cargar la API key desde los secrets de Streamlit
api_key = st.secrets["GROQ_API_KEY"]

# Inicializar cliente de Groq
client = Groq(api_key=api_key)

# Interfaz
pregunta = st.text_area("🗣 Escribí tu pregunta para la IA:")

if st.button("Responder"):
    if pregunta.strip():
        st.write("💬 Generando respuesta...")

        try:
            # Ejemplo de uso con el modelo de Groq
            respuesta = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Sos una IA amable y útil creada por Bauti."},
                    {"role": "user", "content": pregunta},
                ],
            )

            st.success("🧠 Respuesta:")
            st.write(respuesta.choices[0].message.content)

        except Exception as e:
            st.error(f"❌ Error al generar respuesta: {e}")
    else:
        st.warning("Por favor escribí una pregunta antes de presionar 'Responder'.")
