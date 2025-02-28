import streamlit as st
import logging
from utils.doc_utils import parse_pdf, chunk_text
from utils.pinecone_utils import upsert_docs

logger = logging.getLogger(__name__)

def app():
    logger.info("Entrando a CargarDocumentos (pdfs)")

    st.title("Cargar PDF de Currículas/Cursos")
    st.write("Sube tus PDFs y se indexarán en Pinecone para consultas RAG.")

    uploaded_files = st.file_uploader("Selecciona PDFs", type=["pdf"], accept_multiple_files=True)

    if st.button("Procesar e Indexar"):
        if not uploaded_files:
            st.warning("No subiste archivos.")
            return

        all_chunks = []
        for f in uploaded_files:
            pdf_text = parse_pdf(f)
            chunks = chunk_text(pdf_text, chunk_size=800)
            all_chunks.extend(chunks)

        upsert_docs(all_chunks)
        st.success("¡Documentos indexados!")
        logger.info(f"Indexados {len(all_chunks)} trozos de PDF.")

def main():
    app()

if __name__ == "__main__":
    main()
