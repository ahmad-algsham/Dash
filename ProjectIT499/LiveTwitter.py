"""
# TODO add to project
Dynamically Graphing Terms for Sentiment - Sentiment Analysis GUI with Dash and Python p.5
https://pythonprogramming.net/search-for-term-twitter-sentiment-analysis-gui-dash-python/"""
import dash
from dash.dependencies import Output, Event, Input
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
    [
        html.H1('Live Twitter Sentiment'),
        dcc.Input(id='sentiment_term', value='', type='text'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
         id='graph-update',
         interval=1 * 1000
     ),
        dcc.Graph(id='live-graph2', animate=True),
        dcc.Graph(id='example',
                  figure={'data': [
                      {'x': ['SA', 'QA', 'AE', 'KW', 'BH', 'OM'], 'y': [5, 6, 7, 2, 1, 8], 'type': 'bar',
                       'name': 'boats'},
                      {'x': ['SA', 'QA', 'AE', 'KW', 'BH', 'OM'], 'y': [8, 3, 2, 3, 5, 8], 'type': 'bar',
                       'name': 'polarity'},
                  ],
                      'layout': {
                          'title': 'Sentiment Analysis of Gulf States'
                      }
                  })
     ]
)


@app.callback(Output('live-graph', 'figure'),
              [Input(component_id='sentiment_term', component_property='value')],
              events=[Event('graph-update', 'interval')])
def updata_graph(sentiment_term):
    try:
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()
        #                                                      the term
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 200", conn,
                         params=('%' + sentiment_term + '%',))
        df.sort_values('unix', inplace=True)
        df['date'] = pd.to_datetime(df['unix'], unit='ms')
        df.set_index('date', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df) / 5)).mean()
        df.dropna(inplace=True)
        # df = df.resample('100ms').mean()

        # X = df.unix.values[-100:]  # set in x-axis
        X = df.index[-100:]  # set in x-axis
        Y = df.sentiment_smoothed.values[-100:]  # set in y-axis

        data = go.Scatter(
            x=X,
            y=Y,
            name='Scatter',
            mode='lines+markers'
        )

        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                    yaxis=dict(range=[min(Y), max(Y)]),
                                                    title='Term: {}'.format(sentiment_term))}
    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')


if __name__ == '__main__':
    app.run_server(debug=True)
