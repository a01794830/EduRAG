import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import logging

logger = logging.getLogger(__name__)

def generar_pdf_report(data, tipo, input_id):
    """
    data: dict con la info
    Ej: { "student_data": [...], "courses": [...] }
    ó   { "course_data": [...], "students": [...] }
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setTitle("Reporte EduRAG")
    x_margin = inch*0.5
    y = height - inch

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_margin, y, f"Reporte de {tipo}: {input_id}")
    y -= 0.4*inch
    c.setFont("Helvetica", 10)

    if "student_data" in data:
        st_info = data["student_data"][0]
        for k,v in st_info.items():
            line = f"{k}: {v}"
            c.drawString(x_margin, y, line)
            y-=0.2*inch
        c.drawString(x_margin, y, "Cursos Matriculados:")
        y-=0.2*inch
        for cinfo in data["courses"]:
            line = f"- {cinfo['course_id']}: {cinfo['nombre_curso']}, {cinfo['horario']}"
            c.drawString(x_margin, y, line)
            y-=0.2*inch

    if "course_data" in data:
        co_info = data["course_data"][0]
        for k,v in co_info.items():
            line = f"{k}: {v}"
            c.drawString(x_margin, y, line)
            y-=0.2*inch
        c.drawString(x_margin, y, "Estudiantes en el curso:")
        y-=0.2*inch
        for sinfo in data["students"]:
            line = f"- {sinfo['student_id']}: {sinfo['nombre']} (edad {sinfo['edad']})"
            c.drawString(x_margin, y, line)
            y-=0.2*inch

    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    logger.info("generar_pdf_report completado")
    return pdf_bytes
