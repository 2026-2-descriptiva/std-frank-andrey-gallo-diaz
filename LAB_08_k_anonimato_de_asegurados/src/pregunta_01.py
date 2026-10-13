import json
import os
import pandas as pd


def pregunta_01():
    """Una aseguradora quiere publicar datos de sus afiliados para que un grupo

    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """
    os.makedirs("submission", exist_ok=True)

    df = pd.read_csv("data/insurance.csv.gz")

    orig_qis = ["age", "sex", "bmi", "children", "region"]
    orig_counts = df.groupby(orig_qis).transform("size")
    original_k = int(orig_counts.min())
    original_unique_records = int((orig_counts == 1).sum())

    def obtener_grupo_edad(edad):
        if edad <= 29:
            return "18-29"
        elif edad <= 39:
            return "30-39"
        elif edad <= 49:
            return "40-49"
        else:
            return "50-64"

    def obtener_grupo_bmi(bmi):
        if bmi < 18.5:
            return "bajo peso"
        elif bmi < 25.0:
            return "normal"
        elif bmi < 30.0:
            return "sobrepeso"
        else:
            return "obesidad"

    def obtener_grupo_hijos(hijos):
        if hijos == 0:
            return "0"
        elif hijos <= 2:
            return "1-2"
        else:
            return "3+"

    df["age_group"] = df["age"].apply(obtener_grupo_edad)
    df["bmi_group"] = df["bmi"].apply(obtener_grupo_bmi)
    df["children_group"] = df["children"].apply(obtener_grupo_hijos)

    esquemas_config = {
        "with_children": [
            "age_group",
            "sex",
            "bmi_group",
            "children_group",
            "region",
        ],
        "without_children": ["age_group", "sex", "bmi_group", "region"],
    }

    resultados_esquemas = {}
    metricas_esquemas = {}

    for nombre_esquema, qis in esquemas_config.items():
        df[f"_tamano_clase_{nombre_esquema}"] = df.groupby(qis).transform(
            "size"
        )
        equivalence_classes = int(df[qis].drop_duplicates().shape[0])
        k_before_suppression = int(
            df[f"_tamano_clase_{nombre_esquema}"].min()
        )

        mascara_publicada = df[f"_tamano_clase_{nombre_esquema}"] >= 5
        suppressed_records = int((~mascara_publicada).sum())
        published_records = int(mascara_publicada.sum())

        df_publicado = df[mascara_publicada]
        published_classes = int(df_publicado[qis].drop_duplicates().shape[0])

        clase_smoker_nunique = df_publicado.groupby(qis)["smoker"].nunique()
        clases_sin_diversidad = clase_smoker_nunique[
            clase_smoker_nunique == 1
        ].index
        if len(clases_sin_diversidad) > 0:
            temp_pub = df_publicado.copy()
            if len(qis) == 1:
                mascara_sin_div = temp_pub[qis[0]].isin(clases_sin_diversidad)
            else:
                mascara_sin_div = pd.MultiIndex.from_frame(
                    temp_pub[qis]
                ).isin(
                    pd.MultiIndex.from_frame(
                        pd.DataFrame(list(clases_sin_diversidad), columns=qis)
                    )
                )
            records_without_diversity = int(mascara_sin_div.sum())
            classes_without_diversity_count = len(clases_sin_diversidad)
        else:
            records_without_diversity = 0
            classes_without_diversity_count = 0

        resultados_esquemas[nombre_esquema] = {
            "quasi_identifiers": qis,
            "equivalence_classes": equivalence_classes,
            "k_before_suppression": k_before_suppression,
            "suppressed_records": suppressed_records,
            "published_records": published_records,
            "published_classes": published_classes,
            "classes_without_smoker_diversity": classes_without_diversity_count,
            "records_without_smoker_diversity": records_without_diversity,
        }
        metricas_esquemas[nombre_esquema] = suppressed_records

    selected_scheme = min(metricas_esquemas, key=metricas_esquemas.get)

    mean_charges_original = float(df["charges"].mean())
    smoker_rate_original = float(
        (df["smoker"].str.lower() == "yes").mean()
    )

    selected_qis = esquemas_config[selected_scheme]
    selected_pub_mask = df[f"_tamano_clase_{selected_scheme}"] >= 5
    df_selected_published = df[selected_pub_mask]

    mean_charges_published = float(df_selected_published["charges"].mean())
    smoker_rate_published = float(
        (df_selected_published["smoker"].str.lower() == "yes").mean()
    )

    reporte = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": resultados_esquemas,
        "selected_scheme": selected_scheme,
        "mean_charges_original": mean_charges_original,
        "mean_charges_published": mean_charges_published,
        "smoker_rate_original": smoker_rate_original,
        "smoker_rate_published": smoker_rate_published,
    }

    report_path = os.path.join("submission", "privacy_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=4, ensure_ascii=False)

    output_cols = selected_qis + ["smoker", "charges"]
    df_published_output = df_selected_published[output_cols].copy()
    csv_path = os.path.join("submission", "insurance_published.csv")
    df_published_output.to_csv(csv_path, index=False)

    return reporte