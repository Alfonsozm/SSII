import pandas as pd
import sqlite3

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


print(dataframe_permisos(0))
print(dataframe_permisos(1))
print(dataframe_correos("mayor"))
print(dataframe_correos("menor"))
