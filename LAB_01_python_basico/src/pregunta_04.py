from collections import Counter
import gzip

def pregunta_04():
    """Cuente cuántos registros hay en cada mes, usando la fecha de la tercera

    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """
    counts = Counter()
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for line in file:
            date_str = line.split("\t")[2]
            month = date_str.split("-")[1]
            counts[month] += 1

    return sorted(counts.items())