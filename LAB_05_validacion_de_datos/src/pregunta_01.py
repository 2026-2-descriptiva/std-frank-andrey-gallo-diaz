import json
import os
import re
import pandas as pd


def main():
    """Antes de limpiar o analizar un conjunto de datos, un analista debe

    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """
    
    os.makedirs("submission", exist_ok=True)

    required_columns = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email",
    ]

    df = pd.read_csv("data/ventas.csv.gz", dtype=str, keep_default_na=False)
    raw_columns = list(df.columns)
    normalized_columns = [
        re.sub(r"\s+", "_", col.lstrip("\ufeff").strip().lower())
        for col in raw_columns
    ]
    df.columns = normalized_columns
    row_count = int(len(df))
    column_count = int(len(df.columns))
    missing_required_columns = sorted(
        [col for col in required_columns if col not in df.columns]
    )
    unexpected_columns = sorted(
        [col for col in df.columns if col not in required_columns]
    )
    duplicate_row_count = int(df.duplicated(keep="first").sum())

    if "supplier_id" in df.columns:
        supplier_id_counts = df["supplier_id"].value_counts()
        duplicated_ids = supplier_id_counts[supplier_id_counts > 1].index
        duplicate_supplier_id_row_count = int(
            df["supplier_id"].isin(duplicated_ids).sum()
        )
    else:
        duplicate_supplier_id_row_count = 0

    missing_value_count_by_column = {}
    for col in df.columns:
        is_missing = df[col].apply(
            lambda x: x is None or str(x).strip() in ["", "N/A"]
        )
        missing_value_count_by_column[col] = int(is_missing.sum())

    invalid_email_count = 0
    if "contact_email" in df.columns:
        email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        for val in df["contact_email"]:
            if val is None or str(val).strip() in ["", "N/A"]:
                invalid_email_count += 1
            else:
                if not email_regex.match(str(val).strip()):
                    invalid_email_count += 1

    invalid_unit_count = 0
    if "units" in df.columns:
        for val in df["units"]:
            if val is None or str(val).strip() in ["", "N/A"]:
                continue
            v_str = str(val).strip()
            try:
                val_num = float(v_str)
                if not (val_num.is_integer() and val_num > 0):
                    invalid_unit_count += 1
            except ValueError:
                invalid_unit_count += 1

    country_values = []
    if "country" in df.columns:
        country_values = sorted(df["country"].unique().tolist())

    report = {
        "row_count": row_count,
        "column_count": column_count,
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values,
    }

    report_path = os.path.join("submission", "data_quality_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    return report

if __name__ == "__main__":
    main()