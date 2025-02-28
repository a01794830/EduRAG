import streamlit as st
import logging
from utils.pinecone_utils import search_docs
from utils.embedding_utils import generate_chat_response
import pandas as pd
import os

logger = logging.getLogger(__name__)

def app():
    logger.info("Entrando a Chat educativo")

    st.title("Chat Educativo - Info de Cursos y PDFs")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Muestra el historial
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Pregunta sobre cursos, horarios, PDFs...")

    if user_input:
        st.session_state["messages"].append({"role":"user","content":user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # 1) Data Estructurada (CSV). 
        # Podrías parsear la query y si ve "estudiante S001", etc. 
        # Ej: fallback a "search_docs" para PDFs, y/o genera 
        # un 'synthetic context' con la data tabular. 
        data_context = get_data_context()
        
        # 2) Buscamos en Pinecone
        pinecone_contexts = search_docs(user_input)
        
        # 3) Combine
        combined_contexts = data_context + pinecone_contexts
        
        # 4) Generar respuesta
        assistant_resp = generate_chat_response(combined_contexts, user_input)
        st.session_state["messages"].append({"role":"assistant","content":assistant_resp})

        with st.chat_message("assistant"):
            st.markdown(assistant_resp)

def get_data_context():
    """
    Combina CSV en un string. Podrías filtrar con regex, etc.
    Para la demo, nos limitamos a 5 filas.
    """
    context_lines = []
    if os.path.exists("data/students.csv"):
        df_st = pd.read_csv("data/students.csv").head(5)
        context_lines.append("Estudiantes:\n" + df_st.to_string(index=False))

    if os.path.exists("data/courses.csv"):
        df_co = pd.read_csv("data/courses.csv").head(5)
        context_lines.append("Cursos:\n" + df_co.to_string(index=False))

    if os.path.exists("data/enrollments.csv"):
        df_en = pd.read_csv("data/enrollments.csv").head(5)
        context_lines.append("Enrollments:\n" + df_en.to_string(index=False))

    return context_lines

def main():
    app()

if __name__ == "__main__":
    main()
