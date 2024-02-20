import pandas as pd


# df = pd.read_csv('data/a.csv', encoding="utf-32")

df = pd.read_excel('12.xlsx', na_values='None')


print(df.head())
print(df.columns)