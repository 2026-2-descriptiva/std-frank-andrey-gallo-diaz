import gzip

def pregunta_10():
    """Para cada registro del archivo, en el mismo orden en que aparecen,

    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """
    result = []

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("\t")
            letter = parts[0]
            num_codes = len(parts[3].split(","))
            num_metrics = len(parts[4].split(","))
            result.append((letter, num_codes, num_metrics))

    return result