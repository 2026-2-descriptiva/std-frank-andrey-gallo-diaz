from collections import defaultdict
import gzip

def pregunta_03():
    """Sume los valores de la segunda columna (`value`) para cada letra de la

    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """
    totals = defaultdict(int)
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for line in file:
            parts = line.split("\t")
            totals[parts[0]] += int(parts[1])

    return sorted(totals.items())