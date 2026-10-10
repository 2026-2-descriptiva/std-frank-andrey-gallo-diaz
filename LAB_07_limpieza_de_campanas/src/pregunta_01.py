import pandas as pd
import glob
import os

def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Los datos de una campaña de mercadeo bancario llegaron repartidos en diez

    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    os.makedirs("submission", exist_ok=True)
    file_paths = sorted(glob.glob("data/bank-marketing-campaing-*.csv.gz"))
    dataframes = [pd.read_csv(f, compression="gzip") for f in file_paths]
    df = pd.concat(dataframes, ignore_index=True)

    client = df[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]
    ].copy()

    client["job"] = (
        client["job"].astype(str).str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    )
    client["education"] = (
        client["education"].astype(str).str.replace(".", "_", regex=False)
    )
    client["education"] = client["education"].replace("unknown", pd.NA)
    client["credit_default"] = (
        (client["credit_default"].astype(str).str.lower() == "yes")
        .astype(int)
    )
    client["mortgage"] = (
        (client["mortgage"].astype(str).str.lower() == "yes")
        .astype(int)
    )

    campaign = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "month",
            "day",
        ]
    ].copy()

    campaign["previous_outcome"] = (
        (campaign["previous_outcome"].astype(str).str.lower() == "success")
        .astype(int)
    )
    campaign["campaign_outcome"] = (
        (campaign["campaign_outcome"].astype(str).str.lower() == "yes")
        .astype(int)
    )
    month_map = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }

    months = campaign["month"].astype(str).str.lower().map(month_map)
    days = campaign["day"].astype(str).str.zfill(2)
    campaign["last_contact_date"] = "2022-" + months + "-" + days

    campaign = campaign[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "last_contact_date",
        ]
    ]

    economics = df[
        ["client_id", "cons_price_idx", "euribor_three_months"]
    ].copy()
    client.to_csv("submission/client.csv", index=False)
    campaign.to_csv("submission/campaign.csv", index=False)
    economics.to_csv("submission/economics.csv", index=False)

    return client, campaign, economics