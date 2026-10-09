from collections import defaultdict
import gzip

def pregunta_12():
    """Para cada letra de la primera columna (`letter`), sume todos los valores

    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """
    totals = defaultdict(int)

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("\t")
            letter = parts[0]
            metrics_str = parts[4]
            pairs = metrics_str.split(",")
            for pair in pairs:
                _, val = pair.split(":")
                totals[letter] += int(val)

    return dict(sorted(totals.items()))