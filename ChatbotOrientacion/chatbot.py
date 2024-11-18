import streamlit as st
from test import generar_preguntas_iniciales

def mostrar_chat(usuario):
    """
    Muestra la interfaz del chat y maneja la interacción con el usuario.
    """
    st.title("Chat con IA")
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = {}

    # Bienvenida e introducción (solo al inicio)
    if "inicio_chat" not in st.session_state:
        st.session_state.inicio_chat = True
        with st.chat_message("assistant"):
            st.write(f"¡Hola {usuario['nombre']}! Bienvenido/a al Chat de Orientación Vocacional.")
            st.write("Este chat te ayudará a explorar tus intereses, habilidades y personalidad para que puedas descubrir posibles carreras que se ajusten a tu perfil.")
            st.write("Para comenzar, te haré algunas preguntas. ¿Estás listo/a para empezar?")

        # Esperar la confirmación del usuario
        if st.button("Sí, estoy listo/a"):
            st.session_state.inicio_chat = False
            st.session_state.respuestas = {}  # Inicializar el diccionario de respuestas
            st.rerun()  # Recargar la página para mostrar las preguntas
        else:
            return  # Salir de la función si el usuario no está listo

    # Inicializar el historial del chat y el índice de la pregunta actual
    if "historial" not in st.session_state:
        st.session_state.historial = []
    if "indice_pregunta" not in st.session_state:
        st.session_state.indice_pregunta = 0

    # Generar preguntas iniciales (solo si no se han generado)
    if "preguntas_actuales" not in st.session_state:
        st.session_state.preguntas_actuales = generar_preguntas_iniciales()

    # Mostrar las preguntas al usuario
    if st.session_state.indice_pregunta < len(st.session_state.preguntas_actuales):
        pregunta_actual = st.session_state.preguntas_actuales[st.session_state.indice_pregunta]
        st.write(pregunta_actual["text"])  # Mostrar la pregunta

        # Mostrar las opciones de respuesta según el tipo de test
        if pregunta_actual.get("opciones"):
            respuesta = st.radio("Selecciona tu respuesta:", pregunta_actual["opciones"], key=pregunta_actual["id"])
        else:
            respuesta = st.text_input("Escribe tu respuesta:", key=pregunta_actual["id"])

        # Guardar la respuesta en el diccionario de respuestas
        st.session_state.respuestas[pregunta_actual["id"]] = respuesta

        # Incrementar el índice de la pregunta y actualizar la página
        st.session_state.indice_pregunta += 1
        st.rerun()

    # Mostrar el historial del chat
    for i in range(st.session_state.indice_pregunta):
        pregunta = st.session_state.preguntas_actuales[i]
        respuesta = st.session_state.respuestas.get(pregunta["id"])
        if respuesta:
            with st.chat_message("user"):
                st.write(f"Pregunta: {pregunta['text']}")
                st.write(f"Respuesta: {respuesta}")

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
        respuesta_bot = generar_respuesta(mensaje_usuario, usuario)
        st.session_state.historial.append({"rol": "assistant", "contenido": respuesta_bot})

def generar_respuesta(mensaje, usuario):
    return "Hola, estoy aprendiendo a responder preguntas. Pronto podré ayudarte mejor."