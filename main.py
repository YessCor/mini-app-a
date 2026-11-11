from __future__ import annotations

import random
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent

QUESTIONS = [
    {
        "category": "Ciencia",
        "text": "¿Cuál es el planeta más grande del sistema solar?",
        "options": ["Saturno", "Júpiter", "Neptuno", "Marte"],
        "answer": 1,
        "fact": "Júpiter es tan grande que cabrían más de 1.300 Tierras en su interior.",
    },
    {
        "category": "Ciencia",
        "text": "¿Qué gas absorben principalmente las plantas?",
        "options": ["Oxígeno", "Nitrógeno", "Dióxido de carbono", "Hidrógeno"],
        "answer": 2,
        "fact": "Las plantas usan dióxido de carbono durante la fotosíntesis para producir energía.",
    },
    {
        "category": "Ciencia",
        "text": "¿Cuántos huesos tiene, aproximadamente, un adulto?",
        "options": ["106", "206", "306", "406"],
        "answer": 1,
        "fact": "El cuerpo adulto tiene normalmente 206 huesos; al nacer tenemos cerca de 270.",
    },
    {
        "category": "Ciencia",
        "text": "¿Cuál es el metal líquido a temperatura ambiente?",
        "options": ["Mercurio", "Cobre", "Aluminio", "Hierro"],
        "answer": 0,
        "fact": "El mercurio es el único metal que permanece líquido a temperatura ambiente.",
    },
    {
        "category": "Ciencia",
        "text": "¿Qué órgano del cuerpo humano produce insulina?",
        "options": ["Hígado", "Riñón", "Páncreas", "Estómago"],
        "answer": 2,
        "fact": "El páncreas regula el azúcar en sangre, entre otras funciones.",
    },
    {
        "category": "Historia",
        "text": "¿En qué año llegó el ser humano a la Luna por primera vez?",
        "options": ["1959", "1969", "1979", "1989"],
        "answer": 1,
        "fact": "Neil Armstrong y Buzz Aldrin caminaron sobre la Luna el 20 de julio de 1969.",
    },
    {
        "category": "Historia",
        "text": "¿Qué civilización construyó Machu Picchu?",
        "options": ["Maya", "Azteca", "Inca", "Olmeca"],
        "answer": 2,
        "fact": "Machu Picchu fue una ciudad inca construida en el siglo XV en los Andes peruanos.",
    },
    {
        "category": "Historia",
        "text": "¿Quién fue la primera mujer en ganar un Premio Nobel?",
        "options": ["Ada Lovelace", "Marie Curie", "Rosalind Franklin", "Jane Goodall"],
        "answer": 1,
        "fact": "Marie Curie ganó el Nobel de Física en 1903 y el de Química en 1911.",
    },
    {
        "category": "Historia",
        "text": "¿Qué ciudad fue conocida como Constantinopla?",
        "options": ["Atenas", "Roma", "Estambul", "El Cairo"],
        "answer": 2,
        "fact": "La ciudad cambió oficialmente su nombre a Estambul en 1930.",
    },
    {
        "category": "Historia",
        "text": "¿En qué país comenzó el Renacimiento?",
        "options": ["Francia", "Italia", "España", "Grecia"],
        "answer": 1,
        "fact": "El Renacimiento comenzó en ciudades italianas como Florencia durante el siglo XIV.",
    },
    {
        "category": "Geografía",
        "text": "¿Cuál es el océano más grande del planeta?",
        "options": ["Atlántico", "Índico", "Ártico", "Pacífico"],
        "answer": 3,
        "fact": "El océano Pacífico cubre más superficie que toda la tierra firme de la Tierra.",
    },
    {
        "category": "Geografía",
        "text": "¿Cuál es la capital de Australia?",
        "options": ["Sídney", "Melbourne", "Canberra", "Brisbane"],
        "answer": 2,
        "fact": "Canberra fue elegida como capital para resolver la rivalidad entre Sídney y Melbourne.",
    },
    {
        "category": "Geografía",
        "text": "¿En qué continente está el desierto del Sahara?",
        "options": ["Asia", "África", "Oceanía", "América"],
        "answer": 1,
        "fact": "El Sahara es el desierto cálido más grande del mundo y ocupa gran parte del norte de África.",
    },
    {
        "category": "Geografía",
        "text": "¿Qué país tiene forma de bota?",
        "options": ["Grecia", "Portugal", "Italia", "Croacia"],
        "answer": 2,
        "fact": "La península italiana suele compararse con una bota pateando la isla de Sicilia.",
    },
    {
        "category": "Geografía",
        "text": "¿Cuál es la montaña más alta del mundo sobre el nivel del mar?",
        "options": ["K2", "Kilimanjaro", "Everest", "Aconcagua"],
        "answer": 2,
        "fact": "El Everest mide aproximadamente 8.849 metros sobre el nivel del mar.",
    },
    {
        "category": "Cultura pop",
        "text": "¿Cómo se llama la escuela de Harry Potter?",
        "options": ["Narnia", "Hogwarts", "Nevermore", "Camelot"],
        "answer": 1,
        "fact": "El nombre completo de la escuela es Colegio Hogwarts de Magia y Hechicería.",
    },
    {
        "category": "Cultura pop",
        "text": "¿Qué banda publicó el álbum «Abbey Road»?",
        "options": ["Queen", "The Rolling Stones", "The Beatles", "Pink Floyd"],
        "answer": 2,
        "fact": "Abbey Road fue el último álbum que grabaron juntos los cuatro Beatles.",
    },
    {
        "category": "Cultura pop",
        "text": "¿En qué saga aparece el personaje Darth Vader?",
        "options": ["Star Trek", "Star Wars", "Dune", "Matrix"],
        "answer": 1,
        "fact": "Darth Vader es uno de los personajes centrales de la saga Star Wars.",
    },
    {
        "category": "Cultura pop",
        "text": "¿Cuál es el nombre del vaquero de Toy Story?",
        "options": ["Buzz", "Andy", "Woody", "Rex"],
        "answer": 2,
        "fact": "Woody es un muñeco vaquero y el juguete favorito de Andy en la primera película.",
    },
    {
        "category": "Cultura pop",
        "text": "¿Qué instrumento toca Lisa Simpson?",
        "options": ["Guitarra", "Saxofón", "Trompeta", "Piano"],
        "answer": 1,
        "fact": "Lisa toca el saxofón barítono y es una apasionada del jazz.",
    },
]

