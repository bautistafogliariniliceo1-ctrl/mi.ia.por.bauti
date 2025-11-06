import streamlit as st
from groq import Groq
import os

st.title("IA Bauti Talentotech 🧠")

api_key = st.text_input("🔑 Ingresá tu API Key de Groq", type="password")

if api_key:
    client = Groq(api_key=api_key)
    st.success("✅ API Key cargada correctamente.")
else:
    st.warning("Esperando tu API Key...")

pregunta = st.text_area("🗣 Escribí tu pregunta para la IA:")
if st.button("Responder"):
    if not api_key:
        st.error("Por favor ingresá tu API Key primero.")
    elif pregunta.strip():
        st.write("Generando respuesta...")
        # Aquí iría tu llamada real al modelo
        st.info("Simulando respuesta: la IA diría algo inteligente 😉")

