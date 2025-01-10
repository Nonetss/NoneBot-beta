import json
import os

from langchain.schema import Document

from embeding.utils.hash import calcular_hash


def leer_archivos(
    directorio, text_splitter, archivos_guardados, archivos_guardados_path
):
    doc = []
    for file in os.listdir(directorio):
        path = os.path.join(directorio, file)

        # Intentar obtener la fecha de modificación
        try:
            fecha_modificacion = os.path.getmtime(path)
        except OSError as e:
            print(f"Error al obtener la fecha de modificación de {path}: {e}")
            continue

        # Intentar calcular el hash del archivo
        try:
            hash = calcular_hash(path)
        except OSError as e:
            print(f"Error al obtener el hash del archivo {path}: {e}")
            continue

        # Comprobar si el archivo ha cambiado
        if file not in archivos_guardados or archivos_guardados[file]["hash"] != hash:
            try:
                with open(path, "r", encoding="utf-8") as doc_info:
                    content = doc_info.read()
                    doc_split = text_splitter.split_text(content)

                # Añadir los fragmentos al documento
                for i, fragment in enumerate(doc_split):
                    doc.append(
                        Document(
                            page_content=fragment,
                            metadata={
                                "filename": file,
                                "last_modified": fecha_modificacion,
                                "fragment_index": i,
                                "hash_document": hash,
                            },
                        )
                    )

                # ✅ Guardar tanto la información anterior como la actual
                archivos_guardados[file] = {
                    "previous_hash": (
                        archivos_guardados[file]["hash"]
                        if file in archivos_guardados
                        else None
                    ),
                    "previous_last_modified": (
                        archivos_guardados[file]["last_modified"]
                        if file in archivos_guardados
                        else None
                    ),
                    "hash": hash,
                    "last_modified": fecha_modificacion,
                }

            except Exception as e:
                print(f"Error al leer el archivo {path}: {e}")

    # Guardar el estado actualizado de archivos guardados
    with open(archivos_guardados_path, "w", encoding="utf-8") as f:
        json.dump(archivos_guardados, f, ensure_ascii=False, indent=4)

    return doc
