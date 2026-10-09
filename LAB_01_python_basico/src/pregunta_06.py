from collections import defaultdict
import gzip

def pregunta_06():
    """La quinta columna (`metrics`) contiene pares `clave:valor` separados por

    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    values_by_key = defaultdict(list)

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for line in file:
            metrics_str = line.strip().split("\t")[4]
            pairs = metrics_str.split(",")
            for pair in pairs:
                key, val = pair.split(":")
                values_by_key[key].append(int(val))

    return [
        (key, min(vals), max(vals))
        for key, vals in sorted(values_by_key.items())
    ]