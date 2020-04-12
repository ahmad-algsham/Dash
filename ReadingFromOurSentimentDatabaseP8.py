"""
# TODO add to project
Reading from our sentiment database - Sentiment Analysis GUI with Dash and Python p.3
https://pythonprogramming.net/twitter-sentiment-analysis-gui-dash-python/
"""
import sqlite3
import pandas as pd

conn = sqlite3.connect('twitter.db')
c = conn.cursor()

df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%car%' ORDER BY unix DESC LIMIT 1000", conn)
df.sort_values('unix', inplace=True)
df['smoothed_sentiment'] = df['sentiment'].rolling(int(len(df)/5)).mean()
df.dropna(inplace=True)

print(df.head())
