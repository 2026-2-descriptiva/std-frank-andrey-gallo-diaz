import pandas as pd
import os

def pregunta_01():
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    df = pd.read_csv("data/superstore_orders.csv.gz", compression="gzip", sep=";", decimal=",")

    os.makedirs("submission", exist_ok=True)

    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")
    df["is_loss"] = df["Profit"] < 0
    df["loss_amount"] = df["Profit"].apply(lambda x: -x if x < 0 else 0)

    # tabla 1. profitability_summary.csv
    total_lines = len(df)
    total_orders = df["Order ID"].nunique()
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_profit_margin = (total_profit / total_sales if total_sales != 0 else 0)
    loss_lines = df["is_loss"].sum()
    loss_line_rate = loss_lines / total_lines if total_lines > 0 else 0
    lost_profit = df["loss_amount"].sum()
    df_profitability = pd.DataFrame(
        [
            {
                "lines": total_lines,
                "orders": total_orders,
                "sales": total_sales,
                "profit": total_profit,
                "profit_margin": total_profit_margin,
                "loss_lines": loss_lines,
                "loss_line_rate": loss_line_rate,
                "lost_profit": lost_profit,
            }
        ]
    )

    df_profitability.to_csv("submission/profitability_summary.csv", index=False)

    # tabla 2. discount_summary.csv
    def assign_discount_band(discount):
        pct = discount * 100
        if pct == 0:
            return "0%"
        elif pct <= 5:
            return "1%-5%"
        elif pct <= 10:
            return "6%-10%"
        else:
            return "más de 10%"

    df["discount_band"] = df["Discount"].apply(assign_discount_band)
    bands_order = ["0%", "1%-5%", "6%-10%", "más de 10%"]
    discount_rows = []

    for band in bands_order:
        sub = df[df["discount_band"] == band]
        lines_b = len(sub)
        sales_b = sub["Sales"].sum()
        profit_b = sub["Profit"].sum()
        profit_margin_b = profit_b / sales_b if sales_b != 0 else 0
        loss_lines_b = sub["is_loss"].sum()
        loss_line_rate_b = loss_lines_b / lines_b if lines_b > 0 else 0
        lost_profit_b = sub["loss_amount"].sum()

        discount_rows.append(
            {
                "discount_band": band,
                "lines": lines_b,
                "sales": sales_b,
                "profit": profit_b,
                "profit_margin": profit_margin_b,
                "loss_line_rate": loss_line_rate_b,
                "lost_profit": lost_profit_b,
            }
        )

    df_discount = pd.DataFrame(discount_rows)
    df_discount.to_csv("submission/discount_summary.csv", index=False)

    # tabla 3. priority_segments.csv
    grouped = df.groupby(["Customer Segment", "Product Category"])

    seg_rows = []
    for name, group in grouped:
        lines_s = len(group)
        if lines_s >= 100:
            sales_s = group["Sales"].sum()
            profit_s = group["Profit"].sum()
            profit_margin_s = profit_s / sales_s if sales_s != 0 else 0
            lost_profit_s = group["loss_amount"].sum()

            seg_rows.append(
                {
                    "Customer Segment": name[0],
                    "Product Category": name[1],
                    "lines": lines_s,
                    "sales": sales_s,
                    "profit": profit_s,
                    "profit_margin": profit_margin_s,
                    "lost_profit": lost_profit_s,
                }
            )

    df_priority = pd.DataFrame(seg_rows)
    if not df_priority.empty:
        df_priority = df_priority.sort_values(by="lost_profit", ascending=False).head(5)

    df_priority.to_csv("submission/priority_segments.csv", index=False)

    return df_profitability, df_discount, df_priority