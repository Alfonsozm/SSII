import pandas as pd
import sqlite3
from flask import Flask, render_template, request
import altair as alt
import requests

con = sqlite3.connect('database.db', check_same_thread=False)
cursorObj = con.cursor()

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/users/")
def users():
    args = request.args
    amount = args.get("amount", default=10)
    df = df_critic_users(int(amount))
    chart = alt.Chart(df).mark_bar().encode(x="username", y="prob_click")
    df2 = df_spam_click(bool(args.get("greater", default=False)))

    return render_template('users.html', graphJSON=chart.to_json(), click=df2.to_html())


@app.route("/pages/")
def vuln_webs():
    args = request.args
    amount = args.get("amount", default=5)
    df = df_vuln_webs(int(amount))
    chart = alt.Chart(df).mark_bar().encode(x="url", y="Politicas")

    return render_template('pages.html', graphJSON=chart.to_json())


@app.route("/vulnerabilities/")
def vulns():
    return render_template('vulnerabilities.html', vulns=get_latest_vuln())


# Ejercicio 2
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


# Ejercicio 3
def df_spam_click(greater: bool):
    if greater:
        return pd.read_sql_query(
            "SELECT username,telefono,provincia,emails_total,emails_phishing,emails_clicados FROM usuarios where emails_clicados>usuarios.emails_phishing/2",
            con)
    else:
        return pd.read_sql_query(
            "SELECT username,telefono,provincia,emails_total,emails_phishing,emails_clicados FROM usuarios where emails_clicados<=usuarios.emails_phishing/2",
            con)


# Ejercicio 4
def get_latest_vuln():
    response = requests.get("https://cve.circl.lu/api/last")
    if response.status_code == 200:
        json = response.text
        df = pd.DataFrame()
        df["id"] = pd.read_json(json)["id"]
        print(df)
        df["summary"] = pd.read_json(json)["summary"]
        print(df)
        return df.head(10).to_html()
    else:
        raise Exception


if __name__ == '__main__':
    app.run()
