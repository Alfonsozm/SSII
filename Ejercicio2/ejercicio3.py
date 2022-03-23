import pandas as pd
import sqlite3
import numpy as np

con = sqlite3.connect('database.db')
cursorObj = con.cursor()


def dataframe_permisos(permisos: int):
    if permisos == 1 or permisos == 0:
        df = pd.read_sql_query("SELECT * FROM usuarios WHERE permisos = \'{}\' group by username".format(permisos), con)
        df["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(username) WHERE permisos "
                                      "= \'{}\' group by username".format(permisos), con)
        df["Fechas"] = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(username) WHERE "
                                         "permisos = \'{}\' group by username".format(permisos), con)
        return df
    else:
        return "error"


def dataframe_correos(rango: str):
    correos = 200

    if rango == "mayor":
        df = pd.read_sql_query("SELECT * FROM usuarios WHERE emails_total >= \'{}\' group by username".format(correos),
                               con)
        df["IPs"] = pd.read_sql_query(
            "SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(username) WHERE emails_total "
            ">= \'{}\' group by username".format(correos), con)
        df["Fechas"] = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(username) WHERE "
                                         "emails_total >= \'{}\' group by username".format(correos), con)
        return df
    elif rango == "menor":
        df = pd.read_sql_query("SELECT * FROM usuarios WHERE emails_total < \'{}\' group by username".format(correos),
                               con)
        df["IPs"] = pd.read_sql_query(
            "SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(username) WHERE emails_total "
            "< \'{}\' group by username".format(correos), con)
        df["Fechas"] = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(username) WHERE "
                                         "emails_total < \'{}\' group by username".format(correos), con)
        return df
    else:
        return "error"


def mediana(dataframe):
    return np.median(dataframe["emails_phishing"].to_numpy())


def media(dataframe) -> float:
    return dataframe["emails_phishing"].sum() / len(dataframe)


def varianza(dataframe):
    return np.var(dataframe["emails_phishing"].to_numpy())


def maximo(dataframe) -> int:
    return dataframe["emails_phising"].max()


#No sé a que se refiere en este apartado
def valores_missing(dataframe):
    missing = 0
    for index, row in dataframe.iterrows():
        if row["emails_phishing"] == 0:
            missing += 1
    return missing


#No sé a que se refiere en este apartado
def observaciones(dataframe):
    obs = 0
    for index, row in dataframe.iterrows():
        if row["emails_phishing"] != 0:
            obs += 1
    return obs


#print(dataframe_permisos(0))
#print(dataframe_permisos(1))
#print(dataframe_correos("mayor"))
#print(dataframe_correos("menor"))

print(varianza(dataframe_correos("mayor")))
