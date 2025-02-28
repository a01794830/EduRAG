import streamlit as st
from utils.logging_config import setup_logging
import logging

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    st.set_page_config(
        page_title="EduRAG",
        page_icon="🎓",
        layout="wide"
    )
    logger.info("Iniciando EduRAG app.py")

    st.write("""
    # EduRAG
    Sistema para gestión educativa + RAG con PDFs.
    Usa el menú lateral:
    - Generar Data (matrículas, cursos)
    - Documentos (ver PDFs y subirlos a Pinecone)
    - Chat (consultas)
    - Reportes (ID estudiante/curso)
    """)

if __name__=="__main__":
    main()
