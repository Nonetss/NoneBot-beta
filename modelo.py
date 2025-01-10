from modelo.llama import llm
from template.crearPrompt import CrearPrompt
from template.utils.normaliza_text import normalizar_texto

promp = CrearPrompt()

pregunta = promp.generar_prompt(
    nombre_prompt="searchDoc", prompt_humano="Sabes quien es Antonio?"
)

respuesta = llm.invoke(pregunta)

print(normalizar_texto(respuesta))
