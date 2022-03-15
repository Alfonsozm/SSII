import pandas as pd
import sqlite3
import json

con = sqlite3.connect('ejercicio1.db')


def create():
    cursorObj = con.cursor()
    cursorObj.execute("DROP TABLE IF EXISTS usuarios")
    cursorObj.execute("DROP TABLE IF EXISTS fechas")
    cursorObj.execute("DROP TABLE IF EXISTS ips")

    cursorObj.execute("CREATE TABLE usuarios (username text, telefono integer, contrasena text, provincia text, "
                      "permisos integer, emails_total integer, emails_phising integer, emails_clicados integer, constraint PK_usuarios primary key (username)) ")
    cursorObj.execute(
        "CREATE TABLE fechas (username text, fecha text, constraint PK_fechas primary key (username,fecha), constraint FK_fechas_usuarios foreign key (username) references usuarios(username))")
    cursorObj.execute(
        "CREATE TABLE ips (username text, ip text, constraint PK_ips primary key (username,ip), constraint FK_ips_usuarios foreign key (username) references usuarios(username))")
    con.commit()


def instantiate():
    create()
    cursorObj = con.cursor()
    with open("users.json", "r") as file:
        lines = json.load(file)

        for user in lines["usuarios"]:
            for usernames in user.keys():
                query = "INSERT INTO usuarios (username) VALUES ({})".format(usernames)

                cursorObj.execute(query)
    con.commit()


instantiate()
