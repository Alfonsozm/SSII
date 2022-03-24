import pandas as pd
import sqlite3
import numpy as np
import math

con = sqlite3.connect('database.db')
cursorObj = con.cursor()


def dataframe_v2():
    df = pd.read_sql_query("SELECT * FROM usuarios group by username", con)
    df["IPs"] = pd.read_sql_query("SELECT COUNT(ip) from ips group by username", con)
    df["Fechas"] = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas group by username", con)
    return df


def valores_missing(dataframe):
    missing = 0
    for index, row in dataframe.iterrows():
        if math.isnan(row["telefono"]):
            missing += 1
        if row["provincia"] is None:
            missing += 1
        if row["IPs"] == 0:
            missing += 1
    return missing


def valores_presentes(dataframe):
    """Calcula el tamaño total del dataframe y se le resta los valores que no esten presentes"""
    return len(dataframe) * len(dataframe.columns) - valores_missing(dataframe)


def media_fechas(dataframe) -> float:
    """Calcula la media del total de fechas que se ha iniciado sesión."""
    return dataframe["Fechas"].sum() / len(dataframe)


def desviacion_fechas(dataframe) -> float:
    """Calcula la desviación estándar del total de fechas que se ha iniciado sesión."""
    return float(np.std(dataframe["Fechas"].to_numpy()))


def max_fechas(dataframe) -> int:
    """Calcula el valor máximo del total de fechas que se ha iniciado sesión"""
    return dataframe["Fechas"].max()


def min_fechas(dataframe) -> int:
    """Calcula el valor mínimo del total de fechas que se ha iniciado sesión"""
    return dataframe["Fechas"].min()


def media_ips(dataframe) -> float:
    """Calcula la media del total de IPs que se han detectado"""
    return dataframe["IPs"].sum() / len(dataframe)


def desviacion_ips(dataframe) -> float:
    """Calcula la desviación estándar del total de IPs que se han detectado"""
    return float(np.std(dataframe["IPs"].to_numpy()))


def media_emails_totales(dataframe) -> float:
    """Calcula la media del número de emails recibidos"""
    return dataframe["emails_total"].sum() / len(dataframe)


def desviacion_emails_totales(dataframe) -> float:
    """Calcula la desviación estándar del número de emails recibidos"""
    return float(np.std(dataframe["emails_total"].to_numpy()))


def max_emails_totales(dataframe) -> int:
    """Calcula el valor máximo del número de emails recibidos"""
    return dataframe["emails_total"].max()


def min_emails_totales(dataframe) -> int:
    """Calcula el valor mínimo del número de emails recibidos"""
    return dataframe["emails_total"].min()


df = dataframe_v2()
print("Muestras presentes:\n", valores_presentes(df))
print("Media del total de fechas que se ha iniciado sesión:\n", media_fechas(df))
print("Desviación estándar del total de fechas que se ha iniciado sesión:\n", desviacion_fechas(df))
print("Media del total de IPs que se han detectado:\n", media_ips(df))
print("Desviación estándar del total de IPs que se han detectado:\n", desviacion_ips(df))
print("Media del número de emails recibidos:\n", media_emails_totales(df))
print("Desviación estándar del número de emails recibidos:\n", desviacion_emails_totales(df))
print("Valor mínimo del total de fechas que se ha iniciado sesión:\n", min_fechas(df))
print("Valor máximo del total de fechas que se ha iniciado sesión:\n", max_fechas(df))
print("Valor mínimo del número de emails recibidos:\n", min_emails_totales(df))
print("Valor máximo del número de emails recibidos:\n", max_emails_totales(df))
