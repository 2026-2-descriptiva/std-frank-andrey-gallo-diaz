from collections import defaultdict
import gzip

def pregunta_05():
    """Para cada letra de la primera columna (`letter`), encuentre el valor

    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """
    values_by_letter = defaultdict(list)
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for line in file:
            parts = line.split("\t")
            letter = parts[0]
            val = int(parts[1])
            values_by_letter[letter].append(val)

    return [
        (letter, max(vals), min(vals))
        for letter, vals in sorted(values_by_letter.items())
    ]