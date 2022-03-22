import pandas as pd
import sqlite3
import json
import numpy as np

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
    sum = 0
    with open("users.json", "r") as file:
        lines = json.load(file)

        for user in lines["usuarios"]:
            for username in user.keys():
                sum += 9
                query = "INSERT INTO usuarios (username) VALUES (\'{}\')".format(username)
                cursorObj.execute(query)
                telefono = user[username]["telefono"]
                if telefono != 'None':
                    query = "UPDATE usuarios SET telefono = {} WHERE username = \'{}\'".format(telefono, username)
                    cursorObj.execute(query)
                else:
                    sum -= 1
                query = "UPDATE usuarios SET contrasena = \'{}\' WHERE username = \'{}\'".format(
                    user[username]["contrasena"], username)
                cursorObj.execute(query)
                provincia = user[username]["provincia"]
                if provincia != 'None':
                    query = "UPDATE usuarios SET provincia = \'{}\' WHERE username = \'{}\'".format(provincia, username)
                    cursorObj.execute(query)
                else:
                    sum -= 1
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
                for ip in user[username]["ips"]:
                    if ip not in test:
                        query = "INSERT INTO ips (username,ip) VALUES (\'{}\',\'{}\')".format(username, ip)
                        cursorObj.execute(query)
                        test.append(ip)
    con.commit()
    return sum


def dataframe_users():
    users = []
    fechas = []
    emails = []
    ips = []
    for user in cursorObj.execute("SELECT username FROM usuarios").fetchall():
        users.append(user[0])
    for num in cursorObj.execute("SELECT COUNT(fecha) FROM fechas group by username").fetchall():
        fechas.append(num[0])
    for num in cursorObj.execute("SELECT emails_total FROM usuarios group by username").fetchall():
        emails.append(num[0])
    for num in cursorObj.execute("SELECT COUNT(ip) FROM ips group by username").fetchall():
        ips.append(num[0])
    data = {

        "Usuario": users,
        "Fechas": fechas,
        "Emails": emails,
        "IPs": ips
    }

    dataframe = pd.DataFrame(data)
    print(dataframe)


def media_fechas() -> float:
    """Calcula la media del total de fechas que se ha iniciado sesión."""
    sum = 0
    for num in cursorObj.execute("SELECT COUNT(fecha) FROM fechas group by username").fetchall():
        sum += num[0]
    return sum / cursorObj.execute("SELECT COUNT(DISTINCT(username)) FROM fechas").fetchone()[0]


def desviacion_fechas() -> float:
    """Calcula la desviación estándar del total de fechas que se ha iniciado sesión."""
    aux = []
    for num in cursorObj.execute("SELECT COUNT(fecha) FROM fechas group by username").fetchall():
        aux.append(num[0])
    return float(np.std(aux))


def max_fechas() -> int:
    """Calcula el valor máximo del total de fechas que se ha iniciado sesión"""
    aux = 0
    for num in cursorObj.execute("SELECT COUNT(fecha) FROM fechas group by username").fetchall():
        if aux < num[0]:
            aux = num[0]
    return aux


def min_fechas() -> int:
    """Calcula el valor mínimo del total de fechas que se ha iniciado sesión"""
    aux = float("inf")
    for num in cursorObj.execute("SELECT COUNT(fecha) FROM fechas group by username").fetchall():
        if aux > num[0]:
            aux = num[0]
    return aux


def media_ips() -> float:
    """Calcula la media del total de IPs que se han detectado"""
    sum = 0
    for num in cursorObj.execute("SELECT COUNT(ip) FROM ips group by username").fetchall():
        sum += num[0]
    return sum / cursorObj.execute("SELECT COUNT(DISTINCT(username)) FROM ips").fetchone()[0]


def desviacion_ips() -> float:
    """Calcula la desviación estándar del total de IPs que se han detectado"""
    aux = []
    for num in cursorObj.execute("SELECT COUNT(ip) FROM ips group by username").fetchall():
        aux.append(num[0])
    return float(np.std(aux))


def media_emails_totales() -> float:
    """Calcula la media del número de emails recibidos"""
    sum = 0
    for num in cursorObj.execute("SELECT emails_total FROM usuarios").fetchall():
        sum += num[0]
    return sum / cursorObj.execute("SELECT COUNT(username) FROM usuarios").fetchone()[0]


def desviacion_emails_totales() -> float:
    """Calcula la desviación estándar del número de emails recibidos"""
    aux = []
    for num in cursorObj.execute("SELECT emails_total FROM usuarios").fetchall():
        aux.append(num[0])
    return float(np.std(aux))


def max_emails_totales() -> int:
    """Calcula el valor máximo del número de emails recibidos"""
    return cursorObj.execute("SELECT MAX(emails_total) FROM usuarios").fetchone()[0]


def min_emails_totales() -> int:
    """Calcula el valor mínimo del número de emails recibidos"""
    return cursorObj.execute("SELECT MIN(emails_total) FROM usuarios").fetchone()[0]


instantiate()
print("Media del total de fechas que se ha iniciado sesión:\n", media_fechas())
print("Desviación estándar del total de fechas que se ha iniciado sesión:\n", desviacion_fechas())
print("Media del total de IPs que se han detectado:\n", media_ips())
print("Desviación estándar del total de IPs que se han detectado:\n", desviacion_ips())
print("Media del número de emails recibidos:\n", media_emails_totales())
print("Desviación estándar del número de emails recibidos:\n", desviacion_emails_totales())
print("Valor mínimo del total de fechas que se ha iniciado sesión:\n", min_fechas())
print("Valor máximo del total de fechas que se ha iniciado sesión:\n", max_fechas())
print("Valor mínimo del número de emails recibidos:\n", min_emails_totales())
print("Valor máximo del número de emails recibidos:\n", max_emails_totales())

dataframe_users()