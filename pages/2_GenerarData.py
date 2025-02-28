import streamlit as st
import logging
from utils.synthetic_data import generate_all_data
import os
import pandas as pd

logger = logging.getLogger(__name__)

def app():
    logger.info("Entrando a GenerarData")

    st.title("Generar Data Educativa Sintética")
    st.write("Crea estudiantes, cursos, etc.")

    if st.button("Generar Data"):
        generate_all_data()
        st.success("Data generada en /data/ .")

    # Mostrar si ya existen
    st.subheader("Vista previa:")
    if os.path.exists("data/students.csv"):
        df_st = pd.read_csv("data/students.csv")
        st.write("Estudiantes:", df_st.head())

    if os.path.exists("data/courses.csv"):
        df_co = pd.read_csv("data/courses.csv")
        st.write("Cursos:", df_co.head())

    if os.path.exists("data/enrollments.csv"):
        df_en = pd.read_csv("data/enrollments.csv")
        st.write("Enrollments:", df_en.head())

def main():
    app()

if __name__ == "__main__":
    main()
