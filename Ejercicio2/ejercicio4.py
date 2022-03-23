import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

con = sqlite3.connect('database.db')
cursorObj = con.cursor()


def grafico_criticos():
    # Cómo se que una contraseña es débil??
    df = pd.read_sql_query("SELECT username, emails_clicados FROM usuarios ORDER BY emails_clicados DESC LIMIT 10", con)
    eje_x = df["username"]
    eje_y = df["emails_clicados"]
    plt.bar(eje_x, eje_y)
    plt.ylabel("Emails clicados")
    plt.xlabel("Usuarios")
    plt.title("Usuarios críticos")
    plt.show()


def x(a, b):
    return a - b


def usuarios_criticos():
    df = pd.read_sql_query("SELECT username,emails_clicados FROM usuarios ORDER BY emails_clicados DESC LIMIT 10", con)
    print(df)
    df2 = pd.read_sql_query("SELECT username, COUNT(ip) FROM ips GROUP BY username", con)
    df2["Fechas"] = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas group by username", con)
    print(df2)

    #df2 = df2.assign(d_minus_a = df['COUNT(ip)'] - df['Fechas'])
    print(df2["COUNT(ip)"] - df2["Fechas"])


# grafico_criticos()

usuarios_criticos()
