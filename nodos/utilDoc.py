from embeding.usarDoc import buscar_embeding
from nodos.inDoc import inDoc
from nodos.searchDoc import searchDoc
from template.crearPrompt import CrearPrompt
from template.crearRespuesta import CrearRespuesta


def utilDoc(doc, question):
    promp = CrearPrompt()
    respuesta = CrearRespuesta()

    if doc != "no":
        # Evaluar documento por documento
        for document in doc["document"]:
            prompt_document = document.page_content

            # Generar el prompt individualmente
            pregunta = promp.generar_prompt(
                nombre_prompt="utilDoc",
                prompt_humano=question,
                prompt_document=prompt_document,
            )

            # Generar la respuesta
            result = respuesta.generar_respuesta(pregunta)

            # ✅ No es necesario json.loads(), ya es un diccionario
            if result.get("utilDoc") == "si":
                print("✅ Documento útil encontrado")
                return "si"

        # Si ningún documento es útil
        return "no"
    else:
        return "no"
