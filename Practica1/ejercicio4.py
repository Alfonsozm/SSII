import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import hashlib
from urllib.request import urlopen

con = sqlite3.connect('database.db')
cursorObj = con.cursor()


def usuarios_criticos():
    # Primero filtrar por contaseñas debiles y luego coger los que tengas mas emails clicados
    df = pd.read_sql_query("SELECT username, emails_clicados, contrasena FROM usuarios ORDER BY emails_clicados DESC",
                           con)
    lista_contrasenas = df["contrasena"].tolist()
    set_contrasenas = set(lista_contrasenas)

    # Creacion de .txt con hashes definitivamente eficiente XD
    # with open("realhuman_phill.txt", "r", encoding='ISO-8859-1') as file:
    #    pss = file.read()
    #
    # lista = set(pss.split("\n"))
    #
    # with open("hashes.txt", "w") as hashes:
    #    for password in lista:
    #        hashes.write(hashlib.md5(bytes(password, 'utf-8')).hexdigest() + "\n")

    #Más rápido que Raio Macuin
    set_hashes = set(line.strip() for line in open('hashes.txt'))

    matches = set()
    for password in set_contrasenas:
        if password in set_hashes:
            print("Contraseña vulnerable:", password)
            matches.add(password)

    #df_xd = pd.DataFrame()
    #for password in abc:
    #df_xd = pd.read_sql_query("SELECT username, emails_clicados FROM usuarios WHERE contrasena IN ({})".format(abc), con)
    df_xd = df[df["contrasena"].isin(matches)]
    df_xd = df_xd.head(10)
    print(df_xd)
    # for password in lista:
    #    #print(password)
    #    guess = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
    #    if guess in set_contrasenas:
    #        print("Contraseña vulnerable:", guess)
    #        x.add(guess)


def webs_politicas_desactualizadas():
    df = pd.read_sql_query("SELECT url, cookies, aviso, proteccion_de_datos FROM webs WHERE (cookies = 0 AND aviso = 0 "
                           "AND proteccion_de_datos = 0) OR (cookies = 0 AND aviso = 0) "
                           "OR (cookies = 0 AND proteccion_de_datos = 0) OR (aviso = 0 AND proteccion_de_datos = 0) "
                           "GROUP BY url LIMIT 5", con)
    print(df)


# grafico_criticos()
# usuarios_criticos()
usuarios_criticos()
# webs_politicas_desactualizadas()
