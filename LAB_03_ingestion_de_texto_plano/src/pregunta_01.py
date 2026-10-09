import pandas as pd
import re

def pregunta_01():
    """El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """
    with open("data/clusters_report.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    content_lines = lines[4:]
    clusters = []
    current_cluster = None

    for line in content_lines:
        match = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)", line)
        if match:
            if current_cluster:
                keywords = re.sub(r"\s+", " ", current_cluster[3]).strip()
                if keywords.endswith("."):
                    keywords = keywords[:-1]
                current_cluster[3] = keywords
                clusters.append(current_cluster)
            cluster_num = int(match.group(1))
            quantity = int(match.group(2))
            percentage = float(match.group(3).replace(",", "."))
            keywords = match.group(4).strip()
            current_cluster = [cluster_num, quantity, percentage, keywords]
        else:
            if current_cluster and line.strip():
                current_cluster[3] += " " + line.strip()
    if current_cluster:
        keywords = re.sub(r"\s+", " ", current_cluster[3]).strip()
        if keywords.endswith("."):
            keywords = keywords[:-1]
        current_cluster[3] = keywords
        clusters.append(current_cluster)

    df = pd.DataFrame(
        clusters,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )

    return df