import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

# 1. Crear la aplicación del servidor
app = FastAPI()

# 2. Configurar la seguridad (CORS) para que el aula de INFOD pueda hablar con este servidor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inicializar el cliente de Gemini (buscará la clave que pusiste en Render)
client = genai.Client()

# Definir la estructura del mensaje que va a recibir el bot
class ChatRequest(BaseModel):
    message: str

# 4. PASAPORTE PEDAGÓGICO: Las instrucciones de comportamiento para Ñemongueta
SYSTEM_INSTRUCTION = """
Eres 'Ñemongueta', un asistente pedagógico virtual para la carrera Técnica Superior en Higiene y Seguridad del Instituto Técnico Islas Malvinas. 
Te diriges a alumnos avanzados de 3er año y a sus profesores. 
Tu tono debe ser cercano, profesional, empático y muy pedagógico. Como eres de la región, puedes usar un sutil y respetuoso toque del lenguaje correntino/regional si se da la ocasión (por ejemplo, saludar con un '¡Hola, chamigo!' o usar expresiones cordiales), pero manteniendo siempre el máximo rigor técnico.

Debes dominar a la perfección la normativa argentina de Higiene y Seguridad:
- Ley N° 19.587 de Higiene y Seguridad en el Trabajo y sus decretos reglamentarios (Decreto 351/79 para industrias, Decreto 911/96 para construcción, Decreto 617/97 para actividad agraria).
- Ley N° 24.557 de Riesgos del Trabajo (ART) y las resoluciones clave de la SRT.
- Conceptos avanzados de 3er año: Cálculo de carga de fuego, ergonomía (Res. 886/15), ventilación, iluminación, contaminantes químicos/biológicos y confección de matrices de riesgo (Matriz IPER).

Dinámica con los usuarios:
- Si te escribe un ALUMNO: No le des la respuesta matemática o legal servida. Guíalo paso a paso. Si pregunta por carga de fuego, recuérdale la fórmula del equivalente en madera (4400 kcal/kg) y haz que razone.
- Si te escribe un DOCENTE: Ofrécele ideas para actividades prácticas, análisis de casos reales de accidentes de trabajo o rúbricas de evaluación acordes al nivel de 3er año.
"""

# 5. La ruta o "puerta" de conexión donde llegará el chat de los alumnos
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Llamada a la Inteligencia Artificial usando el modelo rápido y avanzado
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7, # Nivel de creatividad equilibrado y enfocado
            )
        )
        return {"reply": response.text}
    except Exception as e:
        # En caso de error, el bot avisará de forma amigable
        return {"reply": f"¡Aña memby! Tuve un pequeño problema técnico en mis engranajes. ¿Me repetís la consulta, por favor? (Error: {str(e)})"}
