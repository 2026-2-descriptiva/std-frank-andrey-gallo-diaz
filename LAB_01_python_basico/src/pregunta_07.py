from collections import defaultdict
import gzip

def pregunta_07():
    """Para cada valor distinto de la segunda columna (`value`), construya la

    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """
    letters_by_value = defaultdict(list)

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("\t")
            letter = parts[0]
            val = int(parts[1])
            letters_by_value[val].append(letter)

    return sorted(letters_by_value.items())