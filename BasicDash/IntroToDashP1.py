"""
Intro - Data Visualization Applications with Dash and Python p.1
https://pythonprogramming.net/data-visualization-application-dash-python-tutorial-introduction/
"""
import dash
import dash_core_components as dcc  # graphs
import dash_html_components as html  # tags

# start application
app = dash.Dash()

# the HTML of entire project

app.layout = html.Div(children=
                      [html.H1('Dash tutorial'),
                       dcc.Graph(id='example',
                                 figure={'data': [
                                     {'x': ['SA', 'QA', 'AE', 'KW', 'BH', 'OM'], 'y': [5, 6, 7, 2, 1, 8], 'type': 'bar', 'name': 'boats'},
                                     {'x': ['SA', 'QA', 'AE', 'KW', 'BH', 'OM'], 'y': [8, 3, 2, 3, 5, 8], 'type': 'bar', 'name': 'polarity'},
                                 ],
                                     'layout': {
                                         'title': 'Sentiment Analysis of Gulf States'
                                     }
                                 })
                       ])

if __name__ == '__main__':
    app.run_server(debug=True)

