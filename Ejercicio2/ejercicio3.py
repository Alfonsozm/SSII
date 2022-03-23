import pandas as pd
import sqlite3

con = sqlite3.connect('database.db')
cursorObj = con.cursor()


#def dataframe_administradores():
#    df = pd.read_sql_query("SELECT * FROM usuarios WHERE permisos = 1 group by username", con)
#    df["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(username) WHERE permisos = 1 "
#                                  "group by username", con)
#    df["Fechas"] = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(username) WHERE "
#                                     "permisos = 1 group by username", con)
#    return df
#
#
#def dataframe_usuarios():
#    df = pd.read_sql_query("SELECT * FROM usuarios WHERE permisos = 0 group by username", con)
#    df["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(username) WHERE permisos = 0 "
#                                  "group by username", con)
#    df["Fechas"] = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(username) WHERE "
#                                     "permisos = 0 group by username", con)
#    return df


def dataframe_permisos(permisos: int):
    #if permisos == 1:
    #    df = pd.read_sql_query("SELECT * FROM usuarios WHERE permisos = 1 group by username", con)
    #    df["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(username) WHERE permisos = 1 "
    #                                  "group by username", con)
    #    df["Fechas"] = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(username) WHERE "
    #                                     "permisos = 1 group by username", con)
    #    return df
    #if permisos == 0:
    #    df = pd.read_sql_query("SELECT * FROM usuarios WHERE permisos = 0 group by username", con)
    #    df["IPs"] = pd.read_sql_query(
    #        "SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(username) WHERE permisos = 0 "
    #        "group by username", con)
    #    df["Fechas"] = pd.read_sql_query(
    #        "SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(username) WHERE "
    #        "permisos = 0 group by username", con)
    #    return df
    #else:
    #    return "error"

    if permisos == 1 or permisos == 0:
        df = pd.read_sql_query("SELECT * FROM usuarios WHERE permisos = \'{}\' group by username".format(permisos), con)
        df["IPs"] = pd.read_sql_query("SELECT COUNT(ip) FROM ips INNER JOIN usuarios USING(username) WHERE permisos "
                                      "= \'{}\' group by username".format(permisos), con)
        df["Fechas"] = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas INNER JOIN usuarios USING(username) WHERE "
                                         "permisos = \'{}\' group by username".format(permisos), con)
        return df
    else:
        return "error"


print(dataframe_permisos(0))
print(dataframe_permisos(1))
