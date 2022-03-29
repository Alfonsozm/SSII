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


@app.route('/users/graph')
def users_graph():
    df = df_critic_users(10)
    fig, ax = plt.subplots(figsize=(6, 5))
    plt.subplots_adjust(bottom=0.3)
    x = df["username"]
    y = df["prob_click"]
    ax.bar(x, y, color='r')
    plt.xticks(rotation=65)
    plt.xlabel("Usernames")
    plt.ylabel("Probability to click on phishing email")
    plt.title("Top x critic users")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/webs/graph')
def webs_graph():
    df = df_vuln_webs(10)
    fig, ax = plt.subplots(figsize=(6, 5))
    plt.subplots_adjust(bottom=0.4)
    x = df["url"]
    y = df["Politicas"]
    ax.bar(x, y, color='r')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xticks(rotation=90)
    plt.xlabel("url")
    plt.ylabel("Total de políticas actualizadas")
    plt.title("Top x vulnerable webs")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/users/")
def users():
    return render_template('users.html', url='/users/graph')


@app.route("/webs")
def webs():
    return render_template('webs.html', url='/webs/graph')


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
