import random
import csv
import logging
import os

logger = logging.getLogger(__name__)

STUDENT_COUNT = 20
COURSE_COUNT = 5

def generate_synthetic_students(n=20):
    """
    Genera n estudiantes con:
    - student_id
    - nombre
    - edad
    - etc.
    """
    first_names = ["Juan", "María", "Pedro", "Lucía", "Carlos", "Sofía", "Miguel", "Laura"]
    last_names = ["Pérez", "García", "Rodríguez", "López", "Martínez", "Sánchez"]

    students = []
    for i in range(n):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        stud_id = f"S{i+1:03d}"
        nombre = f"{fn} {ln}"
        edad = random.randint(18, 35)
        students.append({
            "student_id": stud_id,
            "nombre": nombre,
            "edad": edad
        })
    return students

def generate_synthetic_courses(m=5):
    """
    Genera m cursos con:
    - course_id
    - nombre_curso
    - horario
    - creditos
    """
    course_names = ["Matemáticas Básicas", "Programación 1", "Historia Universal", 
                    "Inglés Avanzado", "Física General", "Biología", "Literatura", "Química"]
    courses = []
    for i in range(m):
        course_id = f"C{i+1:02d}"
        c_name = random.choice(course_names)
        schedule = random.choice(["Lun-Mie 8-10am", "Mar-Jue 10-12pm", "Vie 2-4pm"])
        creditos = random.randint(2,5)
        courses.append({
            "course_id": course_id,
            "nombre_curso": c_name,
            "horario": schedule,
            "creditos": creditos
        })
    return courses

def generate_enrollments(students, courses):
    """
    Asocia cada estudiante con algunos cursos.
    """
    enrollments = []
    for st in students:
        # elige 1-3 cursos
        n_cursos = random.randint(1,3)
        c_sample = random.sample(courses, k=n_cursos)
        for c in c_sample:
            # supongamos un random de nota o algo
            enrollments.append({
                "student_id": st["student_id"],
                "course_id": c["course_id"]
            })
    return enrollments

def save_to_csv(students, courses, enrollments, filename="data/synthetic_data.csv"):
    """
    Guarda todo en un CSV o varios CSV. 
    Para simplificar, se guarda uno distinto por cada tipo.
    """
    os.makedirs("data", exist_ok=True)

    # Estudiantes
    with open("data/students.csv","w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id","nombre","edad"])
        writer.writeheader()
        for st in students:
            writer.writerow(st)

    # Cursos
    with open("data/courses.csv","w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["course_id","nombre_curso","horario","creditos"])
        writer.writeheader()
        for c in courses:
            writer.writerow(c)

    # Enrollments
    with open("data/enrollments.csv","w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id","course_id"])
        writer.writeheader()
        for e in enrollments:
            writer.writerow(e)

    logger.info(f"Guardados CSV en data/ (students, courses, enrollments)")

def generate_all_data():
    logger.info("Generando data sintética educativa...")
    students = generate_synthetic_students(STUDENT_COUNT)
    courses = generate_synthetic_courses(COURSE_COUNT)
    enrollments = generate_enrollments(students, courses)
    save_to_csv(students, courses, enrollments)
    logger.info("Data generada con éxito.")
