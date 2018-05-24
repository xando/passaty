import pandas as pd


df = pd.read_csv(
    'passaty.csv',
    names=['year', 'distance', 'engine', 'power', 'color']
)


colors = df.groupby('color')['color'].count()
colors = df.groupby('year')['color'].count()


