from modelo.llama import llm
from template.crearPrompt import CrearPrompt
from template.crearRespuesta import CrearRespuesta
from template.utils.normaliza_text import normalizar_texto

promp = CrearPrompt()

respuesta = CrearRespuesta()

pregunta = promp.generar_prompt(
    nombre_prompt="searchDoc", prompt_humano="Sabes quien es Antonio?"
)


print(respuesta.generar_respuesta(pregunta))
