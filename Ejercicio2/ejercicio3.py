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
    return dataframe["emails_phishing"].max()


def minimo(dataframe) -> int:
    return dataframe["emails_phishing"].min()


#No sé a que se refiere en este apartado
def valores_missing(dataframe):
    missing = 0
    for index, row in dataframe.iterrows():
        if row["emails_phishing"] is None:
            missing += 1
    return missing


#No sé a que se refiere en este apartado
def observaciones(dataframe) -> int:
    return dataframe["emails_phishing"].sum()


#print(dataframe_permisos(0))
#print(dataframe_permisos(1))
#print(dataframe_correos("mayor"))
#print(dataframe_correos("menor"))

df_administradores = dataframe_permisos(1)
df_usuarios = dataframe_permisos(0)

print("Resultados por agrupación de permisos:")
print("Permisos == 1:")
print("Número de observaciones:", observaciones(df_administradores))
print("Número de valores ausentes:", valores_missing(df_administradores))
print("Mediana:", mediana(df_administradores))
print("Media:", media(df_administradores))
print("Varianza:", varianza(df_administradores))
print("Valor máximo:", maximo(df_administradores))
print("Valor mínimo:", minimo(df_administradores))
print()

print("Permisos == 0:")
print("Número de observaciones:", observaciones(df_usuarios))
print("Número de valores ausentes:", valores_missing(df_usuarios))
print("Mediana:", mediana(df_usuarios))
print("Media:", media(df_usuarios))
print("Varianza:", varianza(df_usuarios))
print("Valor máximo:", maximo(df_usuarios))
print("Valor mínimo:", minimo(df_usuarios))
print()

df_correosmas = dataframe_correos("mayor")
df_correosmenos = dataframe_correos("menor")
print("Resultados por agrupación de número de emails recibidos:")
print("Más de 200 correos:")
print("Número de observaciones:", observaciones(df_correosmas))
print("Número de valores ausentes:", valores_missing(df_correosmas))
print("Mediana:", mediana(df_correosmas))
print("Media:", media(df_correosmas))
print("Varianza:", varianza(df_correosmas))
print("Valor máximo:", maximo(df_correosmas))
print("Valor mínimo:", minimo(df_correosmas))
print()

print("Menos de 200 correos:")
print("Número de observaciones:", observaciones(df_correosmenos))
print("Número de valores ausentes:", valores_missing(df_correosmenos))
print("Mediana:", mediana(df_correosmenos))
print("Media:", media(df_correosmenos))
print("Varianza:", varianza(df_correosmenos))
print("Valor máximo:", maximo(df_correosmenos))
print("Valor mínimo:", minimo(df_correosmenos))