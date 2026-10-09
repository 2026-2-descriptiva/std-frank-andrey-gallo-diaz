import gzip

def pregunta_01():
    """Calcule la suma de los valores de la segunda columna (`value`) del

    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        total_sum = sum(int(line.split("\t")[1]) for line in file)

    return total_sum  

#En todas las preguntas al final va esto: raise NotImplementedError con una(1 columna) de identación 