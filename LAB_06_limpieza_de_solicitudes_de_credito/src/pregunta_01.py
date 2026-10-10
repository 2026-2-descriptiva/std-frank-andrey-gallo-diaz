import os
import pandas as pd

def pregunta_01():
    """El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de

    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    os.makedirs("submission", exist_ok=True)
    df = pd.read_csv("data/solicitudes_de_credito.csv.gz", sep=";", index_col=0)
    subset_columns = [col for col in df.columns if col != "comuna_ciudadano"]
    df.dropna(subset=subset_columns, inplace=True)

    text_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]

    for col in text_columns:
        df[col] = df[col].astype(str).str.lower()
        df[col] = df[col].str.replace("-", " ").str.replace("_", " ")
        df[col] = df[col].str.strip()

    df["barrio"] = df["barrio"].str.replace(r"\s+", " ", regex=True)
    df["estrato"] = df["estrato"].astype(int)
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.strip()
        .astype(float)
        .astype(int)
    )

    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    ).fillna(
        pd.to_datetime(
            df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce"
        )
    )
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].dt.strftime("%Y-%m-%d")
    target_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]
    df = df[target_columns]
    df.drop_duplicates(inplace=True)
    output_path = os.path.join("submission", "solicitudes_de_credito.csv")
    df.to_csv(output_path, sep=";", index=False)