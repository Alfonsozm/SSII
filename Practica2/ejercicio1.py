import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
con = sqlite3.connect('database.db')
cursorObj = con.cursor()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/grafico')
def usuarios_criticos():


    fig = plt.Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = np.random.rand(100)
    ys = np.random.rand(100)
    axis.plot(xs, ys)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
