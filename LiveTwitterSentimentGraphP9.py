"""
# TODO add to project
Live Graphs - Data Visualization GUIs with Dash and Python p.4
https://pythonprogramming.net/live-graphs-data-visualization-application-dash-python-tutorial/
"""

import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import sqlite3
import pandas as pd

app = dash.Dash(__name__)
app.layout = html.Div(
    [html.H1('Live Twitter Sentiment'),
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1000
    )
])


@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def updata_graph():
    try:
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()
        #                                                             the term
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%trump%' ORDER BY unix DESC LIMIT 1000", conn)
        df.sort_values('unix', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df) / 5)).mean()
        df.dropna(inplace=True)

        X = df.unix.values[-100:]  # set in x-axis
        Y = df.sentiment_smoothed.values[-100:]  # set in y-axis

        data = go.Scatter(
            x=list(X),  # x=X
            y=list(Y),  # y=Y
            name='Scatter',
            mode='lines+markers'
        )

        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                    yaxis=dict(range=[min(Y), max(Y)]))}
    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')


if __name__ == '__main__':
    app.run_server(debug=True)
