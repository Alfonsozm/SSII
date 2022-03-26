import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
#import hashlib
#from urllib.request import urlopen

con = sqlite3.connect('database.db')
cursorObj = con.cursor()


def usuarios_criticos():
    """A partir de una wordlist de contraseñas he creado una wordlist con los hashes de estas contraseñas
    y las que coincidian con los hashes de las de los usuarios las he guardado en un .txt"""

    # lista_contrasenas = df["contrasena"].tolist()
    # set_contrasenas = set(lista_contrasenas)
    # Creacion de .txt con hashes definitivamente eficiente XD
    # with open("realhuman_phill.txt", "r", encoding='ISO-8859-1') as file:
    #    pss = file.read()
    #
    # lista = set(pss.split("\n"))
    #
    # with open("hashes.txt", "w") as hashes:
    #    for password in lista:
    #        hashes.write(hashlib.md5(bytes(password, 'utf-8')).hexdigest() + "\n")

    # Más rápido que Raio Macuin
    # set_hashes = set(line.strip() for line in open('hashes.txt'))

    # matches = set()
    # for password in set_contrasenas:
    #    if password in set_hashes:
    #        print("Contraseña vulnerable:", password)
    #        matches.add(password)

    # with open("weak_pass.txt", "w") as file:
    #    for hash in matches:
    #        file.write(hash+"\n")

    df = pd.read_sql_query("SELECT username, emails_clicados, emails_phishing, contrasena FROM usuarios",
                           con)
    for index, row in df.iterrows():
        if row["emails_phishing"] != 0:
            df._set_value(index, "prob_click", row["emails_clicados"] / row["emails_phishing"])
        else:
            df._set_value(index, "prob_click", 0)
    df = df.sort_values("prob_click", ascending=False)

    with open("weak_pass.txt", "r") as file:
        weak_passwords = set(file.read().split("\n"))
    df_xd = df[df["contrasena"].isin(weak_passwords)]
    df_xd = df_xd.head(10)

    indice = np.arange(len(df_xd))
    ancho = 0.35
    plt.bar(indice, df_xd['prob_click'], width=ancho, color='r', label='cookies')
    plt.xticks(indice + ancho, df_xd["username"])
    plt.xlabel('Usuarios')
    plt.ylabel('Probabilidad de click')
    plt.title('Top 10 usuarios críticos')
    plt.show()
    return df_xd


def webs_politicas_desactualizadas():
    df = pd.read_sql_query("SELECT url, cookies, aviso, proteccion_de_datos FROM webs ORDER BY url", con)
    df["Politicas"] = df["cookies"] + df["aviso"] + df["proteccion_de_datos"]
    df = df.sort_values("Politicas").head(5)
    df_aux = df.replace({0:1, 1:0})
    indice = np.arange(len(df_aux))
    ancho = 0.35
    plt.bar(indice, df_aux['cookies'], width=ancho, color='b', label='cookies')
    plt.bar(indice + ancho, df_aux['aviso'], width=ancho, color='r', label='aviso')
    plt.bar(indice + ancho, df_aux['proteccion_de_datos'], width=ancho, color='g', label='proteccion_de_datos')
    plt.xticks(indice + ancho, df_aux["url"])
    plt.xlabel('webs')
    plt.title('Top 5 webs desactualizadas')
    plt.show()
    return df


def media_conexiones_vulnerables(condicion: bool):
    if condicion:
        df = pd.read_sql_query(
            "SELECT username, contrasena FROM usuarios",
            con)
        df["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips group by username", con)
        with open("weak_pass.txt", "r") as file:
            weak_passwords = set(file.read().split("\n"))
        df_xd = df[df["contrasena"].isin(weak_passwords)]
        return df_xd["IPs"].sum() / len(df_xd)
    else:
        df = pd.read_sql_query(
            "SELECT username, contrasena FROM usuarios",
            con)
        df["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips group by username", con)
        with open("weak_pass.txt", "r") as file:
            weak_passwords = set(file.read().split("\n"))
        df_xd = df[~df["contrasena"].isin(weak_passwords)]
        return df_xd["IPs"].sum() / len(df_xd)


def webs_creacion():
    df = pd.read_sql_query("SELECT creacion, url, cookies, aviso, proteccion_de_datos FROM webs ORDER BY url", con)
    df["Politicas"] = df["cookies"] + df["aviso"] + df["proteccion_de_datos"]
    df_cumplen = df[df["Politicas"] == 3]
    print(df_cumplen)
    df_no_cumplen = df[df["Politicas"] != 3]
    print(df_no_cumplen)


def num_contrasenas_comprometidas():
    df = pd.read_sql_query(
        "SELECT username, contrasena FROM usuarios",
        con)
    df["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips group by username", con)
    with open("weak_pass.txt", "r") as file:
        weak_passwords = set(file.read().split("\n"))
    df_comprometidas = df[df["contrasena"].isin(weak_passwords)]
    df_no_comprometidas = df[~df["contrasena"].isin(weak_passwords)]
    print("Número de contraseñas comprometidas:", len(df_comprometidas))
    print("Número de contraseñas no comprometidas:", len(df_no_comprometidas))


print("10 usuarios más críticos:\n", usuarios_criticos())
print()
print("Webs con más políticas desactualizadas:\n", webs_politicas_desactualizadas())
print()
print("Media de conexiones de usuarios con contraseña vulnerable:", media_conexiones_vulnerables(True))
print("Media de conexiones de usuarios con contraseña no vulnerable:", media_conexiones_vulnerables(False))
print()
webs_creacion()
print()
num_contrasenas_comprometidas()