CATEGORY_META = {
    "Ciencia": {"icon": "✳", "color": "mint", "description": "El mundo y cómo funciona"},
    "Historia": {"icon": "◷", "color": "peach", "description": "Viaja a través del tiempo"},
    "Geografía": {"icon": "◎", "color": "lilac", "description": "Lugares que dejan huella"},
    "Cultura pop": {"icon": "♫", "color": "yellow", "description": "De la pantalla al escenario"},
}


class QuizStart(BaseModel):
    category: str = "Aleatoria"
    question_count: int = Field(default=5, ge=1, le=10)


class AnswerSubmission(BaseModel):
    question_index: int = Field(ge=0)
    answer_index: int = Field(ge=0, le=3)


class QuizSession(BaseModel):
    id: str
    category: str
    questions: list[dict]
    answers: list[int | None]
    score: int = 0


app = FastAPI(title="Trivia Club", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
sessions: dict[str, QuizSession] = {}


def public_question(question: dict) -> dict:
    return {key: value for key, value in question.items() if key != "answer"}


def get_session(session_id: str) -> QuizSession:
    session = sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="No encontramos esta partida.")
    return session


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/categories")
def list_categories() -> list[dict]:
    categories = []
    for name, meta in CATEGORY_META.items():
        categories.append(
            {
                "name": name,
                "count": sum(question["category"] == name for question in QUESTIONS),
                **meta,
            }
        )
    return categories


@app.post("/api/quiz")
def start_quiz(request: QuizStart) -> dict:
    if request.category == "Aleatoria":
        available = QUESTIONS.copy()
    elif request.category in CATEGORY_META:
        available = [
            question for question in QUESTIONS if question["category"] == request.category
        ]
    else:
        raise HTTPException(status_code=422, detail="La categoría seleccionada no existe.")

    selected = random.sample(available, min(request.question_count, len(available)))
    session_id = str(uuid.uuid4())
    session = QuizSession(
        id=session_id,
        category=request.category,
        questions=selected,
        answers=[None] * len(selected),
    )
    sessions[session_id] = session
    return {
        "id": session_id,
        "category": session.category,
        "total": len(selected),
        "questions": [public_question(question) for question in selected],
    }


@app.post("/api/quiz/{session_id}/answer")
def submit_answer(session_id: str, submission: AnswerSubmission) -> dict:
    session = get_session(session_id)
    question_index = submission.question_index
    if question_index >= len(session.questions):
        raise HTTPException(status_code=404, detail="Esta pregunta no existe.")
    if session.answers[question_index] is not None:
        raise HTTPException(status_code=409, detail="Esta pregunta ya fue respondida.")
    if any(answer is None for answer in session.answers[:question_index]):
        raise HTTPException(status_code=409, detail="Responde las preguntas en orden.")

    question = session.questions[question_index]
    is_correct = submission.answer_index == question["answer"]
    session.answers[question_index] = submission.answer_index
    if is_correct:
        session.score += 1
    return {
        "correct": is_correct,
        "correct_answer": question["answer"],
        "fact": question["fact"],
        "score": session.score,
        "answered": question_index + 1,
        "total": len(session.questions),
    }


@app.get("/api/quiz/{session_id}/result")
def get_result(session_id: str) -> dict:
    session = get_session(session_id)
    if any(answer is None for answer in session.answers):
        raise HTTPException(status_code=409, detail="La partida todavía está en curso.")
    total = len(session.questions)
    percentage = round(session.score / total * 100) if total else 0
    if percentage == 100:
        message = "¡Impecable! Tienes una memoria increíble."
    elif percentage >= 60:
        message = "¡Muy bien! Sabes más de lo que crees."
    else:
        message = "¡Buen intento! Siempre hay algo nuevo que aprender."
    return {
        "category": session.category,
        "score": session.score,
        "total": total,
        "percentage": percentage,
        "message": message,
    }
