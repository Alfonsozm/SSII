import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from flask import Flask, render_template
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator

con = sqlite3.connect('database.db', check_same_thread=False)
cursorObj = con.cursor()

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/users/")
def users():
    return render_template('users.html')

@app.route("/pages/")
def vuln_webs():
    return render_template('pages.html')

@app.route("/vulnerabilities/")
def vulns():
    return render_template('vulnerabilities.html')


def df_critic_users(top: int):
    df = pd.read_sql_query("SELECT username, emails_clicados, emails_phishing, contrasena FROM usuarios", con)
    for index, row in df.iterrows():
        if row["emails_phishing"] != 0:
            df._set_value(index, "prob_click", row["emails_clicados"] / row["emails_phishing"])
        else:
            df._set_value(index, "prob_click", 0)
    df = df.sort_values("prob_click", ascending=False)

    with open("weak_pass.txt", "r") as file:
        weak_passwords = set(file.read().split("\n"))
    df = df[df["contrasena"].isin(weak_passwords)]
    df = df.head(top)
    return df


def df_vuln_webs(top: int):
    # Qué se entiende por web vulnerable?
    df = pd.read_sql_query("SELECT url, cookies, aviso, proteccion_de_datos FROM webs ORDER BY url", con)
    df["Politicas"] = df["cookies"] + df["aviso"] + df["proteccion_de_datos"]
    df = df.sort_values("Politicas").head(top)
    # df = df.replace({0:1, 1:0})
    return df




if __name__ == '__main__':
    app.run()
