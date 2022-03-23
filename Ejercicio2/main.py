import pandas as pd
import sqlite3
import json
import numpy as np
import math

con = sqlite3.connect('ejercicio1.db')
cursorObj = con.cursor()


def create() -> None:
    """Creación de la base de datos. Si ya existía, la borra."""
    cursorObj.execute("DROP TABLE IF EXISTS usuarios")
    cursorObj.execute("DROP TABLE IF EXISTS fechas")
    cursorObj.execute("DROP TABLE IF EXISTS ips")

    cursorObj.execute("CREATE TABLE usuarios (username text, telefono integer, contrasena text, provincia text, "
                      "permisos bool, emails_total integer, emails_phishing integer, emails_clicados integer, "
                      "constraint PK_usuarios primary key (username)) ")
    cursorObj.execute(
        "CREATE TABLE fechas (username text, fecha text, constraint PK_fechas primary key (username,fecha), "
        "constraint FK_fechas_usuarios foreign key (username) references usuarios(username))")
    cursorObj.execute(
        "CREATE TABLE ips (username text, ip text, constraint PK_ips primary key (username,ip), constraint "
        "FK_ips_usuarios foreign key (username) references usuarios(username))")
    con.commit()


def instantiate():
    """Lee el archivo users.json e inserta todos los valores en la base de datos.
    Si un valor es 'None', no se inserta nada.
    Esta función llama a create()"""
    create()
    with open("users.json", "r") as file:
        lines = json.load(file)

        for user in lines["usuarios"]:
            for username in user.keys():
                query = "INSERT INTO usuarios (username) VALUES (\'{}\')".format(username)
                cursorObj.execute(query)
                telefono = user[username]["telefono"]
                if telefono != 'None':
                    query = "UPDATE usuarios SET telefono = {} WHERE username = \'{}\'".format(telefono, username)
                    cursorObj.execute(query)
                query = "UPDATE usuarios SET contrasena = \'{}\' WHERE username = \'{}\'".format(
                    user[username]["contrasena"], username)
                cursorObj.execute(query)
                provincia = user[username]["provincia"]
                if provincia != 'None':
                    query = "UPDATE usuarios SET provincia = \'{}\' WHERE username = \'{}\'".format(provincia, username)
                    cursorObj.execute(query)
                permisos = user[username]["permisos"]
                query = "UPDATE usuarios SET permisos = {} WHERE username = \'{}\'".format(permisos, username)
                cursorObj.execute(query)
                emails_total = user[username]["emails"]["total"]
                query = "UPDATE usuarios SET emails_total = {} WHERE username = \'{}\'".format(emails_total, username)
                cursorObj.execute(query)
                emails_phishing = user[username]["emails"]["phishing"]
                query = "UPDATE usuarios SET emails_phishing = {} WHERE username = \'{}\'".format(emails_phishing,
                                                                                                  username)
                cursorObj.execute(query)
                emails_clicados = user[username]["emails"]["cliclados"]
                query = "UPDATE usuarios SET emails_clicados = {} WHERE username = \'{}\'".format(emails_clicados,
                                                                                                  username)
                cursorObj.execute(query)
                test = []
                for fecha in user[username]["fechas"]:
                    if fecha not in test:
                        query = "INSERT INTO fechas (username,fecha) VALUES (\'{}\',\'{}\')".format(username, fecha)
                        cursorObj.execute(query)
                        test.append(fecha)
                test = []
                if user[username]["ips"] == "None":
                    query = "INSERT INTO ips (username,ip) VALUES (\'{}\',Null)".format(username)
                    cursorObj.execute(query)
                else:
                    for ip in user[username]["ips"]:
                        if ip not in test:
                            query = "INSERT INTO ips (username,ip) VALUES (\'{}\',\'{}\')".format(username, ip)
                            cursorObj.execute(query)
                            test.append(ip)
    con.commit()


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
    return len(dataframe)*len(dataframe.columns) - valores_missing(dataframe)

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


instantiate()

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

