import pandas as pd
import os
import numpy as np

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """

    path_web = "data/historical_requests_web.csv.gz"
    path_letter = "data/historical_requests_letter.csv.gz"
    df_web = pd.read_csv(path_web).drop_duplicates()
    df_letter = pd.read_csv(path_letter).drop_duplicates()
    df_web["channel"] = "web"
    df_letter["channel"] = "letter"
    df = pd.concat([df_web, df_letter], ignore_index=True)
    df["in_date"] = pd.to_datetime(df["in_date"])
    df["out_date"] = pd.to_datetime(df["out_date"])
    df["year"] = df["in_date"].dt.year
    df["answered"] = df["out_date"].notna()
    df["calendar_days"] = (df["out_date"] - df["in_date"]).dt.days

    mask_answered = df["answered"]
    df["business_days"] = np.nan
    in_dates_ans = (df.loc[mask_answered, "in_date"] + pd.Timedelta(days=1)).dt.date.values.astype("datetime64[D]")
    out_dates_ans = (df.loc[mask_answered, "out_date"] + pd.Timedelta(days=1)).dt.date.values.astype("datetime64[D]")

    df.loc[mask_answered, "business_days"] = np.busday_count(in_dates_ans, out_dates_ans)
    df["on_time"] = (df["answered"]) & (df["business_days"] <= 15)

    os.makedirs("submission", exist_ok=True)

    channel_list = []
    for ch in sorted(df["channel"].unique()):
        sub = df[df["channel"] == ch]
        reqs = len(sub)
        ans = sub["answered"].sum()
        pend = reqs - ans
        med_bus = sub.loc[sub["answered"], "business_days"].median()
        ontime_rate = sub["on_time"].sum() / reqs

        channel_list.append(
            {
                "channel": ch,
                "requests": reqs,
                "answered": ans,
                "pending": pend,
                "median_business_days": med_bus,
                "on_time_rate": ontime_rate,
            }
        )

    channel_summary = pd.DataFrame(channel_list)
    channel_summary.to_csv("submission/channel_summary.csv", index=False)

    yearly_list = []
    years = sorted(df["year"].unique())
    channels = sorted(df["channel"].unique())

    for yr in years:
        for ch in channels:
            sub = df[(df["year"] == yr) & (df["channel"] == ch)]
            if len(sub) > 0:
                reqs = len(sub)
                pend = (~sub["answered"]).sum()
                ontime_rate = sub["on_time"].sum() / reqs
                yearly_list.append(
                    {
                        "year": yr,
                        "channel": ch,
                        "requests": reqs,
                        "pending": pend,
                        "on_time_rate": ontime_rate,
                    }
                )

    yearly_summary = pd.DataFrame(yearly_list)
    yearly_summary.to_csv("submission/yearly_summary.csv", index=False)

    sample_day = df["day_name"].iloc[0]
    days_order_en = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    days_order_es = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo",
    ]

    if sample_day in days_order_es or "Miercoles" in df["day_name"].values:
        df["day_name_clean"] = df["day_name"].replace({"Miercoles": "Miércoles"})
        target_days = days_order_es
    else:
        df["day_name_clean"] = df["day_name"]
        target_days = days_order_en

    entry_day_list = []
    for day in target_days:
        sub = df[df["day_name_clean"] == day]
        if len(sub) > 0:
            reqs = len(sub)
            ans_sub = sub[sub["answered"]]
            med_cal = ans_sub["calendar_days"].median()
            med_bus = ans_sub["business_days"].median()

            entry_day_list.append(
                {
                    "day_name": day,
                    "requests": reqs,
                    "median_calendar_days": med_cal,
                    "median_business_days": med_bus,
                }
            )

    entry_day_summary = pd.DataFrame(entry_day_list)
    entry_day_summary.to_csv("submission/entry_day_summary.csv", index=False)

    return channel_summary, yearly_summary, entry_day_summary