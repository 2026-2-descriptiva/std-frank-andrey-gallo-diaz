from collections import defaultdict
import gzip

def pregunta_11():
    """La cuarta columna (`codes`) contiene letras minúsculas separadas por

    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """
    totals = defaultdict(int)

    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("\t")
            val = int(parts[1])
            codes = parts[3].split(",")
            for code in codes:
                totals[code] += val

    return dict(sorted(totals.items()))