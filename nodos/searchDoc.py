from embeding.usarDoc import buscar_embeding
from template.crearPrompt import CrearPrompt
from template.crearRespuesta import CrearRespuesta


def searchDoc(indoc, question):
    if indoc["inDoc"] == "si":
        rEmbeding = buscar_embeding(question)
    else:
        rEmbeding = "no"

    return rEmbeding
