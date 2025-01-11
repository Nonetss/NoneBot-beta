from template.crearPrompt import CrearPrompt
from template.crearRespuesta import CrearRespuesta


def inDoc(question: str):
    promp = CrearPrompt()
    respuesta = CrearRespuesta()

    pregunta = promp.generar_prompt(nombre_prompt="inDoc", prompt_humano=question)
    result = respuesta.generar_respuesta(pregunta)
    return result
