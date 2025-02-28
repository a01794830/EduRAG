import streamlit as st
import logging
import pandas as pd
import os
from utils.pdf_utils import generar_pdf_report

logger = logging.getLogger(__name__)

def app():
    logger.info("Entrando a Reportes Educativos")

    st.title("Reportes")
    st.write("Genera un reporte detallado de Estudiante o Curso")

    tipo = st.radio("Elige tipo ID:", ["Estudiante","Curso"])
    input_id = st.text_input("ID:", value="")

    if st.button("Generar Reporte"):
        if not input_id.strip():
            st.warning("Ingresa un ID")
            return

        # Busca data en CSV:
        if tipo=="Estudiante":
            report_data = generate_student_report(input_id)
        else:
            report_data = generate_course_report(input_id)

        if report_data:
            st.success("Reporte encontrado. Generando PDF...")
            pdf_bytes = generar_pdf_report(report_data, tipo, input_id)
            st.download_button(
                label="Descargar PDF",
                data=pdf_bytes,
                file_name=f"Reporte_{tipo}_{input_id}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("No se encontró información con ese ID.")

def generate_student_report(stud_id):
    if not os.path.exists("data/students.csv"):
        return None
    df_st = pd.read_csv("data/students.csv")
    student_info = df_st[df_st["student_id"]==stud_id]
    if student_info.empty:
        return None

    df_en = pd.read_csv("data/enrollments.csv")
    df_co = pd.read_csv("data/courses.csv")

    # sub-data
    enrolled = df_en[df_en["student_id"]==stud_id]
    merged = enrolled.merge(df_co, on="course_id", how="left")

    # Estructuramos
    info = {
        "student_data": student_info.to_dict(orient="records"),
        "courses": merged.to_dict(orient="records")
    }
    return info

def generate_course_report(course_id):
    if not os.path.exists("data/courses.csv"):
        return None
    df_co = pd.read_csv("data/courses.csv")
    c_info = df_co[df_co["course_id"]==course_id]
    if c_info.empty:
        return None

    df_en = pd.read_csv("data/enrollments.csv")
    df_st = pd.read_csv("data/students.csv")
    enrolled = df_en[df_en["course_id"]==course_id]
    joined = enrolled.merge(df_st, on="student_id", how="left")

    info = {
        "course_data": c_info.to_dict(orient="records"),
        "students": joined.to_dict(orient="records")
    }
    return info

def main():
    app()

if __name__=="__main__":
    main()
