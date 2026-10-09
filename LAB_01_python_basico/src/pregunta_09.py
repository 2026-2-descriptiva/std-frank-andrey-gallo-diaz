from collections import Counter
import gzip

def pregunta_09():
    """Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)

    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    counts = Counter()

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for line in file:
            metrics_str = line.strip().split("\t")[4]
            pairs = metrics_str.split(",")
            for pair in pairs:
                key, _ = pair.split(":")
                counts[key] += 1

    return dict(sorted(counts.items()))
