import json
import os
import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from test import generar_preguntas_iniciales
from funciones_chat import cargar_datos_usuario, guardar_respuestas, cargar_datos_tests, buscar_id_pregunta


def mostrar_chat(usuario):
    """
    Muestra la interfaz del chat y maneja la interacción con el usuario.
    """
    st.title("Chat con IA")

    # Inicializar variables de sesión si no existen
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = {}
    if 'inicio_chat' not in st.session_state:
        st.session_state.inicio_chat = True
    if 'preguntas_actuales' not in st.session_state:
        st.session_state.preguntas_actuales = generar_preguntas_iniciales()
    if 'indice_pregunta' not in st.session_state:
        st.session_state.indice_pregunta = 0

    # Bienvenida e introducción (solo al inicio)
    if st.session_state.inicio_chat:
        with st.chat_message("assistant"):
            st.write(f"¡Hola {usuario['nombre']}! Bienvenido/a al Chat de Orientación Vocacional.")
            st.write("Este chat te ayudará a explorar tus intereses, habilidades y personalidad para que puedas descubrir posibles carreras que se ajusten a tu perfil.")
            st.write("Para comenzar, te haré algunas preguntas. ¿Estás listo/a para empezar?")

        if st.button("Sí, estoy listo/a"):
            st.session_state.inicio_chat = False
        else:
            return  # Salir de la función si el usuario no está listo

    # Mostrar la pregunta actual solo si no se ha respondido
    if st.session_state.indice_pregunta < len(st.session_state.preguntas_actuales):
        pregunta_actual = st.session_state.preguntas_actuales[st.session_state.indice_pregunta]
        if pregunta_actual["id"] not in st.session_state.respuestas:  # Verificar si ya se ha respondido
            with st.chat_message("assistant"):
                st.write(pregunta_actual["text"])

            # Mostrar opciones de respuesta o campo de texto
            if pregunta_actual.get("opciones"):
                with st.form(key=f"pregunta_{st.session_state.indice_pregunta}"):
                    respuesta = st.radio("Selecciona tu respuesta:", pregunta_actual["opciones"], index=None)
                    submitted = st.form_submit_button("Enviar")
                    if submitted:
                        st.session_state.respuestas[pregunta_actual["id"]] = respuesta
                        st.session_state.indice_pregunta += 1
            else:
                # Usar un formulario para el input de texto
                with st.form(key=f"pregunta_{st.session_state.indice_pregunta}"):
                    respuesta = st.text_input("Escribe tu respuesta:")
                    submitted = st.form_submit_button("Enviar")
                    if submitted:
                        st.session_state.respuestas[pregunta_actual["id"]] = respuesta
                        st.session_state.indice_pregunta += 1
        else:
            # Si ya se respondió, pasar a la siguiente pregunta
            st.session_state.indice_pregunta += 1

    # Mostrar el historial de la conversación
    for i in range(st.session_state.indice_pregunta):
        pregunta = st.session_state.preguntas_actuales[i]
        respuesta = st.session_state.respuestas.get(pregunta["id"])
        if respuesta:
            with st.chat_message("assistant"):  # Pregunta del asistente
                st.write(pregunta["text"])
            with st.chat_message("user"):  # Respuesta del usuario
                st.write(respuesta)

    if "historial" not in st.session_state:
        st.session_state.historial = []
    for mensaje in st.session_state.historial:
        if mensaje["rol"] == "user":
            with st.chat_message("user"):
                st.write(f"{usuario['nombre']} {usuario['apellidos']}: {mensaje['contenido']}")
        else:
            with st.chat_message("assistant"):
                st.write(mensaje["contenido"])
    mensaje_usuario = st.chat_input("Escribe tu mensaje aquí")

    if mensaje_usuario:
        st.session_state.historial.append({"rol": "user", "contenido": mensaje_usuario})
        sentimiento = analizar_sentimiento(mensaje_usuario)
        print(f"Sentimiento del usuario: {sentimiento}")
        respuesta_bot = generar_respuesta(mensaje_usuario, usuario, sentimiento)
        st.session_state.historial.append({"rol": "assistant", "contenido": respuesta_bot})

        respuestas = {
                "usuario": usuario,
                "respuestas_tests": st.session_state.respuestas,
                "historial_chat": st.session_state.historial
            }
        guardar_respuestas(usuario, respuestas)

def generar_respuesta(mensaje, usuario, sentimiento=None):
    """
    Genera una respuesta del chatbot basada en la información del usuario.
    """
    datos_usuario = cargar_datos_usuario(usuario['nombre'])
    
    if datos_usuario:
        datos_tests = cargar_datos_tests() 
        id_pregunta = buscar_id_pregunta(mensaje, datos_tests)
        if id_pregunta:
            respuesta_test = datos_usuario['respuestas_tests'].get(id_pregunta)
            if respuesta_test:
                return f"Respondiste '{respuesta_test}' a esa pregunta."
            else:
                return "No encontré tu respuesta para esa pregunta."
        else:
            return "No entiendo tu pregunta. ¿Podrías reformularla?"
    else:
        return "No se encontraron tus datos."


def analizar_sentimiento(texto):
  """
  Analiza el sentimiento de un texto usando VADER.
  """
  analyzer = SentimentIntensityAnalyzer()
  puntajes = analyzer.polarity_scores(texto)
  # Clasificar el sentimiento como positivo, negativo o neutral
  if puntajes['compound'] >= 0.05:
    sentimiento = 'positivo'
  elif puntajes['compound'] <= -0.05:
    sentimiento = 'negativo'
  else:
    sentimiento = 'neutral'
  return sentimiento